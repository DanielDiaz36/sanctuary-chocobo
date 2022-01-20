from adventure import models, notifiers, repositories, serializers, usecases
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError


class CreateVehicleAPIView(APIView):
    def post(self, request: Request) -> Response:
        payload = request.data
        vehicle_type = models.VehicleType.objects.get(name=payload["vehicle_type"])
        vehicle = models.Vehicle.objects.create(
            name=payload["name"],
            passengers=payload["passengers"],
            vehicle_type=vehicle_type,
        )
        return Response(
            {
                "id": vehicle.id,
                "name": vehicle.name,
                "passengers": vehicle.passengers,
                "vehicle_type": vehicle.vehicle_type.name,
            },
            status=201,
        )


class StartJourneyAPIView(generics.CreateAPIView):
    serializer_class = serializers.VehicleSerializer

    def perform_create(self, serializer) -> None:
        repo = self.get_repository()
        notifier = notifiers.Notifier()
        usecase = usecases.StartJourney(repo, notifier).set_params(
            serializer.validated_data
        )
        try:
            usecase.execute()
        except usecases.StartJourney.CantStart as e:
            raise ValidationError({"detail": str(e)})

    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()


class EndJourneyAPIView(generics.UpdateAPIView):

    def put(self, request, *args, **kwargs):
        try:
            journey = models.Journey.objects.get(id=self.kwargs['pk'])

            repo = self.get_repository()
            notifier = notifiers.Notifier()
            data = {"started_journey": journey, "end": timezone.now()}

            usecases.EndJourney(repo, notifier).set_params(data).execute()

            return Response(
                {
                    "journey_id": journey.id,
                    "start": journey.start,
                    "end": journey.end,
                },
                status=status.HTTP_200_OK
            )

        except models.Journey.DoesNotExist as e:
            raise ValidationError({"detail": str(e)})

    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()
