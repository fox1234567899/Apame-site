# 🧠 Backend (Django REST Framework)

This project’s backend is built with Django REST Framework and provides a full API for the e-commerce frontend.

It handles authentication, product management, cart system, orders, and payment transactions.

---

## 📦 Core Models

The database structure is designed like a relational system (similar to tables in Excel), where each model represents a key business entity:

- **Item** → product details (name, price, image, description, slug)
- **Cart** → user shopping cart
- **CartItem** → items inside the cart with quantity
- **Order** → completed purchase records
- **OrderItem** → individual items inside an order
- **Transaction** → payment tracking and verification

These models allow the system to track users’ shopping and payment flow step by step.

---

## 🔄 Django REST Framework (Serializers)

Serializers are used to convert complex Django models into JSON format so that the frontend (React) can understand and use the data.

You can think of serializers as a “translator” between Django and React:

- Django works with Python objects
- React works with JSON data
- Serializers convert between them

Example:
Product detail API returns:
- id
- slug
- name
- price
- image
- description
- similar items

---

## 🌐 Views & API Logic

Views are responsible for handling requests and sending responses.

Example flow:
1. Query database (e.g., all Items)
2. Pass data to serializer
3. Return JSON response to frontend

These views are connected to endpoints through `urls.py`.

---

## 🔐 Authentication (JWT)

Authentication is handled using **JWT (JSON Web Tokens)**:

- Access token → used for API requests
- Refresh token → used to generate new access tokens

This allows secure login and protected routes such as:
- Cart
- Checkout
- Profile
- Orders

---

## 💳 Payment System

The backend handles payment verification using a `Transaction` model.

Flow:
1. User initiates payment
2. Payment gateway processes transaction
3. Backend verifies payment status
4. If successful:
   - Order is created
   - Cart is cleared
   - Transaction is marked as completed

---

## 🗄️ Database

Initially developed with SQLite, then migrated to **PostgreSQL** for production use.

Later integrated with **Supabase** to store and manage PostgreSQL data in the cloud.

---

## ☁️ Supabase Integration

Supabase is used for cloud database and media storage.

### Installation:
```bash
pip install django-supabase-storage 


# Django Settings:

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_BUCKET = os.getenv('SUPABASE_BUCKET_NAME')

STORAGES = {
    'default': {
        'BACKEND': 'django_supabase_storage.SupabaseMediaStorage',
    },
    'staticfiles': {
        'BACKEND': 'django_supabase_storage.SupabaseStaticStorage',
    },
}