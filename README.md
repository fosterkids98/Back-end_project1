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
- ├── __init__.py
- ├── app.py
- ├── config.py
- ├── extensions.py
- ├── models.py
- ├── blueprints/
- │   ├── customer/
- │   │   ├── __init__.py
- │   │   └── routes.py
- │   ├── inventory/
- │   │   ├── __init__.py
- │   │   └── routes.py
- │   ├── mechanic/
- │   │   ├── __init__.py
- │   │   └── routes.py
- │   └── service_ticket/
- │       ├── __init__.py
- │       └── routes.py
- ├── utils/
- │   ├── __init__.py
- │   ├── helpers.py
- │   └── validators.py

# Windows
python -m venv body_shop
body_shop\Scripts\activate

# macOS/Linux
python3 -m venv body_shop
source body_shop/bin/activate

# Install Dependencies
pip install blinker cachelib click colorama Deprecated ecdsa Flask==3.1.1 Flask-Caching==2.3.1 Flask-Limiter==3.12 flask-marshmallow==1.3.0 Flask-SQLAlchemy==3.1.1 marshmallow==4.0.0 marshmallow-sqlalchemy==1.4.2 mysql-connector-python==9.3.0 python-jose==3.5.0 SQLAlchemy==2.0.41 wrapt==1.17.2


```bash
git clone https://github.com/your-username/kia-garage-api.git
cd kia-garage-api
