from rest_framework import serializers
from rounds.models import Task, EventRound1, Round1Submission, Round2Submission, ImageTask, EventRound2

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "detail")

class Round1Serializer(serializers.ModelSerializer):
    task = TaskSerializer()
    class Meta:
        model = EventRound1
        fields = ('id', 'event', 'task', 'title', 'desc')

class Round1SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round1Submission
        fields = '__all__'

class ImageTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTask
        fields = ("id", "detail","ref_image")

class Round2Serializer(serializers.ModelSerializer):
    task = ImageTaskSerializer()
    class Meta:
        model = EventRound1
        fields = ('id', 'event', 'task', 'title', 'desc')

class Round2SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round2Submission
        fields = '__all__'

