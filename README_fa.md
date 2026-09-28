# سیستم مدیریت یادگیری (LMS)

یک سامانه مدیریت یادگیری Full-Stack که با **Django REST API** در سمت Backend و **Vue 3** در سمت Frontend پیاده‌سازی شده است. این پروژه امکاناتی مانند مدیریت کاربران، دوره‌ها، دسته‌بندی‌ها، درس‌ها، آزمون‌ها، دیدگاه‌ها و پیگیری پیشرفت یادگیری را فراهم می‌کند.

## فهرست مطالب

- [معرفی](#معرفی)
- [معماری](#معماری)
- [امکانات](#امکانات)
- [ساختار پروژه](#ساختار-پروژه)
- [Backend](#backend)
- [Frontend](#frontend)
- [API](#api)
- [نصب و راه‌اندازی](#نصب-و-راهاندازی)
- [اجرای پروژه](#اجرای-پروژه)
- [روند استفاده](#روند-استفاده)
- [تنظیمات](#تنظیمات)
- [نکات توسعه](#نکات-توسعه)
- [نکات استقرار Production](#نکات-استقرار-production)

## معرفی

این پروژه یک LMS تحت وب برای انتشار و مصرف محتوای آموزشی ساختاریافته است. Backend یک REST API ارائه می‌کند و Frontend مبتنی بر Vue برای مصرف این API طراحی شده است. محتوای آموزشی در قالب دسته‌بندی، دوره، درس و آزمون سازمان‌دهی می‌شود و کاربران احراز هویت‌شده می‌توانند پروفایل خود را مدیریت کنند، برای درس‌ها دیدگاه ثبت کنند و وضعیت یادگیری خود را پیگیری کنند.

تنظیمات فعلی پروژه بیشتر برای محیط توسعه طراحی شده‌اند؛ از جمله SQLite، فعال بودن `DEBUG`، محدود بودن Hostها به localhost و استفاده از آدرس localhost برای ارتباط Frontend و Backend.

## معماری

```text
+---------------------+       HTTP / JSON        +-------------------------+
|                     |  <------------------->   |                         |
|   Vue 3 Frontend    |                         |   Django REST API       |
|                     |                         |                         |
| - Vue Router        |                         | - Accounts              |
| - Vuex              |                         | - Courses               |
| - Axios             |                         | - Lessons               |
| - Bulma             |                         | - Quizzes               |
| - CKEditor 5        |                         | - Comments              |
|                     |                         | - Activity Tracking     |
+---------------------+                         +------------+------------+
                                                               |
                                                               v
                                                       +---------------+
                                                       | SQLite / Media |
                                                       +---------------+
```

## امکانات

### کاربران و احراز هویت

- مدل سفارشی `User` در Django.
- تصویر پروفایل، بیوگرافی و مشخصه `is_instructor`.
- ثبت‌نام کاربران.
- ورود با JWT و دریافت Access/Refresh Token.
- Endpoint مربوط به `/me/` برای دریافت و ویرایش اطلاعات کاربر فعلی.
- پروفایل عمومی کاربران بر اساس username.
- مدیریت کاربران از طریق Django Admin.

### مدیریت دوره‌ها

- دسته‌بندی دوره‌ها با slug یکتا و توضیحات.
- دوره شامل عنوان، slug، توضیحات کوتاه و کامل، تصویر، سازنده، دسته‌بندی و وضعیت انتشار است.
- وضعیت دوره‌ها: `draft`، `in_review` و `published`.
- ایجاد دوره توسط کاربر احراز هویت‌شده.
- تولید خودکار slug برای دوره و درس.
- فهرست عمومی دوره‌های منتشرشده.
- فیلتر دوره‌ها بر اساس دسته‌بندی.
- دریافت دوره‌های صفحه اصلی.
- دریافت دوره‌های یک مدرس/سازنده.

### درس و محتوای آموزشی

- هر درس متعلق به یک دوره است.
- وضعیت درس: `draft` و `published`.
- انواع درس: مقاله، آزمون و ویدئو.
- پشتیبانی از YouTube Video ID.
- محتوای Rich Text با CKEditor.
- پشتیبانی پیکربندی‌شده از Code Snippet، MathJax، تصویر، Embed، جدول و ابزارهای قالب‌بندی.

### آزمون

- هر درس می‌تواند چندین Quiz داشته باشد.
- هر Quiz شامل سؤال، پاسخ و سه گزینه است.
- دریافت Quizهای یک درس از طریق API اختصاصی.

### دیدگاه‌ها

- کاربران احراز هویت‌شده می‌توانند برای درس‌ها Comment ثبت کنند.
- دریافت Commentهای یک درس برای کاربران عمومی امکان‌پذیر است.
- هر Comment به Course، Lesson و User مرتبط است و زمان ایجاد را نگه می‌دارد.

### پیگیری پیشرفت یادگیری

- ثبت شروع مطالعه یک درس.
- نمایش دوره‌هایی که کاربر در آن‌ها درس شروع‌شده دارد.
- علامت‌گذاری درس به‌عنوان تکمیل‌شده (`done`).
- ثبت Activity بر اساس کاربر، دوره و درس.

## ساختار پروژه

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

> در بخش‌هایی از Backend فایل‌های تولیدشده Python مانند `__pycache__` و `.pyc` نیز در Repository وجود دارند. این فایل‌ها برای اجرای عادی پروژه لازم نیستند و بهتر است با `.gitignore` از نسخه‌گذاری خارج شوند.

## Backend

Backend در پوشه `learnwithadel_django/` قرار دارد.

### Django Apps

| App | مسئولیت |
| --- | --- |
| `accounts` | کاربران سفارشی، ثبت‌نام و APIهای پروفایل |
| `course` | دسته‌بندی، دوره، درس، آزمون و Comment |
| `activity` | پیگیری شروع و پایان درس‌ها |

پروژه از Django REST Framework، Djoser، CORS Headers، احراز هویت Token، Simple JWT و CKEditor/CKEditor uploader استفاده می‌کند.

### مدل داده

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

Frontend در پوشه `learnwithadel_vue/` قرار دارد و از موارد زیر استفاده می‌کند:

- Vue 3
- Vue Router 4
- Vuex 4
- Axios
- Bulma
- Bulma Toast
- Font Awesome
- CKEditor 5
- Sass

دستورات تعریف‌شده در `package.json`:

```bash
npm run serve
npm run build
```

تنظیم فعلی Axios از آدرس زیر برای API استفاده می‌کند:

```text
http://localhost:8000/api/v1/
```

در صورت تغییر آدرس Backend باید این مقدار در Frontend نیز تغییر کند.

## API

### احراز هویت و کاربران

Base path: `/api/v1/accounts/`

| Method | Endpoint | کاربرد | احراز هویت |
| --- | --- | --- | --- |
| `POST` | `/register/` | ثبت‌نام | عمومی |
| `POST` | `/login/` | دریافت JWT | عمومی |
| `POST` | `/login/refresh/` | Refresh Token | با Refresh Token |
| `GET` | `/me/` | اطلاعات کاربر فعلی | الزامی |
| `PATCH` | `/me/` | ویرایش پروفایل | الزامی |
| `GET` | `/profile/<username>/` | پروفایل عمومی | عمومی |

همچنین Endpointهای Djoser در مسیر `/api/v1/` فعال هستند.

### دوره‌ها

Base path: `/api/v1/courses/`

| Method | Endpoint | کاربرد | احراز هویت |
| --- | --- | --- | --- |
| `GET` | `/` | فهرست دوره‌های منتشرشده | عمومی |
| `GET` | `/get_frontpage_courses/` | دوره‌های صفحه اصلی | عمومی |
| `GET` | `/get_categories/` | فهرست دسته‌بندی‌ها | عمومی |
| `GET` | `/get_author_courses/<user_id>/` | دوره‌های منتشرشده یک سازنده | عمومی |
| `POST` | `/create/` | ایجاد دوره و درس‌های اولیه | الزامی |
| `GET` | `/<slug>/` | جزئیات دوره و درس‌ها | عمومی |
| `GET` | `/<course_slug>/lessons/<lesson_slug>/get-quiz/` | دریافت آزمون درس | عمومی |
| `GET` | `/<course_slug>/lessons/<lesson_slug>/comments/get-comments/` | دریافت Commentها | عمومی |
| `POST` | `/<course_slug>/lessons/<lesson_slug>/comments/` | ثبت Comment | الزامی |

فهرست دوره‌ها پارامتر `category_id` را نیز پشتیبانی می‌کند:

```text
GET /api/v1/courses/?category_id=2
```

### Activity

Base path: `/api/v1/activities/`

| Method | Endpoint | کاربرد | احراز هویت |
| --- | --- | --- | --- |
| `GET` | `/get_active_courses/` | دوره‌های دارای درس شروع‌شده | الزامی |
| `POST` | `/track_started/<course_slug>/lessons/<lesson_slug>/` | شروع یک درس | الزامی |
| `POST` | `/mark_as_done/<course_slug>/lessons/<lesson_slug>/` | تکمیل یک درس | الزامی |

### Admin و Media

- پنل مدیریت: `/admin/`
- مسیرهای CKEditor و Upload نیز فعال هستند.
- سرو فایل‌های Media در حالت `DEBUG=True` برای توسعه فعال است.

## نصب و راه‌اندازی

### پیش‌نیازها

محیط پیشنهادی توسعه:

- Python 3.10+
- Node.js 18+ و npm
- Git

در حال حاضر Repository فایل `requirements.txt` یا فایل Lock برای وابستگی‌های Python ندارد؛ بنابراین وابستگی‌های Backend باید به‌صورت دستی نصب شوند.

### 1. Clone

```bash
git clone https://github.com/adelabbaszare/Learning_management_system.git
cd Learning_management_system
```

### 2. راه‌اندازی Django

در Windows CMD:

```cmd
cd learnwithadel_django
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install Django==5.2.7 djangorestframework django-cors-headers djoser django-ckeditor Pillow djangorestframework-simplejwt
```

در macOS/Linux:

```bash
cd learnwithadel_django
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install Django==5.2.7 djangorestframework django-cors-headers djoser django-ckeditor Pillow djangorestframework-simplejwt
```

اجرای Migrationها:

```bash
python manage.py migrate
```

ساخت کاربر مدیر:

```bash
python manage.py createsuperuser
```

اجرای Backend:

```bash
python manage.py runserver
```

API در حالت پیش‌فرض در آدرس زیر قابل دسترسی خواهد بود:

```text
http://127.0.0.1:8000/
```

### 3. راه‌اندازی Vue

در یک Terminal جدید:

```bash
cd learnwithadel_vue
npm install
npm run serve
```

Vue CLI آدرس اجرای Frontend را در Terminal نمایش می‌دهد؛ معمولاً `http://localhost:8080/` است.

### 4. اجرای هم‌زمان

```text
Terminal 1 → Django API → http://127.0.0.1:8000/
Terminal 2 → Vue SPA    → http://localhost:8080/
```

در تنظیمات فعلی Django، مقدار `CORS_ALLOWED_ORIGINS` شامل `http://localhost:8081` است، در حالی که Vue CLI معمولاً روی پورت `8080` اجرا می‌شود. در صورت اجرای Frontend روی پورت دیگر، مقدار CORS را متناسب با Origin واقعی Frontend تنظیم کنید.

## روند استفاده

### مدیر / مدرس

1. مدیریت کاربران از طریق Django Admin.
2. تعیین کاربر به‌عنوان Instructor در صورت نیاز.
3. ایجاد Categoryها.
4. ورود به سیستم.
5. ایجاد Course و Lesson.
6. تنظیم وضعیت انتشار.
7. انتشار Course.

### یادگیرنده

1. ثبت‌نام.
2. ورود و دریافت Token.
3. مشاهده Courseها و Categoryها.
4. ورود به یک Course و Lesson.
5. شروع درس برای ایجاد Activity.
6. تکمیل درس.
7. شرکت در Quizهای موجود.
8. ثبت و مشاهده Comment.
9. ویرایش پروفایل.

## تنظیمات

برخی تنظیمات مهم فعلی:

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

Frontend نیز فعلاً از این API Base URL استفاده می‌کند:

```text
http://localhost:8000/api/v1/
```

قبل از Production باید این مقادیر به Configuration مبتنی بر Environment منتقل شوند.

## نکات توسعه

- پروژه از Custom User Model یعنی `accounts.User` استفاده می‌کند.
- هنگام ایجاد Course، slug دوره و درس‌ها به‌صورت خودکار ساخته می‌شود.
- Endpointهای عمومی Course فقط دوره‌های `published` را برمی‌گردانند.
- هنگام ایجاد Course، Lessonهای اولیه با وضعیت `draft` ساخته می‌شوند.
- CKEditor برای Rich Text، Upload، Code Snippet، MathJax، Embed، Image و Table پیکربندی شده است.
- SQLite برای توسعه مناسب است؛ برای Production بهتر است PostgreSQL یا DB مناسب دیگری استفاده شود.

## نکات استقرار Production

این Repository در وضعیت فعلی برای Development تنظیم شده است. پیش از Production حداقل موارد زیر باید انجام شوند:

1. انتقال `SECRET_KEY` به Environment Variable و تعویض کلید توسعه موجود.
2. قرار دادن `DEBUG = False`.
3. تنظیم `ALLOWED_HOSTS`، CORS و CSRF برای دامنه واقعی.
4. فعال‌سازی HTTPS و Cookieهای امن.
5. جایگزینی SQLite با دیتابیس Production مانند PostgreSQL.
6. تنظیم Storage پایدار برای تصاویر و فایل‌های Upload شده.
7. ایجاد `requirements.txt` یا فایل Lock برای وابستگی‌های Python.
8. حذف `__pycache__` و `.pyc` از Git و افزودن قوانین مناسب `.gitignore`.
9. افزودن تست خودکار برای Authentication، Permission، Course، Comment، Quiz و Activity.
10. بازبینی مجوزهای ایجاد و انتشار Course و نقش Instructor.
11. اجرای Django deployment checks و استفاده از WSGI/ASGI server و Reverse Proxy مناسب.

## License

در Repository فعلی License متن‌باز مشخصی ثبت نشده است. بنابراین تا زمان افزودن License، نباید فرض شود که کد اجازه استفاده یا بازنشر آزاد دارد.

## مستندات مرتبط

- [Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Vue](https://vuejs.org/)
- [Bulma](https://bulma.io/)
