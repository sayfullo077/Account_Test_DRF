from django.core.exceptions import ValidationError
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from common.models import Media


class Category(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100, unique=True)
    click_count = models.PositiveIntegerField(verbose_name="Click Count", default=0)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categorys"


class Subject(models.Model):
    name = models.CharField(verbose_name="Name", max_length=200)
    category = models.ForeignKey(
        verbose_name="Category",
        to=Category,
        on_delete=models.CASCADE,
        related_name="subjects",
    )

    def clean(self):
        subject_count = Subject.objects.filter(category=self.category).count()
        if subject_count >= 2:
            raise ValidationError( "Invalid Subject Type")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"


class UserSubject(models.Model):
    subject = models.ForeignKey(
        verbose_name="Subject",
        to=Subject,
        on_delete=models.CASCADE,
        related_name="user_subjects",
    )
    user = models.ForeignKey(
        verbose_name="User", to="account.User", on_delete=models.CASCADE
    )
    total_test_ball = models.PositiveIntegerField(
        verbose_name="Total test ball", default=0
    )
    started_time = models.DateTimeField(auto_now_add=True)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.email} - {self.subject.name}"

    class Meta:
        verbose_name = "User's subject"
        verbose_name_plural = "User's subjects"
        unique_together = "user", "subject"


class Step(models.Model):
    title = models.CharField(verbose_name="Title", max_length=200)
    order = models.PositiveIntegerField(verbose_name="Order")
    subject = models.ForeignKey(
        verbose_name="Subject",
        to=Subject,
        on_delete=models.CASCADE,
        related_name="steps",
    )
    description = CKEditor5Field("Description")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Step"
        verbose_name_plural = "Steps"


class StepFile(models.Model):
    title = models.CharField(verbose_name="Title", max_length=250)
    file = models.ForeignKey(verbose_name="File", to=Media, on_delete=models.CASCADE)
    step = models.ForeignKey(
        verbose_name="Step",
        to=Step,
        on_delete=models.CASCADE,
        related_name="step_files",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Step's file"
        verbose_name_plural = "Step's files"


class StepTest(models.Model):

    class TestTypes(models.TextChoices):
        MIDTERM = "midterm"
        FINAL = "final"

    step = models.OneToOneField(
        verbose_name="Step", to=Step, on_delete=models.CASCADE, related_name="tests"
    )
    ball_for_each_test = models.FloatField(verbose_name="Bal for each question")
    question_count = models.PositiveIntegerField(verbose_name="Question Count")
    test_type = models.CharField(
        verbose_name="Test type", max_length=30, choices=TestTypes.choices
    )
    time_for_test = models.DurationField(verbose_name="Test time limit")

    def __str__(self) -> str:
        return f"{self.pk} - {self.step.title}"

    class Meta:
        verbose_name = "Step's test"
        verbose_name_plural = "Step's tests"


class TestQuestion(models.Model):
    class QuestionLevel(models.TextChoices):
        EASY = "easy"
        MEDIUM = "medium"
        HARD = "hard"

    class QuestionType(models.TextChoices):
        MULTIPLE = "multiple"
        SINGLE = "single"
        ORDERING = "ordering"

    steptest = models.ForeignKey(
        verbose_name="Step test",
        to=StepTest,
        on_delete=models.CASCADE,
        related_name="test_questions",
    )
    question_type = models.CharField(
        verbose_name="Question type", max_length=30, choices=QuestionType.choices
    )
    question = CKEditor5Field("Question", config_name="extends")
    level = models.CharField(
        max_length=10, choices=QuestionLevel.choices, default=QuestionLevel.EASY
    )

    def __str__(self) -> str:
        return f"{self.pk}"

    class Meta:
        verbose_name = "Test's question"
        verbose_name_plural = "Test's questions"


class TestAnswer(models.Model):
    test_quetion = models.ForeignKey(
        verbose_name="Question",
        to=TestQuestion,
        on_delete=models.CASCADE,
        related_name="test_answers",
    )
    answer = CKEditor5Field("Answer", config_name="extends")
    is_correct = models.BooleanField(verbose_name="Is correct")
    order = models.PositiveIntegerField("Order", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.is_correct}"

    class Meta:
        verbose_name = "Test's answer"
        verbose_name_plural = "Test's answers"


class UserTestResult(models.Model):
    total_result = models.ForeignKey(
        "UserTotalTestResult", on_delete=models.CASCADE, related_name="total_results"
    )
    test_question = models.ForeignKey(
        verbose_name="Question", to=TestQuestion, on_delete=models.CASCADE
    )
    test_answers = models.ManyToManyField(TestAnswer)
    user = models.ForeignKey(
        verbose_name="Users", to="account.User", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.pk} - {self.user.username}"

    class Meta:
        verbose_name = "Test result"
        verbose_name_plural = "Test results"


class UserTotalTestResult(models.Model):
    step_test = models.ForeignKey(
        verbose_name="Step test", to=StepTest, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        verbose_name="Users", to="account.User", on_delete=models.CASCADE
    )
    ball = models.FloatField(verbose_name="Ball", null=True, blank=True)
    correct_answers = models.PositiveIntegerField(
        verbose_name="Count of correct answers", null=True, blank=True
    )
    user_test_results = models.ManyToManyField(
        verbose_name="Test Results", to=UserTestResult, related_name="testresults"
    )
    finished = models.BooleanField(default=False)
    percentage = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.user.username}"

    class Meta:
        verbose_name = "Total test result"
        verbose_name_plural = "Total test results"


class UserStep(models.Model):
    user = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="user_steps"
    )
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="user_steps")
    finished = models.BooleanField(default=False)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["user", "step"]
