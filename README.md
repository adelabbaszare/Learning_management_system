# Learning Management System (LMS)

![Learning Management System (LMS)](https://github.com/adelabbaszare/Learning_management_system/blob/main/Learning_management_system.png)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-42b883?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Bulma](https://img.shields.io/badge/Bulma-1.x-00d1b2?logo=bulma&logoColor=white)](https://bulma.io/)
[![Django](https://img.shields.io/badge/Django-5.x-092e20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-REST_API-a30000?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Axios](https://img.shields.io/badge/Axios-1.x-5A29E4?logo=axios&logoColor=white)](https://axios-http.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)

> **Documentation:** [Read the Persian documentation (README_fa.md)](README_fa.md)

A full-stack learning management system built around a Django REST API and a Vue 3 single-page application. The project provides course publishing, lessons, quizzes, comments, user accounts, instructor profiles, and learner activity tracking.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Backend](#backend)
- [Frontend](#frontend)
- [API](#api)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Typical Workflow](#typical-workflow)
- [Configuration](#configuration)
- [Development Notes](#development-notes)
- [Production Considerations](#production-considerations)

## Overview

This project is a web-based LMS for publishing and consuming structured educational content. The backend exposes REST endpoints consumed by the Vue frontend. Course content is organized into categories, courses, lessons, and quizzes, while authenticated users can maintain profiles, comment on lessons, and track learning progress.

The current repository is primarily a development-oriented application. The Django settings explicitly use SQLite, `DEBUG = True`, localhost hosts, and a localhost frontend/API configuration.

## Architecture

```text
+---------------------+        HTTP/JSON        +-------------------------+
|                     |  <------------------->  |                         |
|   Vue 3 Frontend    |                         |   Django REST API       |
|                     |                         |                         |
| - Vue Router        |                         | - Accounts              |
| - Vuex              |                         | - Courses               |
| - Axios             |                         | - Lessons               |
| - Bulma             |                         | - Quizzes               |
| - CKEditor 5        |                         | - Comments              |
|                     |                         | - Activity tracking     |
+---------------------+                         +------------+------------+
                                                               |
                                                               v
                                                       +---------------+
                                                       | SQLite / Media |
                                                       +---------------+
```

## Features

### User and authentication

- Custom Django `User` model.
- User profile image, biography, and instructor flag.
- User registration.
- JWT login and refresh endpoints.
- Authenticated `/me/` endpoint for reading/updating the current profile.
- Public user profiles by username.
- Django admin integration for user management.

### Course management

- Course categories with unique slugs and descriptions.
- Courses with titles, slugs, short/long descriptions, images, authors, categories, and publication status.
- Course states: `draft`, `in_review`, and `published`.
- Authenticated course creation.
- Automatic slug generation for courses and lessons.
- Public listing of published courses.
- Filtering courses by category.
- Front-page course listing.
- Public author/course pages.

### Lessons and educational content

- Lessons belong to courses.
- Lesson states: `draft` and `published`.
- Lesson types: article, quiz, and video.
- YouTube video ID support.
- Rich-text lesson content through CKEditor.
- Code snippets, MathJax, images, embeds, tables, and other CKEditor capabilities configured on the backend.

### Quizzes

- Multiple quiz records can belong to a lesson.
- Each quiz stores a question, answer, and three option fields.
- Quiz data can be retrieved through a lesson-specific API endpoint.

### Comments

- Authenticated users can add comments to lessons.
- Public users can retrieve lesson comments.
- Comments are linked to both a course and lesson and record their author and creation time.

### Learning activity

- Authenticated users can mark lessons as started.
- Started lessons are available through an active-course endpoint.
- Lessons can be marked as completed (`done`).
- Activity records are associated with the user, course, and lesson.

## Project Structure

```text
Learning_management_system/
├── learnwithadel_django/
│   ├── accounts/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── activity/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── course/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── learnwithadel_django/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   └── manage.py
│
├── learnwithadel_vue/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── router/
│   │   ├── store/
│   │   └── views/
│   ├── package.json
│   └── vue.config.js
│
├── README.md
└── README_fa.md
```

> The repository also contains generated Python cache files in parts of the Django tree. These are not required for normal development and should generally be excluded with `.gitignore`.

## Backend

The Django project is located in `learnwithadel_django/`.

### Main Django apps

| App | Responsibility |
| --- | --- |
| `accounts` | Custom users, registration, authentication-related profile APIs |
| `course` | Categories, courses, lessons, quizzes, and comments |
| `activity` | Started/completed lesson tracking |

The project also integrates Django REST Framework, Djoser, CORS headers, token authentication, Simple JWT views, and CKEditor/CKEditor uploader.

### Data model

The main relationships are:

```text
User
 ├── creates → Course
 ├── writes → Comment
 └── owns → Activity

Category ── many-to-many ── Course

Course
 ├── has many → Lesson
 └── has many → Comment

Lesson
 ├── has many → Quiz
 ├── has many → Comment
 └── has many → Activity
```

## Frontend

The Vue application is located in `learnwithadel_vue/` and uses:

- Vue 3
- Vue Router 4
- Vuex 4
- Axios
- Bulma
- Bulma Toast
- Font Awesome
- CKEditor 5
- Sass

The frontend package defines the standard development and production build commands:

```bash
npm run serve
npm run build
```

The current Axios configuration points to:

```text
http://localhost:8000/api/v1/
```

If the backend is hosted elsewhere, update the frontend API configuration accordingly.

## API

The backend exposes the following main API groups.

### Authentication and users

Base path: `/api/v1/accounts/`

| Method | Endpoint | Purpose | Auth |
| --- | --- | --- | --- |
| `POST` | `/register/` | Register a user | Public |
| `POST` | `/login/` | Obtain JWT access/refresh tokens | Public |
| `POST` | `/login/refresh/` | Refresh an access token | Public with refresh token |
| `GET` | `/me/` | Get current user | Required |
| `PATCH` | `/me/` | Update current profile | Required |
| `GET` | `/profile/<username>/` | Get a public profile | Public |

Djoser endpoints are also mounted under `/api/v1/`, and the project additionally exposes Djoser token-auth routes.

### Courses

Base path: `/api/v1/courses/`

| Method | Endpoint | Purpose | Auth |
| --- | --- | --- | --- |
| `GET` | `/` | List published courses | Public |
| `GET` | `/get_frontpage_courses/` | Get front-page courses | Public |
| `GET` | `/get_categories/` | List categories | Public |
| `GET` | `/get_author_courses/<user_id>/` | List an author's published courses | Public |
| `POST` | `/create/` | Create a course and initial lessons | Required |
| `GET` | `/<slug>/` | Get course details and lessons | Public |
| `GET` | `/<course_slug>/lessons/<lesson_slug>/get-quiz/` | Get lesson quizzes | Public |
| `GET` | `/<course_slug>/lessons/<lesson_slug>/comments/get-comments/` | Get lesson comments | Public |
| `POST` | `/<course_slug>/lessons/<lesson_slug>/comments/` | Add a lesson comment | Required |

The course list supports a `category_id` query parameter, for example:

```text
GET /api/v1/courses/?category_id=2
```

### Learning activity

Base path: `/api/v1/activities/`

| Method | Endpoint | Purpose | Auth |
| --- | --- | --- | --- |
| `GET` | `/get_active_courses/` | Get courses containing started lessons | Required |
| `POST` | `/track_started/<course_slug>/lessons/<lesson_slug>/` | Mark a lesson as started | Required |
| `POST` | `/mark_as_done/<course_slug>/lessons/<lesson_slug>/` | Mark a lesson as completed | Required |

### Django admin and media

- Admin: `/admin/`
- CKEditor browser/upload endpoints: `/ckeditor/` and related uploader routes.
- Development media serving is enabled while `DEBUG` is true.

## Installation

### Prerequisites

Recommended development environment:

- Python 3.10+
- Node.js 18+ and npm
- Git

The repository does not currently provide a backend `requirements.txt` or other Python dependency lock file, so the backend dependencies need to be installed explicitly.

### 1. Clone the repository

```bash
git clone https://github.com/adelabbaszare/Learning_management_system.git
cd Learning_management_system
```

### 2. Set up the Django backend

On Windows CMD:

```cmd
cd learnwithadel_django
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install Django==5.2.7 djangorestframework django-cors-headers djoser django-ckeditor Pillow djangorestframework-simplejwt
```

On macOS/Linux:

```bash
cd learnwithadel_django
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install Django==5.2.7 djangorestframework django-cors-headers djoser django-ckeditor Pillow djangorestframework-simplejwt
```

Apply migrations:

```bash
python manage.py migrate
```

Create an administrator:

```bash
python manage.py createsuperuser
```

Start the API server:

```bash
python manage.py runserver
```

The API should then be available at:

```text
http://127.0.0.1:8000/
```

### 3. Set up the Vue frontend

Open a second terminal:

```bash
cd learnwithadel_vue
npm install
npm run serve
```

Vue CLI will print the local development URL in the terminal, commonly `http://localhost:8080/`.

### 4. Run both applications

For normal local development, keep both processes running:

```text
Terminal 1 → Django API → http://127.0.0.1:8000/
Terminal 2 → Vue SPA    → http://localhost:8080/
```

The current Django CORS configuration explicitly allows `http://localhost:8081`, while the Vue CLI commonly uses port `8080`. If the frontend is served on a different port, update `CORS_ALLOWED_ORIGINS` in `settings.py` to match the actual frontend origin.

## Typical Workflow

### Administrator/instructor

1. Create or manage users through Django admin.
2. Mark a user as an instructor when appropriate.
3. Create categories.
4. Authenticate through the API/frontend.
5. Create courses with categories and lessons.
6. Review or update course/lesson publication state.
7. Publish the course.

### Learner

1. Register an account.
2. Log in and obtain an access/refresh token.
3. Browse published courses and categories.
4. Open a course and its lessons.
5. Start lessons to create activity records.
6. Complete lessons.
7. Take quizzes where available.
8. Add or read lesson comments.
9. Update the personal profile when needed.

## Configuration

Important development settings currently include:

```python
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
WEBSITE_URL = 'http://127.0.0.1:8000'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

The frontend currently uses:

```text
http://localhost:8000/api/v1/
```

Before deployment, these values should be moved into environment-specific configuration.

## Development Notes

- The project uses a custom user model (`accounts.User`).
- Course and lesson slugs are generated automatically during course creation.
- Public course endpoints only expose courses whose status is `published`.
- Course creation creates lessons as drafts even when a course request contains a publication status.
- CKEditor is configured with upload support, code snippets, MathJax, embeds, images, tables, and text formatting.
- SQLite is suitable for local development; a production deployment should use a production database and persistent media storage.

## Production Considerations

This repository is configured for development rather than production. Before deployment, at minimum:

1. Move `SECRET_KEY` to an environment variable and rotate the exposed development key.
2. Set `DEBUG = False`.
3. Configure production `ALLOWED_HOSTS` and CORS/CSRF origins.
4. Use HTTPS and secure cookies.
5. Replace SQLite with an appropriate production database such as PostgreSQL.
6. Configure persistent media/file storage for uploaded profile and course images and CKEditor files.
7. Add a Python dependency lock/requirements file.
8. Remove generated `__pycache__`/`.pyc` files from version control and add suitable `.gitignore` rules.
9. Add automated tests for authentication, permissions, course creation, comments, quizzes, and activity tracking.
10. Review authorization rules around course creation/publication and instructor capabilities.
11. Run Django's deployment checks and configure a production WSGI/ASGI server and reverse proxy.

## License

No explicit open-source license is currently documented in the repository. Until a license is added, treat the source code as **all rights reserved** and do not assume permission to redistribute or reuse it.

## Related Documentation

- [Django documentation](https://docs.djangoproject.com/)
- [Django REST Framework documentation](https://www.django-rest-framework.org/)
- [Vue documentation](https://vuejs.org/)
- [Bulma documentation](https://bulma.io/)
