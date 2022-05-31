from django.contrib import admin
from educate_portal.models import Standard, Subject, Lesson, Comment, Reply, Notes, Homework, Todo, Contact, Poll
from .models import Question, Answer, Result, Quiz

# Register your models here.


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Quiz)
admin.site.register(Result)

admin.site.register(Poll)
admin.site.register(Standard)
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(Comment)
admin.site.register(Reply)

admin.site.register(Contact)

admin.site.register(Notes)
admin.site.register(Homework)
admin.site.register(Todo)
