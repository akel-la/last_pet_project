from django.core.exceptions import ValidationError
from django.db import models

class Status(models.IntegerChoices):
    """
    PUBLISHED - опубликован, имеет все необходимое для работы (перевод в
    состояние PUBLISHED - автоматический запуск проверок корректности данных).
    DRAFT - черновик, т.е. не опубликован.
    """
    DRAFT = False, "Черновик"
    PUBLISHED = True, "Опубликовано"

class Questions(models.Model):
    """Вопрос. На один вопрос - 3 неправильных ответа и один правильный."""
    false_answers_count = 3
    true_answers_count = 1
    status = models.BooleanField(verbose_name="Статус",
                                 choices=Status.choices, default=Status.DRAFT)
    text = models.TextField(verbose_name="Текст вопроса",
                            max_length=250, blank=False, null=False, unique=True)

    def _validation_status_field(self):
        """Проверка того, что при публикации вопроса связанные с ним ответы находятся
        в корректном состоянии."""
        if self.status == Status.PUBLISHED:
            connect_answers = self.answers_set.all()
            amount = len(connect_answers.filter(correct_or_wrong=Answers.CorrectOrWrong.WRONG))
            if amount != Questions.false_answers_count:
                raise ValidationError(
                    message="Неправильное количество связанных с вопросом неправильных ответов. Должно быть %(expected)s, текущее: %(current)s",
                    code='invalid amount connected answers',
                    params={
                        'expected': Questions.false_answers_count,
                        'current': amount,
                    }
                )
            amount = len(connect_answers.filter(correct_or_wrong=Answers.CorrectOrWrong.CORRECT))
            if amount != Questions.true_answers_count:
                raise ValidationError(
                    message="Неправильное количество связанных с вопросом ответов. Должно быть: %(expected)s, текущее: %(current)s",
                    code='invalid amount connected answers',
                    params={
                        'expected': Questions.true_answers_count,
                        'current': amount,
                    }
                )

    def save(self, *args, **kwargs):
        # По умолчанию в save не вызывается full_clean -
        # разрабы Джанго сделали это для оптимизации.
        # full_clean() вызывает clean.
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        self._validation_status_field()
        super().clean()

    # Метод __str__ - для удобного отображения экземпляров класса в django shell.
    # self.get_status_display() - показать значение категориального поля status.
    def __str__(self):
        return f"{self.text} ({self.get_status_display()})"


class Answers(models.Model):
    """Ответы - связанны с таблицей вопросов, многие ответы к одному вопросу."""
    # Класс с вариантами значения поля - поместить прямо перед полем в таблице.
    class CorrectOrWrong(models.IntegerChoices):
        WRONG = False, "Неверный"
        CORRECT = True, "Верный"
    # Верный ли ответ?
    correct_or_wrong = models.BooleanField(verbose_name="Верный ли ответ?",
                                           choices=CorrectOrWrong.choices,
                                           default=CorrectOrWrong.WRONG)
    text = models.TextField(verbose_name="Текст ответа",
                            max_length=150, blank=False, null=False)
    # [1] on_delete=models.CASCADE - при удалении вопроса удаляются и все
    # соответствующие ответы.
    # [2] Django автоматически добавляет суффикс "_id" для полей с внешним ключом.
    # [3] Поле related_name - позволяет обращаться из экземпляров Question
    # к экземплярам Answers через question.answers.all().
    question = models.ForeignKey(Questions, verbose_name="Ответ",
                                 on_delete=models.CASCADE, default=None,
                                 related_name='answers_set')
# Уже не нужен, если есть related_name?
#    def get_related_question(self):
#        """Получить связанный с вопросом ответ"""
#        return self.question.text
    def __str__(self):
        return f"{self.text}({self.correct_or_wrong})"

class Quizes(models.Model):
    """Викторина - коллекция (не упорядоченная) вопросов.
    Викторины и вопросы - связь вида 'Многие ко Многим'.
    Если викторина находится в состоянии 'Опубликовано', то
    все вопросы, которые не находятся в аналогичном состоянии,
    не публикуются."""

    name = models.CharField(verbose_name="Имя викторины",
                            max_length=100, blank=False, null=False, unique=True)
    questions = models.ManyToManyField(Questions, verbose_name="Вопросы",
                                       related_name='quizes')
    published = models.BooleanField(verbose_name="Статус",
                                 choices=Status.choices, default=Status.DRAFT)
    def __str__(self):
        return f"{self.name}:{self.questions}:{self.published}"

# ЗАМЕТКИ:

# [1] Есть 2 способа сделать поле с выбором из нескольких вариантов - кортеж внутри
# класса (устаревший способ) и класс models.TextChoices
# или models.IntegerChoices внутри класса модели (современный способ).

