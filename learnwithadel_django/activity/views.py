from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Activity
from .serializers import ActivitySerializer

from course.serializers import CourseListSerializer
from course.models import Course, Lesson


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_activity_courses(request):
    courses = []

    for activity in request.user.activities.all():
        if activity.status == activity.STARTED and activity.course not in courses:
            courses.append(activity.course)

    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def track_started(request, course_slug, lesson_slug):
    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug)

    # Check if an activity already exists
    activity = Activity.objects.filter(
        created_by=request.user, 
        course=course, 
        lesson=lesson
        ).first()  # Use `first()` to get one or `None` if no record exists

    if not activity:
        # If no activity exists, create one
        activity = Activity.objects.create(
            created_by=request.user, 
            course=course, 
            lesson=lesson, 
            status=Activity.STARTED
        )
        created = True
    else:
        created = False

    serializer = ActivitySerializer(activity)
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_done(request, course_slug, lesson_slug):
    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug)

    activity = Activity.objects.get(
        created_by=request.user,
        course=course,
        lesson=lesson
    )
    activity.status = Activity.DONE
    activity.save()

    serializer = ActivitySerializer(activity)

    return Response(serializer.data)

