from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from user.functions import create_user
from user.models import User
from user.registration_classes.first_step import FirstStepRegister
from user.serializers.FirstStepRegistrationSerializer import FirstStepRegistrationSerializer


class FirstStepRegistrationAPIView(APIView):

    @extend_schema(request=FirstStepRegistrationSerializer)
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            serializer = FirstStepRegistrationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"message": "Inserted username or password is not valid."},
                                status=status.HTTP_400_BAD_REQUEST)

            # first_step_instance = FirstStepRegister(username, password)
            # response = first_step_instance.check_user_and_password()
            # return response
            user_exists: User = User.objects.filter(username=username).first()

            if user_exists is None:
                token = create_user(username=username, password=password)
                return Response({"message": "Successfully", "Authentication Token": token.key},
                                status=status.HTTP_200_OK)

            if user_exists.check_password(password):
                user_token = Token.objects.filter(user_id=user_exists.pk).values('key').first()
                return Response({"message": "Already have a token.", "Authentication Token": user_token.get("key")},
                                status=status.HTTP_200_OK)

            return Response({'message': 'Username already exists.'}, status=status.HTTP_409_CONFLICT)
        except:
            return Response({"message": "The entered information is not complete"}, status=status.HTTP_400_BAD_REQUEST)
