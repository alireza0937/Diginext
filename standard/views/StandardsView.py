from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from standard.functions import create_standards, catch_standards
from user.models import Company


class StandardsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            velocity_range = request.data.get("velocity")
            acceleration_range = request.data.get("acceleration")
            in_tehran = request.data.get("tehran")

            minimum_acceleration, maximum_acceleration = acceleration_range.split('-')
            minimum_velocity, maximum_velocity = velocity_range.split('-')
            user = request.user
            user_company = Company.objects.filter(user_id=user.pk).first()

            create_standards(user=user,
                             company=user_company,
                             min_velocity=minimum_velocity,
                             max_velocity=maximum_velocity,
                             min_acc=minimum_acceleration,
                             max_acc=maximum_acceleration,
                             in_tehran=in_tehran)
            catch_standards(user, minimum_acceleration, maximum_acceleration, minimum_velocity, maximum_velocity,
                            in_tehran)
            return Response({"message": "data save successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid or incomplete data provided"}, status=status.HTTP_400_BAD_REQUEST)
