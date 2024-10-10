from django.urls import path
from .views.tests import *

app_name = "tests"

urlpatterns = [
    path('', TestController.as_view(), name="create-test"),
    path('/student', create_student, name='create-student'),
    path('/<int:test_id>/assign', assign_test, name='assign-test'),
    path('/<int:test_id>/answers', TestAnswersView.as_view(), name='assign-answers'),
]
