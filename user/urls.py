from django.urls import path
from . import views
urlpatterns = [
    path('first-step-registration/', views.FirstStepRegistration.as_view(), name='first-step-registration-page'),
    path('second-step-registration/', views.SecondStepRegistration.as_view(), name='second-step-registration-page'),
    path('third-step-registration/', views.ThirdStepRegistration.as_view(), name='third-step-registration-page'),
    path('state/', views.State.as_view(), name='state-page'),

]