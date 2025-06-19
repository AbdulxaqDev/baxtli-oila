# HappyFamily Django Application

## Overview

HappyFamily is a web-based student and teacher management system built with Django and MongoDB.  
It enables admins to manage student and user records efficiently with role-based access control, inline editing, filtering, and secure authentication.

---

## Features

- User authentication with custom user model (roles: admin, teacher)
- Student management: list, filter, add, update, delete
- User management: list, add, update, delete (admin only)
- Inline editable tables with visual editing cues
- Responsive, mobile-friendly UI with Bootstrap and custom styling
- MongoDB backend for flexible document storage
- Role-based access control and secure login/logout
- Static files management and deployment-ready setup

---

## Tech Stack

- Backend: Python 3.x, Django 5.x
- Database: MongoDB
- Frontend: HTML5, CSS3, Bootstrap 5, JavaScript (Vanilla)
- Deployment: PythonAnywhere (or any WSGI-compatible server)
- Authentication: Django’s authentication framework with custom user model

---

## Installation and Setup

### Prerequisites

- Python 3.10+ installed
- MongoDB running locally or accessible remotely
- Git (optional, for cloning)

### Steps

1. **Clone the repo or upload files**

   ```bash
   git clone https://github.com/yourusername/happyfamily.git
   cd happyfamily
   ```

2. **Create and activate virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MongoDB connection**

   Edit `core/mongo.py` to update the MongoDB URI if needed:

   ```python
   client = MongoClient("mongodb://localhost:27017")
   db = client.event_scheduler
   students_col = db.students
   users_col = db.users
   ```

5. **Apply Django migrations**

   Although MongoDB is used for data, Django user model and auth might need migrations:

   ```bash
   python manage.py migrate
   ```

6. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```bash
   python manage.py runserver
   ```

8. **Access the app**

   Open browser at [http://localhost:8000](http://localhost:8000)

---

## Usage

- Log in with your admin credentials.
- Navigate between “Tolibalar” (Students) and “Ustozalar” (Users) from the navbar (admin only).
- Use the filter form to search students by grade and group.
- Add new students or users using the forms.
- Edit student/user records inline by clicking “Edit” and save changes.
- Delete records with confirmation prompts.

---

## Deployment

The app can be deployed on PythonAnywhere or any WSGI-compatible platform:

- Upload your project files.
- Create virtual environment and install requirements.
- Set up environment variables and `ALLOWED_HOSTS`.
- Configure WSGI file pointing to Django settings.
- Collect static files with `python manage.py collectstatic`.
- Reload web app and test live.

---

## Folder Structure

```
happyfamily/
│
├── core/               # Django app: models, views, templates, static files
│   ├── templates/core/
│   ├── static/core/
│   ├── mongo.py        # MongoDB client setup
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── happyfamily/        # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## Contributing

Contributions welcome! Please fork the repo and open a pull request with clear descriptions.

---

## License

MIT License

---

## Contact

For questions or support, contact [abdulkhak8tursunov@gmail.com].
