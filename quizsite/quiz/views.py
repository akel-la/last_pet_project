from django.shortcuts import render
from django.views.generic import CreateView
from .models import *
from .forms import *

def tests_views(request):
    return render(request, "quiz/answer_form.html", {})

class QuestionsCreateView(CreateView):
    model = Questions
    fields = ["text"]
    template_name = "quiz/question_form.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем дополнительные данные в словарь, связанный с шаблоном:
        additional_data = {
            "draft" : Status.DRAFT.label,
            "published": Status.PUBLISHED.label,
            "false_count": Questions.false_answers_count,
            "true_count": Questions.true_answers_count,
        }
        context.update(additional_data)
        return context
    def get_success_url(self):
        return self.request.path
class AnswersCreateView(CreateView):
    model = Answers
    fields = "__all__"
    template_name = "quiz/answer_form.html"
    def get_success_url(self):
        return self.request.path


class QuizesCreateView(CreateView):
    model = Quizes
    form_class = QuizForm
    #fields = "__all__"
    template_name = "quiz/quiz_form.html"
    def get_success_url(self):
        # При отправке формы пользователь остается на той же странице.
        return self.request.path
