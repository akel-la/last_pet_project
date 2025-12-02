from django.urls import path
from . import views

app_name = "quiz"

urlpatterns = [
    path("send-question/", views.QuestionsCreateView.as_view(), name="send question"),
    path("send-answer/", views.AnswersCreateView.as_view(), name="send answer"),
    path("send-quiz/", views.QuizesCreateView.as_view(), name="send quiz"),
]