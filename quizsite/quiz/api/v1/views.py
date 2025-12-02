from rest_framework import viewsets

from .serializers import AnswerSerializer
from ...models import *

class AnswersViewSet(viewsets.ModelViewSet):
    queryset = Answers.objects.all()
    serializer_class = AnswerSerializer

