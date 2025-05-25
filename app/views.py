from audioop import reverse
from django.contrib import auth
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import PageNotAnInteger, EmptyPage
from app.models import Question, TagManager, Tag, Answer, AnswerLike, QuestionLike
from django.http import HttpResponseNotFound
from .forms import signupForm, loginForm, settingsForm, questionForm, answerForm
from django.contrib.auth import logout
from django.urls import reverse
from math import ceil
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json


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


def annotate_with_user_rate(request, obj_list):
    if request.user.is_authenticated and obj_list:
        user = request.user
        model_type = type(obj_list[0])

        if model_type == Question:
            obj_ids = [obj.id for obj in obj_list]
            user_likes = QuestionLike.objects.filter(user=user, question_id__in=obj_ids)
            like_map = {like.question_id: like for like in user_likes}
            for obj in obj_list:
                obj.user_rate = like_map.get(obj.id)

        elif model_type == Answer:
            obj_ids = [obj.id for obj in obj_list]
            user_likes = AnswerLike.objects.filter(user=user, answer_id__in=obj_ids)
            like_map = {like.answer_id: like for like in user_likes}
            for obj in obj_list:
                obj.user_rate = like_map.get(obj.id)

    return obj_list


def index(request):
    questions = Question.objects.get_new()
    page = paginate(questions, request)
    tags = Tag.objects.get_top()
    annotate_with_user_rate(request, page.object_list)

    return render(request, 'index.html', context={'page': page, 'questions': questions, 'tags': tags})


def question(request, id):
    tags = Tag.objects.get_top()
    question = get_object_or_404(Question, id=id)
    annotate_with_user_rate(request, [question])

    answers = Answer.objects.get_by_question(question)
    page = paginate(answers, request)
    annotate_with_user_rate(request, page.object_list)

    form = answerForm()
    if request.method == 'POST':
        form = answerForm(request.POST, user=request.user, question=question)
        if form.is_valid():
            answer = form.save()
            all_answers = Answer.objects.get_by_question(question=question)
            page_number = get_page_number_for_answer(all_answers, answer, per_page=10)
            url = f"{reverse('question', kwargs={'id': question.id})}?page={page_number}#answer-{answer.id}"
            return redirect(url)
    return render(request, 'question.html',
                  context={'page': page, 'answers': answers, 'question': question, 'tags': tags, 'form': form})


def tag(request, id):
    try:
        questions = Question.objects.get_by_tag(id)
    except:
        return HttpResponseNotFound()

    page = paginate(questions, request)
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
    return render(request, 'ask.html', context={'tags': tags, 'form': form})


def login(request):
    tags = Tag.objects.get_top()
    form = loginForm()
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                continue_url = request.GET.get('continue', '/')
                return redirect(continue_url)
            form.add_error('password', 'Error password or login!')
    return render(request, 'login.html', context={'tags': tags, 'form': form})


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
    return render(request, 'signup.html', context={'tags': tags, 'form': form})


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
    return render(request, 'settings.html', context={'tags': tags, 'form': form})


def hot(request):
    questions = Question.objects.get_top()
    page = paginate(questions, request)
    tags = Tag.objects.get_top()

    return render(request, 'hot.html', context={'page': page, 'questions': questions, 'tags': tags})


def logout_view(request):
    logout(request)
    continue_url = request.GET.get('continue', '/')
    return redirect(continue_url)


@require_POST
@login_required
def toggle_correct(request):
    try:
        data = json.loads(request.body)
        answer_id = data.get('answer_id')
        answer = Answer.objects.get(pk=answer_id)

        # Только автор вопроса может помечать ответы
        if request.user != answer.question.author:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        answer.is_correct = not answer.is_correct
        answer.save(update_fields=['is_correct'])

        return JsonResponse({'status': 'ok', 'is_correct': answer.is_correct})
    except Answer.DoesNotExist:
        return JsonResponse({'error': 'Answer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_POST
def rate_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    data = json.loads(request.body)
    object_type = data.get('type')
    object_id = data.get('id')
    action = data.get('action')

    if object_type == 'question':
        from .models import Question, QuestionLike
        try:
            obj = Question.objects.get(id=object_id)
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question not found'}, status=404)

        like_obj = QuestionLike.objects.filter(user=request.user, question=obj).first()

        if like_obj:
            if (action == 'like' and like_obj.is_dislike is False) or (action == 'dislike' and like_obj.is_dislike is True):
                like_obj.delete()
                status = 'cleared'
            else:
                like_obj.is_dislike = (action == 'dislike')
                like_obj.save(update_fields=['is_dislike'])
                status = 'switched'
        else:
            QuestionLike.objects.create(
                user=request.user, question=obj, is_dislike=(action == 'dislike')
            )
            status = 'liked' if action == 'like' else 'disliked'

        obj.update_rating()
        return JsonResponse({'rating': obj.rating, 'status': status})

    elif object_type == 'answer':
        from .models import Answer, AnswerLike
        try:
            obj = Answer.objects.get(id=object_id)
        except Answer.DoesNotExist:
            return JsonResponse({'error': 'Answer not found'}, status=404)

        like_obj = AnswerLike.objects.filter(user=request.user, answer=obj).first()

        if like_obj:
            if (action == 'like' and like_obj.is_dislike is False) or (action == 'dislike' and like_obj.is_dislike is True):
                like_obj.delete()
                status = 'cleared'
            else:
                like_obj.is_dislike = (action == 'dislike')
                like_obj.save(update_fields=['is_dislike'])
                status = 'switched'
        else:
            AnswerLike.objects.create(
                user=request.user, answer=obj, is_dislike=(action == 'dislike')
            )
            status = 'liked' if action == 'like' else 'disliked'

        obj.update_rating()
        return JsonResponse({'rating': obj.rating, 'status': status})

    return JsonResponse({'error': 'Invalid type'}, status=400)
