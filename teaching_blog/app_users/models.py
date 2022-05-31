
from django.db import models
from django.contrib.auth.models import User
import os


def path_and_rename(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]

    if instance.pk:
        filename = 'User_Profile_Pictures/{}.{}'.format(instance.pk, ext)
    return os.path.join(upload_to, filename)


def upload_profile_image(instance, filename):
    return f"images/users/{instance.user.username}/avatar/{filename}"


class UserProfileInfo(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')

    bio = models.CharField(max_length=500, verbose_name="О себе", blank=True)
    profile_pic = models.ImageField(upload_to=path_and_rename,
                                    default='images/23.webp', verbose_name='Изображение профиля', blank=False)
    teacher = 'teacher'
    student = 'student'

    user_types = [
        (teacher, 'Учитель'),
        (student, 'Студент'),

    ]
    user_type = models.CharField(
        max_length=30, choices=user_types, default=student, verbose_name='Тип пользователя')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Информация о пользователях'
        verbose_name_plural = 'Информация о пользователях'
