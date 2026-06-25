from django.urls import path
from .views import quiz_home, topic_quiz, api_test

urlpatterns = [
    path('', quiz_home, name='quiz_home'),
    path('topic/<int:topic_id>/', topic_quiz, name='topic_quiz'),
    path('api-test/', api_test, name='api_test'),
]