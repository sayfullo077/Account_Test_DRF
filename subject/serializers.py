from rest_framework import serializers

from account.serializers import UserSerializer
from common.serializers import MediaURlSerializer
from subject.models import (
    Category,
    Step,
    StepFile,
    Subject,
    TestAnswer,
    TestQuestion,
    UserStep,
    UserSubject,
    UserTestResult,
    UserTotalTestResult,
)


class StepSerializer(serializers.ModelSerializer):
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = Step

        fields = ["id", "order", "percentage"]

    def get_percentage(self, obj):
        return 0


class UserStepSerializer(serializers.ModelSerializer):
    step = StepSerializer()

    class Meta:
        model = UserStep
        fields = ["step", "finished", "finished_at"]


class SubjectSerializer(serializers.ModelSerializer):
    image = MediaURlSerializer()

    class Meta:
        model = Subject
        fields = ["id", "name", "image"]


class SubjectDetailSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)

    class Meta:
        model = Subject
        fields = ("id", "name", "category", "steps")


class UserSubjectSerializer(serializers.ModelSerializer):
    subject = SubjectDetailSerializer()

    class Meta:
        model = UserSubject
        fields = ["id", "subject", "total_test_ball", "started_time", "started"]


class CategorySerializer(serializers.ModelSerializer):
    bg_image = MediaURlSerializer(read_only=True)
    icon = MediaURlSerializer(read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "click_count",
            "bg_image",
            "icon",
        ]


class StepFilesSerializer(serializers.ModelSerializer):
    file = MediaURlSerializer()

    class Meta:
        model = StepFile
        fields = ["id", "title", "file"]


class StepDetailSerializer(serializers.ModelSerializer):
    step_files = StepFilesSerializer(many=True)

    class Meta:
        model = Step
        fields = ["id", "order", "title", "description", "step_files"]


class StartStepTestSerializer(serializers.Serializer):
    step_id = serializers.IntegerField(required=True)


class TestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAnswer
        fields = ("id", "answer")


class StepTestQuestionTestSerializer(serializers.ModelSerializer):
    test_answers = TestAnswerSerializer(many=True)

    class Meta:
        model = TestQuestion
        fields = ("id", "question_type", "question", "test_answers")


class FinishTestQuestionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(required=True)
    answer_ids = serializers.ListField(child=serializers.IntegerField())


class StepTestFinishSerializer(serializers.Serializer):
    result_id = serializers.IntegerField(required=True)
    questions = serializers.ListField(child=FinishTestQuestionSerializer())


class UserTestResultSerializer(serializers.ModelSerializer):
    test_question = serializers.StringRelatedField()
    test_answers = TestAnswerSerializer(many=True)

    class Meta:
        model = UserTestResult
        fields = ["id", "test_question", "test_answers"]


class UserTotalTestResultSerializer(serializers.ModelSerializer):
    user_test_results = UserTestResultSerializer(many=True)

    class Meta:
        model = UserTotalTestResult
        fields = [
            "id",
            "step_test",
            "user",
            "ball",
            "correct_answers",
            "user_test_results",
            "finished",
            "percentage",
        ]
        read_only_fields = ["id", "user", "step_test"]


class UserTestsResultIDSerializer(serializers.Serializer):
    result_id = serializers.IntegerField(required=True)


class UserTestResultForSubmitSerializer(serializers.Serializer):
    result_id = serializers.IntegerField()
    test_question = serializers.IntegerField()
    test_answers = serializers.ListField(child=serializers.IntegerField())
