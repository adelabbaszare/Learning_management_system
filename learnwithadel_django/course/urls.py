from django.urls import path

from course import views

urlpatterns = [
    path('', views.get_courses, name='course-list'),

    path('get_frontpage_courses/', views.get_frontpage_courses, name='course-list-on-frontpage'),

    path('get_categories/', views.get_categories, name='categories-list'),
    
    # comments endpoint (matches frontend)
    path('<slug:course_slug>/lessons/<slug:lesson_slug>/comments/', views.add_comment, name='course-lesson-comments'),


    path('<slug:course_slug>/lessons/<slug:lesson_slug>/comments/get-comments', views.get_comments),
    
    # course detail (must come after comments)
    path('<slug:slug>/', views.get_course, name='course-detail'),
]   

