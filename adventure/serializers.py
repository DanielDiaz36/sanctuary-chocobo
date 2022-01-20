from rest_framework import serializers


class VehicleSerializer(serializers.Serializer):
    name = serializers.CharField()
    passengers = serializers.IntegerField()


class JourneySerializer(serializers.Serializer):
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
