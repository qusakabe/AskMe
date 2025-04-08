from django.core.management.base import BaseCommand
from app.models import Tag, Answer, Question, QuestionLike, AnswerLike, Profile
from django.contrib.auth.models import User
from faker import Faker
from tqdm import tqdm
import random
from django.db import transaction

fake = Faker()

class Command(BaseCommand):
    help = 'This command will fill the database'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The ratio')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        BATCH_SIZE = 10000

        users, profiles = [], []
        exciting_names = []
        for _ in tqdm(range(ratio), desc='Генерация пользователей'):
            correct_generation = False
            while not correct_generation:
                name = fake.user_name()
                if name not in exciting_names:
                    user = User(
                        username=name,
                        email=f'{name}@mail.ru',
                        password=fake.password()
                    )
                    profile = Profile(user=user, avatar=None)
                    users.append(user)
                    profiles.append(profile)
                    exciting_names.append(name)
                    correct_generation = True

        User.objects.bulk_create(users)
        Profile.objects.bulk_create(profiles)


        tags = []
        exciting_tags = set()
        for _ in tqdm(range(ratio), desc="Генерация тегов"):
            correct_generation = False
            while not correct_generation:
                name = " ".join(fake.words(2))
                if name not in exciting_tags:
                    tag = Tag(name=name)
                    tags.append(tag)
                    exciting_tags.add(name)
                    correct_generation = True

        Tag.objects.bulk_create(tags)

        questions = []

        for _ in tqdm(range(ratio*10), desc="Генерация вопросов"):
            question = Question(
                title=fake.sentence(),
                description=fake.paragraph(),
                author=random.choice(users),
            )
            questions.append(question)
        questions = Question.objects.bulk_create(questions)

        for i in tqdm(range(len(questions)), desc="Добавление тегов к вопросам"):
            questions[i].tags.set(random.sample(tags, 3))


        answers = []
        for _ in tqdm(range(ratio*100), desc="Генерация ответов"):
            answer = Answer(
                text = fake.paragraph(),
                author = random.choice(users),
                question = random.choice(questions),
            )
            answers.append(answer)

        for i in tqdm(range(0, len(answers), BATCH_SIZE), desc="Запись ответов в базу"):
            with transaction.atomic():
                Answer.objects.bulk_create(answers[i:i + BATCH_SIZE], batch_size=BATCH_SIZE)

        question_likes = []
        exciting_question_likes = set()
        for _ in tqdm(range(ratio*100), "Генерация лайков на вопросы"):
            correct_generation = False

            while not correct_generation:
                question = random.choice(questions)
                user = random.choice(users)
                like_info = (question.id, user.id)

                if not (like_info in exciting_question_likes):
                    like = QuestionLike(question=question, user=user, is_dislike=random.choice(['True', 'False']))
                    question_likes.append(like)
                    exciting_question_likes.add(like_info)
                    correct_generation = True

        for i in tqdm(range(0, len(question_likes), BATCH_SIZE), desc="Запись лайков на  вопросы в БД"):
            with transaction.atomic():
                QuestionLike.objects.bulk_create(question_likes[i:i + BATCH_SIZE])


        answer_likes = []
        exciting_answer_likes = set()
        for _ in tqdm(range(ratio * 100), "Генерация лайков на ответы"):
            correct_generation = False

            while not correct_generation:
                answer = random.choice(answers)
                user = random.choice(users)
                like_info = (answer.id, user.id)

                if not (like_info in exciting_answer_likes):
                    like = AnswerLike(answer=answer, user=user, is_dislike=random.choice(['True', 'False']))
                    answer_likes.append(like)
                    exciting_answer_likes.add(like_info)
                    correct_generation = True

        for i in tqdm(range(0, len(answer_likes), BATCH_SIZE), desc="Запись лайков на ответы в БД"):
            AnswerLike.objects.bulk_create(answer_likes[i:i + BATCH_SIZE])
