from django.urls import path
from.views import RegisterView,LoginView,UserView,VerifyEmailView

urlpatterns =[
    path('register/',RegisterView.as_view()),
    path('verify-email/<uid>/<token>',VerifyEmailView.as_view()),
    path('login/',LoginView.as_view()),
    path('me/',UserView.as_view()),
]