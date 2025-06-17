# Kia Garage Service API

This is a Flask RESTful API for managing service tickets, inventory parts, and mechanic/customer operations in a car service center.

---

## 🔧 Features

- JWT-based authentication for customers and mechanics
- Assign mechanics to service tickets
- Add/remove parts (inventory items) to service tickets
- Track cost and part usage per ticket
- Customer and mechanic management

---

## 🚀 Quick Start

# Folder Setup

body_shop/
├── __init__.py
├── app.py
├── config.py
├── extensions.py
├── models.py
├── blueprints/
│   ├── customer/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── inventory/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── mechanic/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── service_ticket/
│       ├── __init__.py
│       └── routes.py
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   └── validators.py

# Windows
python -m venv body_shop
body_shop\Scripts\activate

# macOS/Linux
python3 -m venv body_shop
source body_shop/bin/activate

# Install Dependencies
pip install blinker cachelib click colorama Deprecated ecdsa Flask==3.1.1 Flask-Caching==2.3.1 Flask-Limiter==3.12 flask-marshmallow==1.3.0 Flask-SQLAlchemy==3.1.1 greenlet==3.2.3 itsdangerous==2.2.0 Jinja2==3.1.6 limits==5.2.0 markdown-it-py==3.0.0 MarkupSafe==3.0.2 marshmallow==4.0.0 marshmallow-sqlalchemy==1.4.2 mdurl==0.1.2 mysql-connector-python==9.3.0 ordered-set==4.1.0 packaging==25.0 pyasn1==0.6.1 Pygments==2.19.1 python-jose==3.5.0 rich==13.9.4 rsa==4.9.1 six==1.17.0 SQLAlchemy==2.0.41 typing_extensions==4.14.0 Werkzeug==3.1.3 wrapt==1.17.2


```bash
git clone https://github.com/your-username/kia-garage-api.git
cd kia-garage-api
