from django.urls import path
from app_users import views


# app_name = 'app_users'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profileEd/', views.profile_editor, name='profile_editor'),
    path('contacts/', views.contacts, name='contacts'),




    path('contacts/<int:pk>',
         views.delete_contact, name="delete-contact"),
    path('quizes/', views.QuizListView.as_view(), name='main-view'),
    path('quizes/<pk>/', views.quiz_view, name='quiz-view'),
    path('quizes/<pk>/save/', views.save_quiz_view, name='save-view'),
    path('quizes/<pk>/data/', views.quiz_data_view, name='quiz-data-view'),

]
