from django.shortcuts import render, redirect
from challenge.models import Event, Participation
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from temp.cache import get_challenge
import datetime as dt
from challenge.serializers import ParticipantSerializer, ChallengeSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

class ChallengeViewSet(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        events = Event.objects.filter(open_event=True)
        serializer = ChallengeSerializer(events, many=True)
        response = {'status': 'success','message':'all challenges', 'data':serializer.data}
        return Response(response, status=status.HTTP_200_OK)

class ChallengeDetailViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, challenge_no):
        try:
            events = Event.objects.get(pk=challenge_no)
            serializer = ChallengeSerializer(events)
            response = {'status': 'success','message':'all challenges', 'data':serializer.data}
            return Response(response, status=status.HTTP_200_OK)
            
        except Event.DoesNotExist:
            response = {'status': 'failed','message':'Challenge not found', 'data':{}}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

class ParticipationDetailViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, challenge_no):
        try:
            event = get_challenge(challenge_no)
            participant = Participation.objects.get(event=event, user=request.user)
            serializer = ParticipantSerializer(participant)
            response = {'status': 'success','message':'participation is available', 'data':serializer.data}
            return Response(response, status=status.HTTP_200_OK)

        except Participation.DoesNotExist:
            response = {'status': 'failed','message':'participation not found', 'data':{}}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Event.DoesNotExist:
            response = {'status': 'failed','message':'event not found', 'data':{}}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, challenge_no):
        try:
            event = get_challenge(challenge_no)
            participant = Participation.objects.get(event=event, user=request.user)
            serializer = ParticipantSerializer(participant)
            response = {'status': 'failed','message':'already participated', 'data':serializer.data}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        except Participation.DoesNotExist:
            if event.round1_status() in ('Upcoming','Ongoing') and event.stop_entry is False:
                participant = Participation(event=event, user=request.user)
                participant.save()
                serializer = ParticipantSerializer(participant)
                response = {'status': 'success','message':'participated successfully', 'data':serializer.data}
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response = {'status': 'failed','message':'participation is closed', 'data':{}}
                return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Event.DoesNotExist:
            response = {'status': 'failed','message':'event not found', 'data':{}}
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class LeaderBoardViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, challenge_no):
        try:
            event = get_challenge(challenge_no)
            participant = Participation.objects.filter(event=event)
            serializer = ParticipantSerializer(participant, many=True)
            response = {'status': 'success','message':'leaderboard', 'data':serializer.data}
            return Response(response, status=status.HTTP_200_OK)

        except Event.DoesNotExist:
            response = {'status': 'failed','message':'event not found', 'data':[]}
            return Response(response, status=status.HTTP_404_NOT_FOUND)