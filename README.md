# 🛒 Django E-commerce REST API

A robust and scalable backend API for E-commerce platforms built with **Django** and **Django REST Framework (DRF)**. This project includes essential e-commerce features like cart management, product reviews, wishlists, and seamless payment integration with **Stripe**.

---

## 📌 Features

- ✅ **Product Management:** Product List & Detail views (Slug-based).
- ✅ **Categories:** Categorized browsing with List & Detail views.
- ✅ **Shopping Cart:** Full cart functionality (Add / Update / Delete items).
- ✅ **Reviews:** Users can Add, Update, and Delete product reviews.
- ✅ **Wishlist:** Toggle mechanism to Add/Remove items.
- ✅ **Search:** Advanced search by Name, Description, or Category.
- ✅ **Payments:** Secure Stripe Checkout Integration.
- ✅ **Automation:** Stripe Webhook for automatic Order creation and Cart cleanup.
- ✅ **API Ready:** Fully RESTful API architecture suitable for React, Vue, Next.js, or Mobile Apps.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, Django, Django REST Framework
- **Database:** SQLite (Dev) / PostgreSQL (Recommended for Prod)
- **Authentication:** Django Custom User (Email-based)
- **Payment Gateway:** Stripe
- **Security:** CSRF exemption for Webhooks, Stripe Signature Verification.

---

## 📂 Project Structure

```text
CoreApiProject/
│
├── app/
│   ├── views.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│
├── CoreApiProject/
│   ├── settings.py
│   ├── urls.py
│
├── manage.py
├── .gitignore
└── README.md

```

## 2️ Create Virtual Environment & Installation

Clone Repo:
```bash
  git clone https://github.com/daCircuitSage/DRF-Ecommerce-API.git
```

For windows:
```bash
  python -m venv env
  env\Scripts\activate
```

For linux/mac:
```bash
  python3 -m venv env
  source env/bin/activate
```

### Configure Environment Variables
Open settings.py (or create a .env file) and add your Stripe keys:
```bash
STRIPE_SECRET_KEY = "sk_test_************"
WEBHOOK_SECRET = "whsec_************"
```

### Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```
### Create Superuser
```bash
python manage.py createsuperuser
```

### Run Server
```bash
python manage.py runserver
#The API will be available at http://127.0.0.1:8000/
```

## 🔗 API Endpoints & Usage






#### Get Featured Product List

```http
  GET /api/product_list/
```

#### Get Single Product (Slug Based)

```http
  GET /api/product/<slug>/
```

#### Category List

```http
  GET /api/category_list/
```

#### Category Detail

```http
  GET /api/category/<slug>/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `slug`      | `string` | **Required** slug of item to fetch |


#### Add Product to Cart

```http
  POST /api/add_to_cart/
```
##### Postman:
| Key | Value     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `cart_code`      | `string` | **Required** cart code of the cart |
| `product_id`      | `string` | **Required** product id of the product |

#### Update Cart Item Quantity

```http
  PUT /api/update_cartitem/
```
##### Postman:
| Key | Value     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `cartitem_id`      | `string` | **Required** cartitem id of the cartitem |
| `quantity`      | `string` | **Required** quantity to update |


#### Delete Cart Item

```http
  DELETE /api/delete_cartitem/<id>/
```



#### Add Review

```http
  POST /api/add_review/
```
##### Postman:
| Key | Value     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `product_id`      | `string` | **Required** id of the product |
| `rating`      | `string` | **Required** add rating 1,2,3,4 or 5 |
| `review_text`      | `string` | **Required** review_text as review |
| `email`      | `string` | **Required** email to identity user |



#### Update Review

```http
  PUT /api/update_review/<id>/
```


#### Delete Review

```http
  DELETE /api/delete_review/<id>/
```

#### Add Wishlist

```http
  POST /api/add_to_wishlist/
```
##### Postman:
| Key | Value     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `email`      | `string` | **Required** email to indentify the user |
| `product_id`      | `string` | **Required** product id of the product |


#### 🔍 Product Search API

```http
  GET /api/product_search?search=phone
```
##### Postman:
| Search Works on |  |                      |
| :-------- | :------- | :-------------------------------- |
| `product name`      |  
| `product description`      |
| `category name`      | 

### 💳 Stripe Payment Integration
#### Create Stripe Checkout Session

```http
  POST /api/create_checkout_session/
```
##### Postman:
| Key | Value     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `cart_code`      | `string` | **Required** code of the cart |
| `email`      | `string` | **Required** email to identify the user|

#### Stripe Payment Flow

 1. User adds products to cart

 2. Checkout session created

 3. User completes payment via Stripe

 4. Stripe webhook triggered

 5. Order & OrderItems created automatically

 6. Cart deleted


#### Stripe Webhook Endpoint

```http
  POST /api/webhook/
```
##### Postman:
| Handled Events |      |                        |
| :-------- | :------- | :-------------------------------- |
| `checkout.session.completed`      | 
| `checkout.session.async_payment_succeeded`      | 

#### 📦 Order System

Order automatically created after successful payment

OrderItems generated from CartItems

Stripe Checkout ID stored for tracking

Payment status marked as Paid

#### 🔐 Security Notes

Stripe Webhook Signature Verification enabled

CSRF disabled only for Stripe webhook

Sensitive keys should be stored as Environment Variables in production

## Authors

- [@daCircuitSage](https://github.com/daCircuitSage)

