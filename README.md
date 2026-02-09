# eCommerce Application

A modern Django-based eCommerce platform with traditional server-side rendering, supporting buyer and vendor roles, product management, shopping cart functionality, and order processing.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [API Sequence Diagram](#api-sequence-diagram)
- [Security Features](#security-features)

## 🎯 Overview

This eCommerce application is built with Django 5.2.x using traditional server-side rendering approach. The platform supports two user types:
- **Buyers**: Can browse products, add items to cart, checkout, and leave reviews
- **Vendors**: Can create stores, manage products

## ✨ Features

### User Management
- User registration with role selection (Buyer/Vendor)
- Secure authentication and login system
- Password reset functionality via email
- Logout functionality
- Role-based access control

### For Vendors
- Create and manage multiple stores
- Add, edit, and delete products
- Organize products by store
- View product listings and details

### For Buyers
- Browse all available products
- View detailed product information
- Add products to shopping cart (fixed cart button in upper right corner)
- Update cart quantities
- Remove items from cart
- Checkout with email confirmation
- Leave product reviews with star ratings

### Shopping Cart
- Session-based cart storage
- Persistent during browser session
- Add/update/remove items
- Real-time quantity management
- Total price calculation
- Checkout confirmation page

### Product Reviews
- 5-star rating system
- Written reviews with comments
- Verified purchase tracking
- Timestamp for each review

### Order Management
- Order creation on checkout
- Email confirmation sent to buyer
- Order tracking with unique order IDs
- Order item details preserved

## 🛠️ Technology Stack

- **Framework**: Django 6.0.2
- **Language**: Python 3.12
- **Database**: MariaDB (MySQL-compatible)
- **Database Driver**: mysqlclient 2.2.7+
- **Frontend**: HTML5, Bootstrap 4, Django Templates
- **API Framework**: Django REST Framework 3.16.1+
- **Authentication**: Django built-in + REST Framework Basic Auth
- **Email Backend**: Console (development) / SMTP (production)
- **Session Management**: Django sessions
- **Architecture**: Hybrid - Server-side rendering + RESTful API
- **X (Twitter) Integration**: Tweepy (optional)



## 📦 Installation

### Prerequisites
- Python 3.12 or higher
- MariaDB or MySQL (if running without Docker)
- pip (Python package manager)
- Virtual environment (recommended)

### Docker (Single Image)

Run the app and embedded MariaDB with a single command:

```
docker run -d -p 8000:8000 --name ecommerce_app wernerval/capstone-final:latest

```

### X (Twitter) API (Optional)

This project can post tweets when a new store or product is created. Tweets are sent via Django signals in [store/signals.py](store/signals.py) and [product/signals.py](product/signals.py).

**Requirements**
- X Developer app with OAuth 1.0a access token/secret
- App permissions set to **Read and Write**
- Sufficient API credits (X will return 402 if credits are depleted - which it does on my end, and I am not loading credits)

**Environment variables**
- `X_TWEETS_ENABLED=true`
- `X_API_KEY=...`
- `X_API_SECRET=...`
- `X_ACCESS_TOKEN=...`
- `X_ACCESS_TOKEN_SECRET=...`

## Usage Guide

### Access the Application
- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Products**: http://127.0.0.1:8000/products/
- **Cart**: http://127.0.0.1:8000/cart/

### Getting Started

1. **Register as a User**
   - Navigate to the registration page
   - Choose user type (Buyer or Vendor)
   - Complete the registration form

2. **For Vendors**
   - Login with your credentials
   - Create a new store
   - Add products to your store
   - Manage your product inventory

3. **For Buyers**
   - Login with your credentials
   - Browse available products
   - Add items to cart using the fixed cart button
   - Proceed to checkout
   - Leave reviews for purchased products

```
ecommerce_app/
│
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── ecommerce_app/              # Main project configuration
│   ├── __init__.py
│   ├── settings.py            # Project settings (includes MariaDB config)
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py                # WSGI configuration
│   ├── asgi.py                # ASGI configuration
│   └── templates/
│       ├── base.html          # Base template with navigation
│       └── home.html          # Landing page
│
├── users/                      # User management app
│   ├── models.py              # Custom User model
│   ├── views.py               # Auth views (register, login, logout)
│   ├── urls.py                # User-related URLs
│   ├── admin.py               # Admin configuration
│   ├── apps.py
│   └── templates/
│       ├── login.html
│       ├── register.html
│       ├── password_reset_request.html
│       └── password_reset_confirm.html
│
├── store/                      # Store management app
│   ├── models.py              # Store model
│   ├── views.py               # Store CRUD views
│   ├── urls.py                # Store URLs
│   ├── admin.py
│   └── templates/
│       └── store/
│           ├── store_list.html
│           ├── store_detail.html
│           ├── store_form.html
│           └── store_confirm_delete.html
│
├── product/                    # Product management app
│   ├── models.py              # Product model
│   ├── views.py               # Product CRUD views
│   ├── urls.py                # Product URLs
│   ├── admin.py
│   └── templates/
│       └── product/
│           ├── product_list.html       # With fixed cart button
│           ├── product_detail.html
│           ├── product_form.html
│           └── product_confirm_delete.html
│
├── cart/                       # Shopping cart app
│   ├── models.py              # Order and OrderItem models
│   ├── views.py               # Cart operations
│   ├── urls.py                # Cart URLs
│   ├── cart.py                # Cart session class
│   └── templates/
│       └── cart/
│           ├── cart.html
│           ├── checkout_confirm.html
│           └── checkout_success.html
│
└── reviews/                    # Product review app
    ├── models.py              # Review model
    ├── views.py               # Review views
    ├── urls.py                # Review URLs
    ├── admin.py
    └── templates/
        └── reviews/
            ├── review_list.html
            ├── review_detail.html
            └── review_form.html
```


**Key Features:**
- UTF8MB4 character set for full Unicode support (including emojis)
- Decimal fields for accurate currency calculations
- ACID compliance for reliable transactions
- Optimized for concurrent user access


```

### Security Settings
```python
AUTH_USER_MODEL = 'users.User'
PASSWORD_RESET_TIMEOUT = 7200  # 2 hours
DEBUG = True  # Set to False in production
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
```

## 🔒 Security Features

- CSRF protection on all forms
- Password hashing with Django's default hasher
- Password validation (minimum 8 characters, must contain uppercase and digit)
- Role-based access control (buyer/vendor separation)
- Django's built-in XSS protection
- SQL injection protection via Django ORM
- Session security with automatic expiration
- Basic Authentication for API endpoints
- Permission-based API access control

---

## 🚀 REST API Documentation

The application provides a comprehensive RESTful API with JSON and XML response formats.

### Base URL
```
http://127.0.0.1:8000
```

### Authentication
Most POST endpoints require Basic Authentication:
```
Authorization: Basic <base64(username:password)>
```

### Response Formats
- **JSON** (default): Accept: application/json
- **XML**: Accept: application/xml

---

## 📍 API Endpoints

### **Store API**

#### Get All Stores (JSON)
```http
GET /get/stores
```
**Response**: List of all stores with id, name, and category

#### Get All Stores (XML)
```http
GET /get/stores/xml
```
**Response**: XML format list of stores

#### Create Store
```http
POST /add/store
Authorization: Basic <credentials>
```
**Body**:
```json
{
  "store_name": "Electronics Hub",
  "store_category": "electronics"
}
```
**Permissions**: Authenticated vendors only

---

### **Product API**

#### Get All Products (JSON)
```http
GET /get/products
```
**Response**: List of all products with details

#### Get All Products (XML)
```http
GET /get/products/xml
```

#### Create Product
```http
POST /add/product
Authorization: Basic <credentials>
```
**Body**:
```json
{
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": "999.99",
  "store": 1
}
```
**Permissions**: Authenticated vendors only

---

### **Order API**

#### Get All Orders (JSON)
```http
GET /cart/get/orders
```
**Response**: List of all orders

#### Get All Orders (XML)
```http
GET /cart/get/orders/xml
```

#### Create Order
```http
POST /cart/add/order
Authorization: Basic <credentials>
```
**Body**:
```json
{
  "user": 1,
  "total_amount": "149.99",
  "status": "completed"
}
```
**Permissions**: Authenticated users, must match logged-in user ID

---

### **Review API**

#### Get All Reviews (JSON)
```http
GET /get/reviews
```

#### Get All Reviews (XML)
```http
GET /get/reviews/xml
```

#### Create Review
```http
POST /add/review
Authorization: Basic <credentials>
```
**Body**:
```json
{
  "product": 1,
  "user": 1,
  "username": "john_doe",
  "rating": 5,
  "comment": "Excellent product!",
  "is_verified_purchase": true
}
```
**Permissions**: Authenticated users, must match logged-in user ID

---

### **User API**

#### Get All Users (JSON) - Admin Only
```http
GET /get/users
Authorization: Basic <admin_credentials>
```
**Permissions**: Admin users only

#### Get All Users (XML) - Admin Only
```http
GET /get/users/xml
Authorization: Basic <admin_credentials>
```

#### Register New User
```http
POST /api/register
```
**Body**:
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "buyer"
}
```
**Permissions**: Public endpoint (no authentication required)

---

## 📝 API Examples

### Example: Get All Products
```bash
curl http://127.0.0.1:8000/get/products
```

### Example: Create a Store (with authentication)
```bash
curl -X POST http://127.0.0.1:8000/add/store \
  -u username:password \
  -H "Content-Type: application/json" \
  -d '{"store_name":"Tech Store","store_category":"electronics"}'
```

### Example: Get Products in XML
```bash
curl -H "Accept: application/xml" http://127.0.0.1:8000/get/products/xml
```

---

## ⚙️ API Configuration

REST Framework settings in `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}
```

