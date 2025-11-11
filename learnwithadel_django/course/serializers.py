# course/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Course, Lesson, Comment, Category, Quiz

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')


class CourseListSerializer(serializers.ModelSerializer):
    get_image = serializers.CharField(read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'short_description', 'get_image')


class CourseDetailListSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(many=False, read_only=True)
    get_image = serializers.CharField(read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'short_description', 'long_description', 'created_by', 'get_image')


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'slug', 'lesson_type', 'short_description', 'long_description', 'youtube_id')


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'name', 'content', 'created_at')


class QuizSerializer(serializers.ModelSerializer):
    # فقط readonly؛ حذف source چون نام فیلد برابر source بود و باعث AssertionError می‌شد
    lesson_id = serializers.IntegerField(read_only=True)

    options = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ('id', 'lesson_id', 'question', 'answer', 'options')

    def get_options(self, obj):
        options_list = [obj.op1, obj.op2, obj.op3]
        return [opt for opt in options_list if opt]
