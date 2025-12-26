from django.urls import path
from.views import RegisterView,LoginView,UserView,VerifyEmailView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns =[
    path('register/',RegisterView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/<uid>/<token>/',VerifyEmailView.as_view()),
    path('login/',LoginView.as_view()),
    path('me/',UserView.as_view()),
]