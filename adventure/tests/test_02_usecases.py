import pytest
from adventure import models, notifiers, repositories, usecases
from django.utils import timezone
from adventure.repositories import JourneyRepository

#########
# Mocks #
#########


class MockJourneyRepository(repositories.JourneyRepository):
    def get_or_create_car(self, name: str = "car", max_capacity: int = 5) -> models.VehicleType:
        return models.VehicleType(name="car", max_capacity=4)

    def create_vehicle(
        self, name: str, passengers: int, vehicle_type: models.VehicleType
    ) -> models.Vehicle:
        return models.Vehicle(
            name=name, passengers=passengers, vehicle_type=vehicle_type
        )

    def create_journey(self, vehicle) -> models.Journey:
        return models.Journey(vehicle=vehicle, start=timezone.now())


class MockNotifier(notifiers.Notifier):
    def send_notifications(self, journey: models.Journey) -> None:
        pass


#########
# Tests #
#########


class TestStartJourney:
    def test_start(self):
        repo = MockJourneyRepository()
        notifier = MockNotifier()
        data = {"name": "Kitt", "passengers": 2}
        usecase = usecases.StartJourney(repo, notifier).set_params(data)
        journey = usecase.execute()

        assert journey.vehicle.name == "Kitt"

    def test_cant_start(self):
        repo = MockJourneyRepository()
        notifier = MockNotifier()
        data = {"name": "Kitt", "passengers": 6}
        usecase = usecases.StartJourney(repo, notifier).set_params(data)
        with pytest.raises(usecases.StartJourney.CantStart):
            journey = usecase.execute()


class TestStopJourney:
    # @pytest.mark.skip  # Remove
    @pytest.mark.django_db
    def test_stop(self):
        # TODO: Implement a StopJourney Usecase
        # it takes a started journey as a parameter and sets an "end" value
        # then saves it to the database

        repo = JourneyRepository()
        notifier = MockNotifier()
        data = {"name": "Tesla", "passengers": 3}
        usecase = usecases.StartJourney(repo, notifier).set_params(data)
        started_journey = usecase.execute()

        end = timezone.now()
        data = {"started_journey": started_journey, "end": end}

        usecase = usecases.EndJourney(repo, notifier).set_params(data)
        end_journey = usecase.execute()

        assert end_journey.is_finished() is True
