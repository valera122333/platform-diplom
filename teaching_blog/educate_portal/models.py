from email.policy import default
from django.utils import timezone
from django.db import models
import random
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

    class Meta:
        verbose_name = 'Предмет обучения'
        verbose_name_plural = 'Предмет обучения'


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

    class Meta:
        verbose_name = 'Категория предмета обучения'
        verbose_name_plural = 'Категория предмета обучения'


def save_lesson_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.lesson_id:
        filename = 'lesson_files/{}/{}.{}'.format(
            ext)
        if os.path.exists(filename):
            new_name = str(instance.name) + str('1')
            filename = 'lesson_images/{}/{}.{}'.format(
                instance.name, new_name, ext)
    return os.path.join(upload_to, filename)


class Lesson(models.Model):

    Standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=250, verbose_name="Заголовок урока")
    description = models.TextField(
        max_length=5000, blank=True, verbose_name="Описание урока")
    description2 = models.TextField(
        max_length=5000, blank=True, verbose_name="Продолжение описания")
    position = models.PositiveSmallIntegerField(verbose_name="Номер урока")
    slug = models.SlugField(
        null=True, blank=True, verbose_name='уникальное поле в адресной строке (eng раскладка)')

    video = EmbedVideoField(default='', verbose_name="ссылка на видео")

    ppt = models.FileField(upload_to=save_lesson_files,
                           verbose_name="презентации", blank=True)
    Notes = models.FileField(upload_to=save_lesson_files,
                             verbose_name="файл урока", blank=True)
    console = models.URLField(
        max_length=250, verbose_name="консоль", default='')

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('educate_portal:lesson_list', kwargs={'slug': self.subject.slug, 'standard': self.Standard.slug})

    class Meta:
        verbose_name = 'Уроки'
        verbose_name_plural = 'Уроки'


class Comment(models.Model):
    lesson_name = models.ForeignKey(
        Lesson, null=True, on_delete=models.CASCADE, related_name='comments')
    comm_name = models.CharField(max_length=100, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.comm_name = (
            "комментарий от" + "-" + str(self.author) + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['-date_added']

    class Meta:
        verbose_name = 'комментарии'
        verbose_name_plural = 'комментарии'


class Reply(models.Model):
    comment_name = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies')
    reply_body = models.TextField(
        max_length=500, verbose_name='ответ на комментарий')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Ответ на комментарий " + str(self.comment_name.comm_name)

    class Meta:
        verbose_name = 'Ответы на комментарии'
        verbose_name_plural = 'Ответы на комментарии'

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

    class Meta:

        verbose_name = "Задания"
        verbose_name_plural = "Задания"


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=180, verbose_name='Ваша задача')
    is_finished = models.BooleanField(default=False, verbose_name='Выполнено')

    def __str__(self):
        return self.title

    class Meta:

        verbose_name = "Планировщик"
        verbose_name_plural = "Планировщик"


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="имя")
    email = models.EmailField(max_length=250, verbose_name="майл")
    phone = models.CharField(max_length=100, verbose_name="телефон")
    subject = models.CharField(max_length=100, verbose_name="сообщение")
    date_posted = models.DateTimeField(
        default=timezone.now, verbose_name="дата обращения")
    answer_contact = models.CharField(
        max_length=100, verbose_name="ответ администратора", default='')
    contact_info = models.ForeignKey(User, on_delete=models.CASCADE,
                                     null=True)

    def __str__(self):
        return self.name

    class Meta:

        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"


class Poll(models.Model):
    question = models.TextField()
    option_one = models.CharField(max_length=30)
    option_two = models.CharField(max_length=30)
    option_three = models.CharField(max_length=30)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)

    def total(self):
        return self.option_one_count + self.option_two_count + self.option_three_count

    def __str__(self):
        return self.question

    class Meta:

        verbose_name = "Опросы"
        verbose_name_plural = "Опросы"


DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)


class Quiz(models.Model):
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    required_score_to_pass = models.IntegerField(
        help_text="required score in %")
    difficluty = models.CharField(max_length=6, choices=DIFF_CHOICES)
    quiz_image = models.ImageField(upload_to='images/quiz_image',
                                   verbose_name='Изображение викторины', blank=False, default='')

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'Викторины'
        verbose_name = "Викторины"


class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answer_set.all()

    class Meta:

        verbose_name = "Вопросы викторины"
        verbose_name_plural = "Вопросы викторины"


class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"

    class Meta:

        verbose_name = "Ответы викторины"
        verbose_name_plural = "Ответы викторины"


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)

    class Meta:

        verbose_name = "Результаты викторины"
        verbose_name_plural = "Результаты викторины"
