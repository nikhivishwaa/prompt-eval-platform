from rest_framework import serializers
from challenge.models import Event, Participation

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = "__all__" 