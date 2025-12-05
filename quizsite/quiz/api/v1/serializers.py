from rest_framework import serializers

from ...models import Answers, Questions, Quizes

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = "__all__"
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = "__all__"
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizes
        fields = "__all__"
