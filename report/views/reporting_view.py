from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from report.reporting_class import Reporting


class ReportingAPIView(APIView):
    def post(self, request):
        try:
            car_id = request.data.get("car_id")
            start_date = request.data.get("start_date")
            end_date = request.data.get("end_date")
            standard_id = request.data.get("standard_id")
            authorization_header = request.headers.get('Authorization')

            if standard_id == '':
                standard_id = None

            token = authorization_header.split(' ')[1]
            reporting_instance = Reporting(car_id=car_id)
            start_date, end_date = reporting_instance.convert_date_type_to_datetime(start_date=start_date,
                                                                                    end_date=end_date)

            if reporting_instance.check_car_existence():

                if reporting_instance.company_member_check(token=token):
                    data = reporting_instance.can_use_cache_or_not(start_date=start_date.date(),
                                                                   end_date=end_date.date(),
                                                                   standard_id=standard_id)

                    return Response(data, status=status.HTTP_200_OK)

                return Response({"message": "Only company's users can see the reports"},
                                status=status.HTTP_403_FORBIDDEN)

            return Response({"message": "Your inserted Car ID seems to be inactive and does not have a trip yet"},
                            status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"message": "Invalid inputs"}, status=status.HTTP_404_NOT_FOUND)
