# 📚 Library Management System

A full-stack **Library Management System** built with **Python, Django, HTML, CSS, and PostgreSQL**. It lets users browse and search books, request to issue/return them, and gives admins tools to manage the catalog and users.

## Features

- User registration and login
- Role-based access — Admin and User roles
- Add, update, delete, and view books
- Search books by title/author/category
- Issue and return book requests
- Issue request management (approve/reject) for admins
- User management dashboard
- Password reset

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django, Django ORM |
| Database | PostgreSQL |
| Frontend | HTML, CSS |

## Project Structure

```
library-management-system/
├── Library/          # Django project settings/config
├── library_app/       # Core app: models, views, urls
├── templates/          # HTML templates
├── manage.py
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.x
- PostgreSQL installed and running

### Installation

```bash
git clone https://github.com/RekhapalliUmaSatyaSantosh/library-management-system.git
cd library-management-system

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install django psycopg2-binary
```

### Configure the Database

Update the `DATABASES` setting in `Library/settings.py` with your PostgreSQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Run Migrations and Start the Server

```bash
python manage.py migrate
python manage.py createsuperuser   # optional, for admin access
python manage.py runserver
```

Open the app in your browser:

```
http://127.0.0.1:8000/
```

## Usage

- **Users** can register, log in, search the catalog, and submit issue/return requests for books.
- **Admins** can log in to add/update/delete books, manage users, and approve or reject issue requests.

## Roadmap / Ideas for Improvement

- [ ] REST API endpoints for mobile/frontend integration
- [ ] Email notifications for due dates and approvals
- [ ] Book cover image uploads
- [ ] Unit tests and CI pipeline

## Author

**Uma Satya Santosh Rekhapalli**
GitHub: [@RekhapalliUmaSatyaSantosh](https://github.com/RekhapalliUmaSatyaSantosh)
LinkedIn: [uma-satya-santosh-rekhapalli](https://linkedin.com/in/uma-satya-santosh-rekhapalli/)

## License

This project currently has no license specified. Add a `LICENSE` file (e.g., MIT) if you'd like others to reuse this code.
