from django.urls import path, include
from rest_framework import routers

from . import views

# Роутеры - для автоматической генерации маршрутов.
router = routers.SimpleRouter()
router.register(r'answers', views.AnswerViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'quizes', views.QuizViewSet)

urlpatterns = [
    path("", include(router.urls)),
]