from django.shortcuts import render
from quizzes.models import QuizResult
from django.db.models import Sum
from django.contrib.auth.models import User
import random
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@login_required(login_url='login')
def certificate(request):
    from courses.models import Topic

    topic = Topic.objects.first()

    return render(
        request,
        'certificate.html',
        {
            'topic': topic
        }
    )

@login_required(login_url='login')
def leaderboard(request):

    users = User.objects.all()

    leaderboard_data = []

    for user in users:

        total_score = QuizResult.objects.filter(
            user=user
        ).aggregate(
            Sum('score')
        )['score__sum'] or 0

        leaderboard_data.append({
            'username': user.username,
            'total_score': total_score
        })

    leaderboard_data.sort(
        key=lambda x: x['total_score'],
        reverse=True
    )

    return render(
        request,
        'leaderboard.html',
        {
            'leaderboard': leaderboard_data
        }
    )

@login_required(login_url='login')
def quiz_history(request):

    results = QuizResult.objects.filter(
        user=request.user
    ).order_by('-date_taken')

    return render(
        request,
        'quiz_history.html',
        {
            'results': results
        }
    )

@login_required(login_url='login')
def dashboard_home(request):
    
    results = QuizResult.objects.filter(
        user=request.user
    ).order_by('-date_taken')

    total_quizzes = results.count()

    topic_percentages = {}

    # Latest score per topic
    for result in results:

        if result.topic.name not in topic_percentages:

            percentage = round(
                (result.score / result.total_questions) * 100
            )

            topic_percentages[result.topic.name] = percentage

    weak_topic = None
    suggestion = None

    if topic_percentages:

        weak_topic = min(
            topic_percentages,
            key=topic_percentages.get
        )

        if weak_topic == "Python":
            suggestion = (
                "Practice Python OOPs and Functions"
            )

        elif weak_topic == "Django":
            suggestion = (
                "Practice Django Models and Views"
            )

        elif weak_topic == "SQL":
            suggestion = (
                "Practice SQL Joins and Queries"
            )

        elif weak_topic == "HTML":
            suggestion = (
                "Practice Forms and Semantic Tags"
            )

        elif weak_topic == "CSS":
            suggestion = (
                "Practice Flexbox and Grid"
            )

        elif weak_topic == "Online Quiz":
            suggestion = (
                "Improve General Computer Knowledge"
            )

    print(topic_percentages)

    return render(
        request,
        'dashboard.html',
        {
            'results': results,
            'total_quizzes': total_quizzes,
            'weak_topic': weak_topic,
            'suggestion': suggestion,
            'topic_percentages': topic_percentages
        }
    )
