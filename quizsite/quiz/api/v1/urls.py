from django.urls import path

from . import views

# модель/тип_запроса/
# если на конце s - то множество записей модели.
urlpatterns = [
    path("answers/get/", views.AnswersViewSet.as_view({'get':'list'}), name="get-answer"),
]