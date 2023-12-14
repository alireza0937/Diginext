from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from user.models import User


class FirstStepRegister:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_user_and_password(self):
        existence_result = self._check_user_existence()
        if existence_result is not None:
            return self._check_insert_password_match(user_info=existence_result)
        return self._create_user()

    def _create_user(self):
        new_user = User.objects.create_user(username=self.username, password=self.password)
        token = Token.objects.create(user_id=new_user.pk)
        return Response({"message": "Successfully",
                         "Authentication Token": token.key},
                        status=status.HTTP_200_OK)

    def _check_user_existence(self):
        response = User.objects.get(username=self.username)
        if response is not None:
            return response
        pass

    def _check_insert_password_match(self, user_info):
        if user_info.check_password(self.password):
            user_token = Token.objects.get(user_id=user_info.pk).key
            return Response({"message": "You have already token",
                             "Token": f"{user_token}"}, status=status.HTTP_200_OK)

        return Response({"message": "Username exist.."}, status=status.HTTP_409_CONFLICT)
