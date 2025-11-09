from django.urls import path
from .import views

urlpatterns = [
    path('get_active_courses/', views.get_activity_courses),
    path('track_started/<slug:course_slug>/lessons/<slug:lesson_slug>/', views.track_started),
]