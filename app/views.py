from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'question_list.html', {'questions': questions})

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'ask_question.html', {'form': form})

@login_required
def answer_question(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', question_id)
    else:
        form = AnswerForm()
    return render(request, 'answer_question.html', {'form': form, 'question': question})

def question_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    return render(request, 'question_detail.html', {'question': question})

@login_required
def like_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    if request.user not in answer.likes.all():
        answer.likes.add(request.user)
    return redirect('question_detail', answer.question.id)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home page view
        else:
            # Authentication failed
            return render(request, 'registration/login.html', {'error': 'Invalid username or password'})
    return render(request, 'registration/login.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home page view
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
