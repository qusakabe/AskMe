from audioop import reverse

from django.contrib import auth
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.paginator import PageNotAnInteger, EmptyPage
from app.models import Question, TagManager, Tag, Answer
from django.http import HttpResponseNotFound
from .forms import signupForm, loginForm, settingsForm, questionForm, answerForm
from django.contrib.auth import logout
from django.urls import reverse
from math import ceil


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)

    page_num = request.GET.get('page', 1)

    try:
        page_num = int(page_num) if int(page_num) > 0 else 1
    except (ValueError, TypeError):
        page_num = 1
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page

def get_page_number_for_answer(answers_queryset, target_answer, per_page):
    answer_ids = list(answers_queryset.values_list('id', flat=True))
    try:
        index = answer_ids.index(target_answer.id)
        return ceil((index + 1) / per_page)
    except ValueError:
        return 1

def index(request):
    questions = Question.objects.get_new()
    page = paginate(questions,request)
    tags = Tag.objects.get_top()

    return render(request, 'index.html', context={'page': page, 'questions': questions, 'tags': tags})


def question(request,id):
    try:
        question = Question.objects.get(id=id)
    except Question.DoesNotExist:
        return HttpResponseNotFound()

    answers = Answer.objects.get_by_question(question=question)
    page = paginate(answers,request)
    tags = Tag.objects.get_top()

    form = answerForm()
    if request.method == 'POST':
        form = answerForm(request.POST,user=request.user, question=question)
        if form.is_valid():
            answer = form.save()
            all_answers = Answer.objects.get_by_question(question=question)
            page_number = get_page_number_for_answer(all_answers, answer, per_page=10)
            url = f"{reverse('question', kwargs={'id': question.id})}?page={page_number}#answer-{answer.id}"
            return redirect(url)
    return render(request, 'question.html', context={'page': page, 'answers': answers, 'question': question, 'tags': tags, 'form': form})


def tag(request,id):
    try:
        questions = Question.objects.get_by_tag(id)
    except:
        return HttpResponseNotFound()

    page = paginate(questions,request)
    tag = Tag.objects.get(id=id)
    tags = Tag.objects.get_top()

    return render(request, 'tag.html', context={'page': page, 'questions': questions, 'tag': tag, 'tags': tags})


def ask(request):
    tags = Tag.objects.get_top()
    form = questionForm()
    if request.method == 'POST':
        form = questionForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('question', kwargs={'id': form.instance.id}))
    return render(request, 'ask.html',context={'tags': tags, 'form': form})

def login(request):
    tags = Tag.objects.get_top()
    form = loginForm()
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request,user)
                continue_url = request.GET.get('continue', '/')
                return redirect(continue_url)
            form.add_error('password','Error password or login!')
    return render(request, 'login.html',context={'tags': tags, 'form': form})

def signup(request):
    tags = Tag.objects.get_top()
    form = signupForm()
    if request.method == 'POST':
        form = signupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
    return render(request, 'signup.html', context={'tags':tags,'form': form})

def settings(request):
    tags = Tag.objects.get_top()
    form = settingsForm(
            user=request.user,
            initial={
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
            })
    if request.method == 'POST':
        form = settingsForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
    return render(request,'settings.html', context={'tags':tags,'form': form})

def hot(request):
    questions = Question.objects.get_top()
    page = paginate(questions, request)
    tags = Tag.objects.get_top()

    return render(request, 'hot.html', context={'page': page, 'questions': questions, 'tags': tags})

def logout_view(request):
    logout(request)
    continue_url = request.GET.get('continue', '/')
    return redirect(continue_url)