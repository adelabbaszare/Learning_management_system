from django.contrib import admin
from .models import Category, Course, Lesson, Comment, Quiz

class LessonCommentInline(admin.TabularInline):
    model = Comment
    raw_id_fields = ['lesson']


class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'status', 'lesson_type']
    list_filter = ['status', 'lesson_type']
    search_fields = ['title', 'short_description', 'long_description']
    inlines = [LessonCommentInline]


class QuizAdmin(admin.ModelAdmin):

    list_display = ('question', 'get_lesson_title', 'get_course_title', 'answer', 'op1', 'op2', 'op3')

    search_fields = ('question', 'answer')

    list_filter = ('lesson__course__title', 'lesson__title')

    def get_lesson_title(self, obj):
        return obj.lesson.title
    get_lesson_title.short_description = 'Lesson' 
    

    def get_course_title(self, obj):
        return obj.lesson.course.title
    get_course_title.short_description = 'Course' 


# --- ModelAdmin برای Comment ---

class CommentAdmin(admin.ModelAdmin):

    list_display = ('name', 'content_snippet', 'get_created_by_username', 'get_lesson_title', 'get_course_title', 'created_at')

    search_fields = ('name', 'content', 'created_by__username')
    
    list_filter = ('course__title', 'lesson__title', 'created_at')
    
    ordering = ('-created_at',)


    def content_snippet(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_snippet.short_description = 'Content'
    
 
    def get_created_by_username(self, obj):
        return obj.created_by.username
    get_created_by_username.short_description = 'Commenter' 


    def get_lesson_title(self, obj):
        return obj.lesson.title
    get_lesson_title.short_description = 'Lesson' 
    

    def get_course_title(self, obj):
        return obj.course.title
    get_course_title.short_description = 'Course'


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Quiz, QuizAdmin)