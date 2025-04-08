from django.core.paginator import Paginator
from django.shortcuts import render
from django.core.paginator import PageNotAnInteger, EmptyPage
from app.models import Question, TagManager, Tag, Answer
from django.http import HttpResponseNotFound


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

    return render(request, 'question.html', context={'page': page, 'answers': answers, 'question': question, 'tags': tags})

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
    return render(request, 'ask.html',context={'tags': tags})

def login(request):
    tags = Tag.objects.get_top()
    return render(request, 'login.html',context={'tags': tags})

def signup(request):
    tags = Tag.objects.get_top()
    return render(request, 'signup.html',context={'tags': tags})

def settings(request):
    return render(request,'settings.html')

def hot(request):
    questions = Question.objects.get_top()
    page = paginate(questions, request)
    tags = Tag.objects.get_top()

    return render(request, 'hot.html', context={'page': page, 'questions': questions, 'tags': tags})