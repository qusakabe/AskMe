from django.core.paginator import Paginator
from django.shortcuts import render
from django.core.paginator import PageNotAnInteger, EmptyPage


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
    #тестовые объекты вопросов
    questions = [
        {"id": i,
         "title": "CMake can't find my Android NDK library file in Flutter project",
         "text": "CMake can't find my Android NDK library file in Flutter project I'm trying to integrate a C++ library with Flutter using FFI. I have a pre-compiled libMesh.so file and want to create a wrapper ...",
         "tags": ['bender','black-jack','bender']}
        for i in range(1, 91)
    ]
    page = paginate(questions,request)
    return render(request, 'index.html', context={'page': page, 'questions': questions})


def question(request):
    answers = [
        {"id": i,
         "text": "CMake can't find my Android NDK library file in Flutter project I'm trying to integrate a C++ library with Flutter using FFI. I have a pre-compiled libMesh.so file and want to create a wrapper ...",
         }
        for i in range(1, 91)
    ]
    page = paginate(answers,request)
    return render(request, 'question.html', context={'page': page, 'answers': answers})

def tag(request,id):
    #тестовые теги
    test_tags = {
        0: "black-jack",
        1: "bender",
        2: "Python",
        3: "C#",
        4: "Go",
        5: "C++",
        6: "HTML",
    }

    tag = test_tags[id]

    #тестовые объекты вопросов (для страницы с вопросами по тегам)
    questions = [
        {"id": i,
         "title": "CMake can't find my Android NDK library file in Flutter project",
         "text": "CMake can't find my Android NDK library file in Flutter project I'm trying to integrate a C++ library with Flutter using FFI. I have a pre-compiled libMesh.so file and want to create a wrapper ...",
         "tags": [tag,'some-tag']}
        for i in range(1, 91)
    ]
    page = paginate(questions,request)
    return render(request, 'tag.html', context={'page': page, 'questions': questions, 'tag': tag})


def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def settings(request):
    return render(request,'settings.html')

def hot(request):
    # тестовые объекты вопросов
    questions = [
        {"id": i,
         "title": "CMake can't find my Android NDK library file in Flutter project",
         "text": "CMake can't find my Android NDK library file in Flutter project I'm trying to integrate a C++ library with Flutter using FFI. I have a pre-compiled libMesh.so file and want to create a wrapper ...",
         "tags": ['hot', 'hot question']}
        for i in range(1, 91)
    ]
    page = paginate(questions, request)
    return render(request, 'hot.html', context={'page': page, 'questions': questions})