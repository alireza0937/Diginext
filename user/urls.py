from django.urls import path
from user.views.FirstStepRegistrationView import FirstStepRegistrationAPIView
from user.views.SecondStepRegistrationView import SecondStepRegistrationAPIView
from user.views.StateView import StateAPIView
from user.views.ThirdStepRegistrationView import ThirdStepRegistrationAPIView

urlpatterns = [
    path('', FirstStepRegistrationAPIView.as_view(), name='first-step-registration-page'),
    path('verify-token/', SecondStepRegistrationAPIView.as_view(), name='second-step-registration-page'),
    path('verify-otp/', ThirdStepRegistrationAPIView.as_view(), name='third-step-registration-page'),
    path('state/', StateAPIView.as_view(), name='state-page'),

]
