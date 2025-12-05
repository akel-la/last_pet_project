from django.urls import path, include
from rest_framework import routers

from . import views

# Роутеры - для автоматической генерации маршрутов.
router = routers.SimpleRouter()
router.register(r'answers', views.AnswersViewSet)

urlpatterns = [
    path("", include(router.urls))
    #path("answers/", views.AnswersViewSet.as_view({"get":"list"}), name="get-answer"),
    #path("answers/<int:pk>/", views.AnswerViewSet.as_view({"retrieve":""}))
]