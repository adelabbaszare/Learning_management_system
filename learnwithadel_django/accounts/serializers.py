from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='get_image', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'image', 'bio', 'is_instructor',)

        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'image': {'required': False}, # اجازه آپدیت تصویر
            'bio': {'required': False},  # اجازه آپدیت بیو
        }
    
    # متد برای محاسبه image_url
    def get_image_url(self, obj):
        # از متد get_image() که در مدل User تعریف کرده‌اید استفاده می‌کند
        return obj.get_image()

    def create(self, validated_data):
        # منطق ایجاد کاربر جدید (ضروری برای RegisterView)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user