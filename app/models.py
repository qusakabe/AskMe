from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class TagManager(models.Manager):
    def get_top(self, limit=5):
        return self.annotate(questions_count=Count('questions')).order_by('-questions_count')[:limit]

class AnswerManager(models.Manager):
    def get_by_question(self,question):
        return self.filter(question=question).order_by('-is_correct','-rating')


class QuestionManager(models.Manager):
    def get_top(self):
        return self.order_by('-rating').prefetch_related('tags')

    def get_new(self):
        return self.order_by('-created_at').prefetch_related('tags')

    def get_by_tag(self,tag_id):
        return self.filter(tags__id=tag_id).order_by('-rating').prefetch_related('tags')


class Tag(models.Model):
    name = models.CharField(verbose_name="Название", max_length=50, unique=True)
    created_at = models.DateTimeField(verbose_name="Создан",auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Изменён", auto_now=True)

    objects = TagManager()

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Question(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=100)
    description = models.CharField(verbose_name="Описание", max_length=3000)
    created_at = models.DateTimeField(verbose_name="Создан",auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Изменён", auto_now=True)
    rating = models.FloatField(default=0)
    answer_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField('Tag',verbose_name="Теги", related_name='questions', blank=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name='questions', db_index=True)

    def update_rating(self):
        self.rating = self.likes.filter(is_dislike=False).count() - self.likes.filter(is_dislike=True).count()
        self.save(update_fields=['rating'])

    def update_answer_count(self):
        self.answer_count = self.answers.count()
        self.save(update_fields=['answer_count'])

    objects = QuestionManager()

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    text = models.CharField(verbose_name="Текст", max_length=3000)
    created_at = models.DateTimeField(verbose_name="Создан",auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Изменён",auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name='answers', db_index=True)
    is_correct = models.BooleanField(default=False)
    rating = models.FloatField(default=0)
    question = models.ForeignKey(Question,on_delete=models.CASCADE,db_index=True, related_name='answers',)

    def update_rating(self):
        self.rating = self.likes.filter(is_dislike=False).count() - self.likes.filter(is_dislike=True).count()
        self.save(update_fields=['rating'])

    objects = AnswerManager()

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class QuestionLike(models.Model):
    question = models.ForeignKey('Question',verbose_name="Вопрос",on_delete=models.CASCADE,db_index=True, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name='question_likes', db_index=True)
    created_at = models.DateTimeField(verbose_name="Поставлен", auto_now_add=True)
    is_dislike = models.BooleanField(verbose_name="Дизлайк",default=False,db_index=True)

    class Meta:
        verbose_name = "Лайк Вопроса"
        verbose_name_plural = "Лайки Вопроса"
        unique_together = ('question', 'user')


class AnswerLike(models.Model):
    answer = models.ForeignKey('Answer', verbose_name="Ответ", on_delete=models.CASCADE, db_index=True, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name='answer_likes', db_index=True)
    created_at = models.DateTimeField(verbose_name="Поставлен", auto_now_add=True)
    is_dislike = models.BooleanField(verbose_name="Дизлайк", default=False, db_index=True)

    class Meta:
        verbose_name = "Лайк Ответа"
        verbose_name_plural = "Лайки Ответа"
        unique_together = ('answer', 'user')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Автор", related_name='profile', db_index=True)
    avatar = models.ImageField(verbose_name="Аватар", upload_to='profiles/avatars/')

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
