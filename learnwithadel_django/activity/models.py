from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from course.models import Course, Lesson

class Activity(models.Model):
    STARTED = 'started'
    DONE = 'done'

    STATUS_CHOICES = (
        (STARTED, 'Started'),
        (DONE,'done')
    )

    course = models.ForeignKey(Course, related_name='activities', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='activities', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STARTED)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='activities', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)