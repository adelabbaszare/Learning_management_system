from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from .models import Course, Lesson, Comment, Category
from .serializers import CourseListSerializer, CourseDetailListSerializer, LessonListSerializer, CommentsSerializer, CategorySerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_courses(request):
    category_id = request.GET.get('category_id', '')
    courses = Course.objects.all()

    if category_id:
        courses = courses.filter(categories__in=[int(category_id)])

    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_frontpage_courses(request):
    courses = Course.objects.all()[0:3]
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

    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_comments(request, course_slug, lesson_slug):
    lesson = Lesson.objects.get(slug=lesson_slug)
    serializer = CommentsSerializer(lesson.comments.all(), many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, course_slug, lesson_slug):
    data = request.data
    name = data.get('name')
    content = data.get('content')

    # validation
    if not name or not content:
        return Response({'detail': 'name and content are required.'},
                        status=status.HTTP_400_BAD_REQUEST)

    # get course and lesson (lesson must belong to course)
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)

    # create comment (created_by from authenticated user)
    user = request.user if request.user.is_authenticated else None

    comment = Comment.objects.create(
        course=course,
        lesson=lesson,
        name=name,
        content=content,
        created_by=user
    )

    serializer = CommentsSerializer(comment)

    return Response(serializer.data, status=status.HTTP_201_CREATED)