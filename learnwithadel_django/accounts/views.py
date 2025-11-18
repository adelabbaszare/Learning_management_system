from django.shortcuts import render

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

# 1. ویو برای ثبت نام کاربران جدید
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

# 2. ویو بسیار مهم برای دریافت اطلاعات کاربر لاگین شده (Me)
# این ویو توسط Vue.js صدا زده می‌شود تا اطلاعات کاربر (عکس، نام) را بگیرد
class UserMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # سریالایزر اطلاعات کاربری که الان توکن دارد (request.user) را برمی‌گرداند
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        # برای آپدیت کردن پروفایل (مثلاً تغییر بیو یا عکس)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 3. ویو برای دیدن پروفایل عمومی دیگران 
class PublicUserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'username' # یا id، بسته به اینکه در url چه چیزی می‌فرستید
