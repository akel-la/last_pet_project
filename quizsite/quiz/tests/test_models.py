from unittest import TestCase
from django.core.exceptions import ValidationError

from ..models import Quizes, Questions, Answers, Status

class ModelsTests(TestCase):
    # Этот метод выполняется каждый раз перед тестовым методом:
    def setUp(self):
        """setUp - выполняется перед каждым методом теста."""
        # Создаем вопрос:
        self.q = Questions.objects.create(status=Status.DRAFT,
                                          text="Вопрос для проведения автотестов.")
        # Создаем необходимое количество неправильных ответов на вопрос:
        for number in range(1, Questions.false_answers_count + 1):
            Answers.objects.create(correct_or_wrong=Answers.CorrectOrWrong.WRONG,
                                   text=f"{number} неправильный ответ на вопрос {self.q}",
                                   question=self.q)
        # Создаем необходимое количество правильных ответов на вопрос:
        for number in range(1, Questions.true_answers_count + 1):
            Answers.objects.create(correct_or_wrong=Answers.CorrectOrWrong.CORRECT,
                                   text=f"{number} правильный ответ на вопрос {self.q}",
                                   question=self.q)
    def test_publish_with_amount_answers(self):
        """Проверка изменения статуса вопроса с 'Черновик' на 'Опубликовано'
        при корректных условиях."""
        # Меняем статус существующего вопроса, сохраняем и проверяем, изменился ли он:
        self.q.status = Status.PUBLISHED
        self.q.save()
        self.assertEqual(self.q.status, Status.PUBLISHED)
        # Перезагружаем запись из БД, чтобы убедиться, что изменения
        # произошли в самой БД:
        updated_q = Questions.objects.get(pk=self.q.pk)
        self.assertEqual(updated_q.status, Status.PUBLISHED)
    def test_cannot_publish_with_extra_true_answers(self):
        """Проверка изменения статуса вопроса с 'Черновик' на 'Опубликовано'
        при лишнем правильном вопросе."""
        Answers.objects.create(correct_or_wrong=Answers.CorrectOrWrong.CORRECT,
                               text=f"Лишний правильный ответ на вопрос {self.q}",
                               question=self.q)
        self.q.status = Status.PUBLISHED
        # Попытка сохранить изменение должна вызывать ValidationError,
        # так как именно эта ошибка прописана в методе clean модели:
        with self.assertRaises(ValidationError):
            self.q.save()
        updated_q = Questions.objects.get(pk=self.q.pk)
        self.assertEqual(updated_q.status, Status.DRAFT)
    def test_cannot_publish_with_extra_false_answers(self):
        """Проверка изменения статуса вопроса с 'Черновик' на 'Опубликовано'
        при лишнем не правильном вопросе"""
        Answers.objects.create(correct_or_wrong=Answers.CorrectOrWrong.WRONG,
                               text=f"Лишний правильный ответ на вопрос {self.q}",
                               question=self.q)
        self.q.status = Status.PUBLISHED
        # Попытка сохранить изменение должна вызывать ValidationError,
        # так как именно эта ошибка прописана в методе clean модели:
        with self.assertRaises(ValidationError):
            self.q.save()
        updated_q = Questions.objects.get(pk=self.q.pk)
        self.assertEqual(updated_q.status, Status.DRAFT)

# ЗАМЕТКИ:

# [1] Если в setUp присвоить нечто как атрибут self, то это можно
# использовать в методах-тестах.

# [2] Большинство (все?) проверок - это атрибуты self.