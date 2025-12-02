from django import forms

from .models import Quizes

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quizes
        fields = "__all__"
        # Чтобы можно было через виджет выбрать
        # несколько воросов для викторины:
        widgets = {
            "questions": forms.CheckboxSelectMultiple()
        }

