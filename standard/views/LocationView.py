from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from standard.models.location import Location
from user.models import Car


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
                car_id=car,
                acceleration=acceleration,
                created_time=date_time
            )

            return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)

        except:
            return Response({"message": "Invalid or incomplete data provided"}, status=status.HTTP_400_BAD_REQUEST)