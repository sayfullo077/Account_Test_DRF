from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryAPIView,
    CategoryListView,
    GetTestResultsView,
    StartStepTestView,
    StartSubjectApi,
    StepDetailAPIView,
    StepTestFinishView,
    SubmitTestView,
    TestQuestionViewSet,
    TestAnswerViewSet,
)

# Initialize the router
router = DefaultRouter()

# Register your ViewSets with the router
router.register(r"question-step-test", TestQuestionViewSet, basename="question-step-test")
router.register(r"answer-step-test", TestAnswerViewSet, basename="answer-step-test")

urlpatterns = [
    path("category/<int:pk>/", CategoryAPIView.as_view(), name="category-subject"),
    path("start-subject/<int:subject_id>/", StartSubjectApi.as_view(), name="start-subject"),
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("steps/<int:pk>/", StepDetailAPIView.as_view(), name="step-detail"),
    path("steps/start-test/", StartStepTestView.as_view(), name="step-start-test"),
    path("subject/get-test/", GetTestResultsView.as_view(), name="get_test"),
    path("step-test/submit/", SubmitTestView.as_view(), name="submit-test"),
    path("finish-step-test/", StepTestFinishView.as_view(), name="finish-step-test"),

    # Include the router's URL patterns
    path("api/", include(router.urls)),
]