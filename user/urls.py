from django.urls import path
from . import views
urlpatterns = [
    path('', views.FirstStepRegistration.as_view(), name='first-step-registration-page'),
    path('verify-token/', views.SecondStepRegistration.as_view(), name='second-step-registration-page'),
    path('verify-otp/', views.ThirdStepRegistration.as_view(), name='third-step-registration-page'),
    path('state/', views.State.as_view(), name='state-page'),

]
