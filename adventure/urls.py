from adventure import views
from django.urls import path

urlpatterns = [
    path("create-vehicle/", views.CreateVehicleAPIView.as_view()),
    path("start/", views.StartJourneyAPIView.as_view()),
    path("end/<int:pk>/", views.EndJourneyAPIView.as_view()),
]
