from django.shortcuts import render
import requests
from courses.models import Topic, Question
from .models import QuizResult

def quiz_home(request):
    topics = Topic.objects.all()
    return render(request, 'quiz_home.html', {'topics': topics})

def api_test(request):

    url = "https://opentdb.com/api.php?amount=5&category=18&type=multiple"

    response = requests.get(url)

    data = response.json()
    questions = data['results']

    return render(request, 'api_test.html', {
        'questions': questions
    })

def topic_quiz(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
   
    if topic.name == "Online Quiz":

        url = "https://opentdb.com/api.php?amount=5&type=multiple"

        response = requests.get(url)

        data = response.json()

        questions = data['results']
        request.session['api_questions'] = questions

        if request.method == "POST":
            questions = request.session.get(
                'api_questions',
                []
            )

            score = 0

            for i, question in enumerate(questions, start=1):

                selected_answer = request.POST.get(
                    f'question_{i}'
                )

                if selected_answer == question['correct_answer']:
                    score += 1
            if request.user.is_authenticated:

                QuizResult.objects.create(
                    user=request.user,
                    topic=topic,
                    score=score,
                    total_questions=len(questions)
                )
            return render(request, 'result.html', {
                'score': score,
                'total_questions': len(questions)
            })

        return render(request, 'online_quiz.html', {
            'questions': questions
        })
    questions = Question.objects.filter(
    topic=topic
).order_by('?')[:10]

    if request.method == "POST":

        score = 0

        for question in questions:

            selected_answer = request.POST.get(
                f'question_{question.id}'
            )

            if selected_answer == question.correct_answer:
                score += 1

        total_questions = questions.count()
        if request.user.is_authenticated:

            QuizResult.objects.create(
            user=request.user,
            topic=topic,
            score=score,
            total_questions=total_questions
        )

        return render(request, 'result.html', {
            'score': score,
            'total_questions': total_questions
        })

    return render(request, 'topic_quiz.html', {
        'topic': topic,
        'questions': questions
    })