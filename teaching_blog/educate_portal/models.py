from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
import os
from embed_video.fields import EmbedVideoField
# Create your models here.


class Standard(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def save_subject_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.subject_id:
        filename = 'Subject_Pictures/{}.{}'.format(instance.subject_id, ext)
    return os.path.join(upload_to, filename)


class Subject(models.Model):
    subject_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    standard = models.ForeignKey(
        Standard, on_delete=models.CASCADE, related_name='subjects')
    image = models.ImageField(
        upload_to=save_subject_image, blank=True, verbose_name='Subject Image')
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args, **kwargs)


def save_lesson_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.lesson_id:
        filename = 'lesson_files/{}/{}.{}'.format(
            instance.lesson_id, instance.lesson_id, ext)
        if os.path.exists(filename):
            new_name = str(instance.lesson_id) + str('1')
            filename = 'lesson_images/{}/{}.{}'.format(
                instance.lesson_id, new_name, ext)
    return os.path.join(upload_to, filename)


class Lesson(models.Model):
    lesson_id = models.CharField(
        max_length=100, unique=True, verbose_name="id урока")
    Standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=250, verbose_name="Заголовок урока")
    position = models.PositiveSmallIntegerField(verbose_name="Номер урока")
    slug = models.SlugField(null=True, blank=True)

    video = EmbedVideoField(default='', verbose_name="ссылка на видео")

    ppt = models.FileField(upload_to=save_lesson_files,
                           verbose_name="презентации", blank=True)
    Notes = models.FileField(upload_to=save_lesson_files,
                             verbose_name="файл урока", blank=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('educate_portal:lesson_list', kwargs={'slug': self.subject.slug, 'standard': self.Standard.slug})


class Comment(models.Model):
    lesson_name = models.ForeignKey(
        Lesson, null=True, on_delete=models.CASCADE, related_name='comments')
    comm_name = models.CharField(max_length=100, blank=True)
    # reply = models.ForeignKey("Comment", null=True, blank=True, on_delete=models.CASCADE,related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.comm_name = slugify(
            "comment by" + "-" + str(self.author) + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['-date_added']


class Reply(models.Model):
    comment_name = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies')
    reply_body = models.TextField(
        max_length=500, verbose_name='ответ на комментарий')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)


# фишки
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='Заголовок заметки')
    description = models.TextField(verbose_name='Описание заметки')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Записи'
        verbose_name_plural = 'Записи'


class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, verbose_name='Предмет')
    title = models.CharField(max_length=80, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание урока')
    time_lesson = models.DateTimeField(verbose_name='Время на выполнение')
    is_finished = models.BooleanField(default=False, verbose_name='Выполнено')

    def __str__(self):
        return self.title


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=180, verbose_name='Ваша задача')
    is_finished = models.BooleanField(default=False, verbose_name='Выполнено')

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="имя")
    email = models.EmailField(max_length=250, verbose_name="майл")
    phone = models.CharField(max_length=100, verbose_name="телефон")
    subject = models.CharField(max_length=100, verbose_name="сообщение")

    contact_info = models.ForeignKey(User, on_delete=models.CASCADE,
                                     null=True)

    def __str__(self):
        return self.name

    class Meta:

        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"
