from django.contrib import admin
from .models import Activity


class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'get_course_title',
        'get_lesson_title',
        'status',
        'get_created_by_username',
        'created_at',
    )
    
    search_fields = (
        'course__title',
        'lesson__title',
        'created_by__username',
    )
    
    list_filter = (
        'status',
        'course',
        'lesson',
        'created_by',
        'created_at',
    )
    ordering = ('-created_at',)

    def get_course_title(self, obj):
        return obj.course.title
    get_course_title.short_description = 'Course' 

    def get_lesson_title(self, obj):
        return obj.lesson.title
    get_lesson_title.short_description = 'Lesson' 

    def get_created_by_username(self, obj):
        return obj.created_by.username
    get_created_by_username.short_description = 'User' 


admin.site.register(Activity, ActivityAdmin)