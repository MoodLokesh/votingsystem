from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.registration, name='register'),
    path('vote/', views.voting, name='vote'),

    path('register-user/', views.register_user, name='register_user'),
    path('login-user/', views.login_user, name='login_user'),
    path('submit-vote/', views.submit_vote, name='submit_vote'),
    path('results/', views.results, name='results'),

]
