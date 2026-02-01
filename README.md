# Blood Bank Management System (BMS)

## Overview
The Blood Bank Management System is a Django REST Framework (DRF) project that connects blood donors and recipients in a seamless, efficient way. Users can create accounts, request blood, accept donation requests, and track their donation history. JWT authentication ensures secure access, and Cloudinary is used for image storage.

---

## Features

### 1. User Management
- Custom User model with fields:
  - `username`, `email`, `age`, `address`, `blood_group`, `gender`, `is_available`, `last_donation_date`, `image`
- JWT authentication via **Simple JWT**
- Djoser used for registration, login, and email verification
- Admin-only delete; users can update only their own profile

### 2. Donor Profiles
- Auto-created when a new user registers
- Fields:
  - `user` (OneToOne), `image`, `last_donation_date`, `is_available`
- Users can update their own profile
- Admin can delete any profile

### 3. Blood Requests
- Users can create blood requests
- Fields:
  - `recipient` (auto set to request.user), `blood_group`, `location`, `description`, `is_active`, `created_at`
- Admin-only delete
- Other users can accept requests → creates `DonationHistory` entry

### 4. Donation History
- Tracks donations with fields:
  - `donor`, `request`, `status` (`donated`, `received`, `cancelled`), `date`
- Users can see their own history
- Admin can see all histories

### 5. Image Handling
- User and donor images uploaded to **Cloudinary**
- `ImageField` integrated with `django-cloudinary-storage`
- Supports multipart/form-data uploads

### 6. Search & Filter
- Blood requests can be filtered by blood group
- Donor search available in API

### 7. Dashboard (Authenticated Users)
- View recipient requests
- Accept requests (donation history auto-created)
- View own donation history

### 8. Swagger / API Documentation
- `drf-yasg` used for API documentation
- JWT token authentication works in Swagger UI
- All endpoints annotated with `swagger_auto_schema` for GET, POST, UPDATE, DELETE

---

## Tech Stack
- Backend: Django 6.0, Django REST Framework
- Authentication: JWT (Simple JWT)
- Image Storage: Cloudinary
- Documentation: Swagger (drf-yasg)
- Languages: Python
- Frontend ready for React / Tailwind integration

---

## Installation

```bash
git clone <repo-url>
cd blood_bank
python -m venv .env
source .env/bin/activate  # or .env\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
# Blood Bank API Endpoints

| Method | URL                         | Description                                        | Auth / Permission                |
|--------|-----------------------------|--------------------------------------------------|---------------------------------|
| POST   | /auth/users/                | Register new user                                 | Public                          |
| POST   | /auth/jwt/create/           | Login, get JWT token                              | Public                          |
| POST   | /auth/jwt/refresh/          | Refresh JWT token                                 | Auth                             |
| GET    | /api/v1/me/                 | Get logged-in user info                            | Auth                             |
| GET    | /api/v1/donors/             | List all donor profiles                            | Auth                             |
| GET    | /api/v1/donors/{id}/        | Retrieve specific donor profile                   | Auth                             |
| PATCH  | /api/v1/donors/{id}/        | Update own donor profile                           | Owner                            |
| DELETE | /api/v1/donors/{id}/        | Delete donor profile                               | Admin only                       |
| GET    | /api/v1/requests/           | List all blood requests                             | Auth                             |
| POST   | /api/v1/requests/           | Create a new blood request (recipient auto-set)   | Auth                             |
| GET    | /api/v1/requests/{id}/      | Retrieve specific blood request                    | Auth                             |
| PATCH  | /api/v1/requests/{id}/      | Update a blood request                              | Owner / Auth                     |
| DELETE | /api/v1/requests/{id}/      | Delete a blood request                              | Admin only                       |
| GET    | /api/v1/histories/          | List donation history                               | Auth                             |
| POST   | /api/v1/histories/          | Create a donation history record                   | Auth                             |
| GET    | /api/v1/histories/{id}/     | Retrieve a specific donation history record       | Owner / Admin                     |
| PATCH  | /api/v1/histories/{id}/     | Update donation history record                     | Owner / Admin                     |
| DELETE | /api/v1/histories/{id}/     | Delete donation history record                     | Admin only                       |
| GET    | /swagger/                   | Swagger interactive API documentation             | Public                           |
| GET    | /redoc/                     | ReDoc API documentation                            | Public                           |
