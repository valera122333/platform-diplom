from django.contrib import admin
from educate_portal.models import Standard, Subject, Lesson, Comment, Reply, Notes, Homework, Todo, Contact

# Register your models here.


admin.site.register(Standard)
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(Comment)
admin.site.register(Reply)

admin.site.register(Contact)

admin.site.register(Notes)
admin.site.register(Homework)
admin.site.register(Todo)
