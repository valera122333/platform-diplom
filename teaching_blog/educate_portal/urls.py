from django.urls import path
from .import views

app_name = 'educate_portal'
urlpatterns = [
    path('', views.StandardListView.as_view(), name='standard_list'),
    path('<slug:slug>/', views.SubjectListView.as_view(), name='subject_list'),
    path('<str:standard>/<slug:slug>/',
         views.LessonListView.as_view(), name='lesson_list'),
    path('<str:standard>/<str:slug>/create/',
         views.LessonCreateView.as_view(), name='lesson_create'),
    path('<str:standard>/<str:subject>/<slug:slug>/',
         views.LessonDetailView.as_view(), name='lesson_detail'),
    path('<str:standard>/<str:subject>/<slug:slug>/update/',
         views.LessonUpdateView.as_view(), name='lesson_update'),
    path('<str:standard>/<str:subject>/<slug:slug>/delete/',
         views.LessonDeleteView.as_view(), name='lesson_delete'),

    # фишки
    path('profile', views.profile, name='profile'),

    path('contact', views.contact, name='contact'),

    path('notes', views.notes, name='notes'),
    path('delete_note/<int:pk>',
         views.delete_note, name='delete-note'),
    path('notes_detail/<int:pk>',
         views.NotesDetailView.as_view(), name="notes-detail"),
    path('homework', views.homework, name='homework'),
    path('update_homework/<int:pk>',
         views.update_homework, name="update-homework"),
    path('delete_homework/<int:pk>',
         views.delete_homework, name="delete-homework"),

    path('todo', views.todo, name='todo'),
    path('update_todo/<int:pk>',
         views.update_todo, name="update-todo"),
    path('delete_todo/<int:pk>',
         views.delete_todo, name="delete-todo"),
    path('books', views.books, name='books'),

    path('wikipedia', views.wiki, name='wiki'),

    path('home_poll', views.home_poll, name='home_poll'),
    path('create_poll', views.create_poll, name='create_poll'),
    path('vote/<poll_id>', views.vote_poll, name='vote_poll'),
    path('results/<poll_id>', views.results_poll, name='results_poll'),

]
