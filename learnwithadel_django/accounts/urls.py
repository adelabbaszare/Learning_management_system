from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 1. ثبت نام
    path('register/', views.RegisterView.as_view(), name='register'),

    # 2. لاگین (دریافت توکن اکسس و رفرش)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # 3. رفرش کردن توکن (وقتی اکسس توکن منقضی شد)
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 4. دریافت اطلاعات کاربری که لاگین کرده (برای هدر و فرم کامنت)
    path('me/', views.UserMeView.as_view(), name='user_me'),

    # 5. پروفایل عمومی کاربران (مثلاً: /api/account/profile/ali_reza/)
    path('profile/<str:username>/', views.PublicUserProfileView.as_view(), name='public_profile'),
]