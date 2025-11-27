from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from .models import Course, Lesson, Comment, Category
from .serializers import CourseListSerializer, CourseDetailListSerializer, LessonListSerializer, CommentsSerializer, CategorySerializer, QuizSerializer, UserSerializer

User = get_user_model()

def generate_unique_slug(model, value, slug_field='slug', queryset=None):
    """
    Generate a unique slug for `model` based on `value`.
    Optional: provide queryset to limit uniqueness scope (e.g. lessons in a course).
    """
    base = slugify(value) or 'item'
    slug = base
    counter = 1
    qs = queryset if queryset is not None else model.objects.all()
    lookup = {slug_field: slug}
    while qs.filter(**lookup).exists():
        slug = f"{base}-{counter}"
        lookup = {slug_field: slug}
        counter += 1
    return slug


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_course(request):
    incoming_status = request.data.get('status')
    # If client sets 'published', force draft first
    title = (request.data.get('title') or '').strip()
    short_description = request.data.get('short_description') or ''
    long_description = request.data.get('long_description') or ''

    # generate a unique slug for the course
    course_slug = generate_unique_slug(Course, title, slug_field='slug')

    course = Course.objects.create(
        title=title,
        slug=course_slug,
        short_description=short_description,
        long_description=long_description,
        status=incoming_status,
        created_by=request.user
    )

    # categories: accept list or empty; be defensive about types
    categories = request.data.get('categories') or []
    # If categories are sent as comma-separated string, try to split
    if isinstance(categories, str):
        categories = [c.strip() for c in categories.split(',') if c.strip()]

    for cat_id in categories:
        try:
            course.categories.add(int(cat_id))
        except (ValueError, TypeError):
            # skip invalid ids
            continue

    course.save()

    # Lessons: create each lesson and generate a stable slug (unique within all lessons)
    lessons = request.data.get('lessons') or []
    if not isinstance(lessons, list):
        # if a single object was posted, try to coerce
        lessons = [lessons]

    for lesson_data in lessons:
        lesson_title = (lesson_data.get('title') or '').strip()
        lesson_short = lesson_data.get('short_description') or ''
        lesson_long = lesson_data.get('long_description') or ''

        # make slug unique within this lesson set (or globally)
        lesson_slug_base = generate_unique_slug(
            Lesson,
            lesson_title or 'lesson',
            slug_field='slug',
            queryset=Lesson.objects.filter(course=course) 
        )

        tmp_lesson = Lesson.objects.create(
            course=course,
            title=lesson_title,
            slug=lesson_slug_base,
            short_description=lesson_short,
            long_description=lesson_long,
            status=Lesson.DRAFT,
        )

    return Response({'course_id': course.id, 'slug': course.slug}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_quiz(request, course_slug, lesson_slug):
    try:
        lesson = Lesson.objects.get(slug=lesson_slug)
    except Lesson.DoesNotExist:
        return Response({"detail": "Lesson not found."}, status=status.HTTP_404_NOT_FOUND)
    
    questions = lesson.quizzes.all() 
    serializer = QuizSerializer(questions, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_courses(request):
    category_id = request.GET.get('category_id', '')
    # prefetch categories reduces DB queries and provides category objects to serializer
    courses = Course.objects.filter(status=Course.PUBLISHED).prefetch_related('categories')

    if category_id:
        courses = courses.filter(categories__in=[int(category_id)])

    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_frontpage_courses(request):
    courses = Course.objects.filter(status=Course.PUBLISHED)[0:4]
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_course(request, slug):
    course = get_object_or_404(Course.objects.filter(status=Course.PUBLISHED), slug=slug)
    lesson_serializer = LessonListSerializer(course.lessons.all(), many=True)

    course_serializer = CourseDetailListSerializer(course)
    course_data = course_serializer.data

    return Response({
        'course': course_data,
        'lesson': lesson_serializer.data
    })


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
    name = request.data.get('name') or request.POST.get('name')
    content = request.data.get('content') or request.POST.get('content')

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


@api_view(['GET'])
@permission_classes([AllowAny])
def get_author_courses(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    courses = user.courses.filter(status=Course.PUBLISHED)

    user_serializer = UserSerializer(user, many=False)
    courses_serializer = CourseListSerializer(courses, many=True)

    return Response({
        'courses': courses_serializer.data,
        'created_by': user_serializer.data
    })