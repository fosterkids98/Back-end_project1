from jose import jwt, JWTError, ExpiredSignatureError
from flask import request, jsonify, abort, Blueprint
import jose
from . import customer_bp
from ...models import Customer
from ...extensions import db, limiter, cache
from .schemas import customer_schema, customers_schema
from ...utils.util import encode_token, encode_refresh_token, token_required, SECRET_KEY


@customer_bp.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    if not refresh_token:
        return jsonify({'message': 'Refresh token is missing!'}), 401
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=['HS256'])
        customer_id = payload['sub']
        new_token = encode_token(str(customer_id))
        return jsonify({'token': new_token}), 200
    except jose.exceptions.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token has expired!'}), 401
    except jose.JWTError:
        return jsonify({'message': 'Invalid refresh token!'}), 401
    
@customer_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    customer = Customer.query.filter_by(email=email, password=password).first()
    if not customer:
        print("[Login Failed] Invalid credentials")
        return jsonify({"error": "Invalid credentials"}), 401

    token = encode_token(customer.id)
    refresh_token = encode_refresh_token(customer.id)

    print(f"[Login Success] ID: {customer.id}")
    print(f"[Token] {token}")
    print(f"[Refresh Token] {refresh_token}")

    return jsonify({
        "token": token,
        "refresh_token": refresh_token
    }), 200

@customer_bp.route('/', methods=['GET'])
@token_required
def get_customers(current_user_id=None):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    paginated = Customer.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'items': customers_schema.dump(paginated.items),
        'page': paginated.page,
        'total': paginated.total,
        'pages': paginated.pages,
    })


@customer_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return customer_schema.dump(customer)

@customer_bp.route('/', methods=['POST'])
@limiter.limit("20 per hour")
def create_customer():
    data = request.get_json()

    try:
        if isinstance(data, list):
            # Bulk create
            customers = customers_schema.load(data, session=db.session)
            db.session.add_all(customers)
            db.session.commit()
            return customers_schema.dump(customers), 201

        elif isinstance(data, dict):
            # Single create
            new_customer = customer_schema.load(data, session=db.session)
            db.session.add(new_customer)
            db.session.commit()
            return customer_schema.dump(new_customer), 201

        else:
            return jsonify({"error": "Invalid data format. Expected a JSON object or list."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@customer_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_customer(id, current_user_id=None):
    customer = Customer.query.get_or_404(id)
    updated_customer = customer_schema.load(request.json, instance=customer, partial=True, session=db.session)
    db.session.commit()
    return customer_schema.dump(updated_customer)

@customer_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_customer(id, current_user_id=None):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return '', 204

""""""