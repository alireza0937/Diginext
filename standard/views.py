from django.http import HttpRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from standard.models import Location
from user.models import Car
from .functions import *


class AccelerationStandardAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest):
        try:
            acceleration_range = request.data.get("acceleration")
            minimum_acceleration, maximum_acceleration = acceleration_range.split('-')
            user = request.user
            existing_standards: Standard = Standard.objects.filter(user_id=request.user.pk).first()
            if existing_standards is None:
                create_standards(user=user, min_acc=minimum_acceleration,
                                 max_acc=maximum_acceleration)
            else:
                update_acceleration_standard(users=existing_standards,
                                             min_acc=minimum_acceleration,
                                             max_acc=maximum_acceleration)
            return Response({"message": "data save successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid acceleration range format"}, status=status.HTTP_400_BAD_REQUEST)


class VelocityStandardAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest):
        try:
            velocity_range = request.data.get("velocity")
            minimum_velocity, maximum_velocity = velocity_range.split('-')
            user = request.user
            existing_standards: Standard = Standard.objects.filter(user_id=request.user.pk).first()
            if existing_standards is None:
                create_standards(user=user, min_velocity=minimum_velocity,
                                 max_velocity=maximum_velocity)
            else:
                update_velocity_standard(users=existing_standards,
                                         min_velocity=minimum_velocity,
                                         max_velocity=maximum_velocity)
            return Response({"message": "data save successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid velocity range format"}, status=status.HTTP_400_BAD_REQUEST)


class IsInTehranAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            in_tehran = request.data.get("tehran")
            existing_standards: Standard = Standard.objects.filter(user_id=request.user.pk).first()
            user = request.user
            if existing_standards is False:
                create_standards(user=user, in_tehran=in_tehran)
            else:
                update_is_tehran_standard(users=user, in_tehran=in_tehran)
            return Response({"message": "data save successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "The entered information is not complete"}, status=status.HTTP_400_BAD_REQUEST)


class LocationAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            latitude = data.get("latitude")
            longitude = data.get("longitude")
            speed = data.get("speed")
            car_id = data.get("car_id")
            acceleration = data.get("acceleration")
            date_time = data.get("date_time")
            car = Car.objects.filter(pk=car_id).first()
            if not car:
                return Response({"message": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

            Location.objects.create(
                latitude=latitude,
                longitude=longitude,
                speed=speed,
                car=car,
                acceleration=acceleration,
                created_time=date_time
            )

            return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)

        except (KeyError, ValueError):
            return Response({"message": "Invalid or incomplete data provided"}, status=status.HTTP_400_BAD_REQUEST)
