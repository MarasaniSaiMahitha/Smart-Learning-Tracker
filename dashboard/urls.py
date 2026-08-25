from django.urls import path
from .views import dashboard_home, quiz_history, leaderboard, certificate

urlpatterns = [
    path('', dashboard_home, name='dashboard'),
    path('history/', quiz_history, name='quiz_history'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('certificate/',certificate,name='certificate'),
]