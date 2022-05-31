from django.shortcuts import render, redirect
from app_users.forms import UserForm, UserProfileInfoForm, ProfileForm, ProfileForm2
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from educate_portal.models import Standard
from django.contrib import messages

from educate_portal.models import Contact
from .models import UserProfileInfo
from educate_portal.models import Question, Quiz, Answer, Result


from django.views.generic import ListView
from django.http import JsonResponse


class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'


def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizes/quiz.html', {'obj': quiz})


def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


def save_quiz_view(request, pk):
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append(
                    {str(q): {'Правильный ответ': correct_answer, 'Ваш ответ': a_selected}})
            else:
                results.append({str(q): 'Не ответили'})

        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("user_login")
        else:
            return HttpResponse("Пожалуйста используйте корректный логин и пароль")
            # return HttpResponseRedirect(reverse('register'))

    else:
        return render(request, 'app_users/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save(request.FILES)

            registered = True

            user = user_form.cleaned_data.get('username')
            messages.success(request, 'Аккаунт с именем ' +
                             user + ' успешно создан')
            return redirect('user_login')

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'app_users/registration.html',
                  {'registered': registered,
                   'user_form': user_form,
                   'profile_form': profile_form})


class HomeView(TemplateView):
    template_name = 'app_users/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        standards = Standard.objects.all()
        teachers = UserProfileInfo.objects.filter(user_type='teacher')
        context['standards'] = standards
        context['teachers'] = teachers
        return context


def profile_editor(request):
    form = ProfileForm(instance=request.user.profile)
    user = request.user.id
    profile = UserProfileInfo.objects.get(user__id=user)

    user_form = ProfileForm2(instance=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        user_form = ProfileForm2(request.POST, request.FILES)
        if form.is_valid() and user_form.is_valid():
            profile.bio = form.cleaned_data.get('bio')
            # profile.first_name = user_form.cleaned_data.get('first_name')

            # profile.email = user_form.cleaned_data.get('email')
            profile_pic = request.POST.get('profile_pic')
            if profile_pic is None:
                profile.profile_pic = form.cleaned_data.get('profile_pic')

            profile.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('profile_editor')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')

    context = {
        'user_form': user_form,
        'form': form,
    }
    return render(request, 'dashboard/profile_editor.html', context)


@login_required
def contacts(request):

    zayzvka = Contact.objects.all().filter(contact_info=request.user)

    return render(request,
                  'dashboard/contacts.html',
                  {'zayzvka': zayzvka})


def delete_contact(request, pk=None):
    Contact.objects.get(id=pk).delete()
    messages.success(
        request, f'Заявка успешно удалена пользователем!{request.user.username} !')
    return redirect('contacts')
