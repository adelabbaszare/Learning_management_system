from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Course
from .serializers import CourseListSerializer, CourseDetailListSerializer

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
    serializer = CourseDetailListSerializer(course)
    return Response(serializer.data)
