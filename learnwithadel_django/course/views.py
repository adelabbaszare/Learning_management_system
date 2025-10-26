from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Course, Lesson
from .serializers import CourseListSerializer, CourseDetailListSerializer, LessonListSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def get_courses(request):
    courses = Course.objects.all()
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    course_serializer = CourseDetailListSerializer(course)
    lesson_serializer = LessonListSerializer(course.lessons.all(), many=True)

    data = {
        'course': course_serializer.data,
        'lesson': lesson_serializer.data
    }

    return Response(serializer.data)

