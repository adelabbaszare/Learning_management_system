from django.contrib import admin
from .models import Category, Course, Lesson, Comment, Quiz
from django.utils.safestring import mark_safe


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'short_description', 'created_at')
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}


class LessonCommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('name', 'content', 'created_by', 'created_at')
    readonly_fields = ('name', 'content', 'created_by', 'created_at')
    can_delete = False


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'status', 'lesson_type', 'quiz_count')
    list_filter = ['status', 'lesson_type', 'course']
    search_fields = ['title', 'short_description', 'long_description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonCommentInline]

    def quiz_count(self, obj):
        return obj.quizzes.count()
    quiz_count.short_description = 'Quizzes'


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_category_list', 'created_by', 'status', 'created_at', 'lesson_count', 'comment_count')
    list_filter = ('status', 'created_by', 'categories')
    search_fields = ('title', 'short_description', 'long_description', 'created_by__username')
    prepopulated_fields = {'slug': ('title',)}
    
    def lesson_count(self, obj):
        return obj.lessons.count()
    lesson_count.short_description = 'Lessons'
    
    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comments'

    def get_category_list(self, obj):
        return ", ".join([c.title for c in obj.categories.all()])
    get_category_list.short_description = 'Categories'


class QuizAdmin(admin.ModelAdmin):
    list_display = ('display_question', 'get_lesson_title', 'get_course_title')
    search_fields = ('question', 'answer')
    list_filter = ('lesson__course__title', 'lesson__title')

    def get_lesson_title(self, obj):
        return obj.lesson.title
    get_lesson_title.short_description = 'Lesson' 
    
    def get_course_title(self, obj):
        return obj.lesson.course.title
    get_course_title.short_description = 'Course' 

    def display_question(self, obj):
        return mark_safe(obj.question)
    
    display_question.short_description = 'Question'
    display_question.allow_tags = True


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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Quiz, QuizAdmin)