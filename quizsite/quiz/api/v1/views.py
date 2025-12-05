from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import *
from ...models import *

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answers.objects.all()
    serializer_class = AnswerSerializer
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        """Обработка ошибки - создание опубликованного
        вопроса с не корректным сосотянием ответов."""
        # Передача в сериализатор входных данных:
        serializer = self.get_serializer(data=request.data)
        # Валидация полученных данных:
        serializer.is_valid(raise_exception=True)
        try:
            # Попытка сохранить объект в базу данных:
            self.perform_create(serializer)
            # Если сохранение успешно - то сохраняются заголовки для ответа:
            headers = self.get_success_headers(serializer.data)
            # Формирование ответа:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValueError as error:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"detail": f"""Неверное значение поля {Questions._meta.get_field("status").verbose_name}: для того, чтобы поле {Questions._meta.get_field("status").verbose_name} имело значение {Status.PUBLISHED.label} нужно, чтобы у вопроса было {Questions.true_answers_count} верных ответов и {Questions.false_answers_count} не верных ответов.""",
                                  "error_type": type(error).__name__,
                                  "message_from_exception": str(error)
                }
            )
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quizes.objects.all()
    serializer_class = QuizSerializer

