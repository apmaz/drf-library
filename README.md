# DRF Library

## 🔧 Features

- Management of books, borrows, and payment 
- Borrow filtering by user and is_active parameter
- JWT authentication  
- Admin panel: [`/admin/`](http://localhost:8000/admin/) 
- Swagger documentation
- Tests

## 🛠 Technologies

- Python
- Django, Django REST Framework
- Django-Q
- Redis
- PostgreSQL
- Stripe
- Docker, Docker Compose


### 🐳 Installation

#### 1. Clone the project

```bash
git clone https://github.com/apmaz/drf-library.git
cd drf-library
```

#### 2. Rename `.env.sample` to `.env` and fill in the values:

```bash
mv .env.sample .env

# Django
SECRET_KEY=secret_key

# Telegram
BOT_TOKEN=bot_token
TELEGRAM_CHAT_ID=telegram_chat_id

# Sripe
STRIPE_SECRET_KEY=stripe_secret_key

# Postgres db
POSTGRES_USER=db_user
POSTGRES_DB=db_name
HOST=db_host
POSTGRES_PASSWORD=db_password
#
PGDATA=/var/lib/postgresql/data/

#Redis
REDIS_HOST=redis_host
REDIS_PORT=redis_port
```

#### 3. Build and run the project

```bash
docker-compose up --build
or
docker compose up --build
```

The service will be available at: [http://127.0.0.1:8000/api/v1/library/](http://127.0.0.1:8000/api/v1/library/)

# 👤 Users and Authentication
This section describes the main API endpoints for working with users: registration, obtaining and refreshing JWT tokens, token validation, and accessing the authenticated user’s profile information.

- Registration: [`/api/v1/library/user/register/`](http://127.0.0.1:8000/api/v1/library/user/register/)
- Token obtain: [`/api/v1/library/user/token/`](http://127.0.0.1:8000/api/v1/library/user/token/)
- Token refresh: [`/api/v1/library/user/token/refresh/`](http://127.0.0.1:8000/api/v1/library/user/token/refresh/)
- Token verify: [`/api/v1/library/user/token/verify/`](http://127.0.0.1:8000/api/v1/library/user/token/verify/)
- User profile: [`/api/v1/library/user/me/`](http://127.0.0.1:8000/api/v1/library/user/me/)

## 📚 Documentation
Here are links to the automatically generated API documentation using Swagger. You can explore available endpoints, their parameters, and example requests and responses:

- Swagger: [http://127.0.0.1:8000/api/v1/library/doc/swagger/](http://127.0.0.1:8000/api/v1/library/doc/swagger/)  


## 🧪 Testing

```bash
python manage.py test
```

## 🧩 Main Models

---

### Book
- Book:
- Title: str
- Author: str
- Cover: Enum: HARD | SOFT
- Inventory*: int
- Daily fee: decimal

---

### User
- Email: str
- First name: str
- Last name: str
- Password: str
- Is staff: bool

---

### Borrowing

- Borrow date: date
- Expected return date: date
- Actual return date: date
- Book id: int
- User id: int

### Payment

- Status: Enum: PENDING | PAID
- Type: Enum: PAYMENT | FINE
- Borrowing id: int
- Session url: Url  # url to stripe payment session
- Session id: str  # id of stripe payment session
- Money to pay: decimal (in $USD)  # calculated borrowing total price
