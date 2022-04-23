
from django.db import models
from django.contrib.auth.models import User
import os


def path_and_rename(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]

    if instance.pk:
        filename = 'User_Profile_Pictures/{}.{}'.format(instance.pk, ext)
    return os.path.join(upload_to, filename)


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.CharField(max_length=500, verbose_name="О себе")
    profile_pic = models.ImageField(
        upload_to=path_and_rename, verbose_name="Изображение профиля*", blank=True)
    teacher = 'teacher'
    student = 'student'
    parent = 'parent'
    user_types = [
        (teacher, 'teacher'),
        (student, 'student'),
        (parent, 'parent'),
    ]
    user_type = models.CharField(
        max_length=30, choices=user_types, default=student, verbose_name='Тип студента')

    def __str__(self):
        return self.user.username
