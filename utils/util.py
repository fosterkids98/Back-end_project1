from datetime import datetime, timedelta, timezone
from jose import jwt
import jose
from flask import request, jsonify
from functools import wraps

SECRET_KEY = "a super secret, secret key"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization', None)
        print(f"[Auth Header] Raw: {auth_header}")

        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
                print(f"[Extracted Token] {token}")
            else:
                print("[Auth Header Format] Invalid format")
        else:
            print("[Auth Header Missing] No Authorization header found")

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user_id = data['sub']
            print(f"[JWT Decode] Success - User ID: {current_user_id}")
        except jose.exceptions.ExpiredSignatureError:
            print("[JWT Error] Token expired")
            return jsonify({'message': 'Token has expired!'}), 401
        except jose.JWTError as e:
            print(f"[JWT Error] Invalid token: {e}")
            return jsonify({"message": "Token is invalid!"}), 401

        return f(*args, current_user_id=current_user_id, **kwargs)
    return decorated


def encode_token(customer_id):
    now = datetime.now(timezone.utc)
    payload = {
        'exp': int((now + timedelta(hours=1)).timestamp()),
        'iat': int(now.timestamp()),
        'sub': str(customer_id)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def encode_refresh_token(customer_id):
    now = datetime.now(timezone.utc)
    payload = {
        'exp': int((now + timedelta(hours=1)).timestamp()),
        'iat': int(now.timestamp()),
        'sub': str(customer_id)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def mechanic_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing'}), 401
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'message': 'Invalid token format'}), 401
        
        mechanic_token = parts[1]
        try:
            data = jwt.decode(mechanic_token, SECRET_KEY, algorithms=['HS256'])
            if data.get('role') != 'mechanic':
                raise jose.JWTError('Not a mechanic')
            mechanic_id = data['sub']
        except jose.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jose.JWTError:
            return jsonify({'message': 'Not authorized as mechanic'}), 401
        
        return f(*args, current_mechanic_id=mechanic_id, **kwargs)
    return decorated


def encode_mechanic_token(mechanic_id):
    now = datetime.now(timezone.utc)
    payload = {
        'exp': int((now + timedelta(hours=1)).timestamp()),
        'iat': int(now.timestamp()),
        'sub': str(mechanic_id),
        'role': 'mechanic'
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
