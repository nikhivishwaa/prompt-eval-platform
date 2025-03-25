from django.shortcuts import render, redirect
from rounds.models import Task, EventRound1, EventRound2, Round1Submission, Round2Submission, ImageTask, Participation, Event
from django.http import HttpResponse, JsonResponse
from worker.evaluator import evaluate_round1, evaluate_round2
import datetime as dt
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Min, Max, Count, F, Value
from django.db.models.functions import Concat
from temp.cache import get_challenge
from rounds.serializers import Round1Serializer, Round1SubmissionSerializer, Round2Serializer, Round2SubmissionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

def validate_participation(participant_id:int):
    try:
        participant = Participation.objects.get(id=participant_id)
        return participant
    except Participation.DoesNotExist:
        return None

class Round1ViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, challenge_no):
        try:
            participant_id = request.data.get('participant')
            if participant_id:
                participant = validate_participation(participant_id)
                if participant is not None:
                    event = participant.event
                    if event.round1_status() == "Upcoming":
                        response = {'status': 'failed','message':'Round 1 not started yet', 'data':[]}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)

                    elif event.round1_status() == "Ongoing" and participant.started_at is None:
                        participant.started_at = dt.datetime.now(dt.timezone.utc)
                        participant.save()
            
                    tasks = EventRound1.objects.filter(event=event)
                    serializer = Round1Serializer(tasks, many=True)
                    response = {'status': 'success','message':'all tasks for round 1', 'data':serializer.data}
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = {'status': 'failed','message':'Invalid participant', 'data':[]}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'status': 'failed','message':'participant is not provided', 'data':[]}
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            response = {'status': 'failed','message':'Challenge not found', 'data':{}}
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class SubmissionViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, challenge_no, task_id):
        try:
            participant_id = request.data.get('participant')
            if participant_id:
                participant = validate_participation(participant_id)
                if participant is not None:
                    event = participant.event
                    if event.round1_status() == "Upcoming":
                        response = {'status': 'failed','message':'Round 1 not started yet', 'data':{}}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)

                    submission = Round1Submission.objects.get(round1_task__id=task_id, participant__user=request.user, participant__event=event)
                    # submission['task_id'] = task_id
                    serializer = Round1SubmissionSerializer(submission)

                    response = {'status': 'success','message':'submitted task', 'data':serializer.data}
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = {'status': 'failed','message':'Invalid participant', 'data':[]}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'status': 'failed','message':'participant is not provided', 'data':[]}
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Round1Submission.DoesNotExist:
            print(e)
            response = {'status': 'failed','message':'Submission not found', 'data':{}}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            response = {'status': 'failed','message':'Challenge not found', 'data':{}}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, challenge_no, task_id):
        try:
            participant_id = request.data.get('participant')
            create = False
            submission = None
            if participant_id:
                participant = validate_participation(participant_id)
                if participant is not None:
                    event = participant.event
                    if event.round1_status() == "Upcoming":
                        response = {'status': 'failed','message':'Round 1 not started yet', 'data':{}}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    elif event.round1_status() == "Finished":
                        response = {'status': 'failed','message':'Round 1 already finished', 'data':{}}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)

                    try:
                        submission = Round1Submission.objects.get(round1_task__id=task_id, participant__user=request.user, participant__event=event)
                        if submission.evaluated:
                            response = {'status': 'failed','message':'Prompt already submitted', 'data':{}}
                            return Response(response, status=status.HTTP_400_BAD_REQUEST)
                        
                    except Round1Submission.DoesNotExist:
                        prompt = request.data.get('prompt').strip()
                        if prompt < 30:
                            response = {'status': 'failed','message':'Prompt should be at least 30 characters long', 'data':{}}
                            return Response(response, status=status.HTTP_400_BAD_REQUEST)

                        submission = Round1Submission(participant=participant, round1_task=EventRound1.objects.get(pk=task_id), prompt=prompt)
                    
                    # evaluate new submission or old submission is not not evaluated yet
                    success = evaluate_round1(submission)
                    if success:
                        now = dt.datetime.now(dt.timezone.utc)
                        participant.round1_finish_time = min(now, event.round1_end_ts)
                        participant.finished_at = min(now, event.round1_end_ts)
                        participant.save()
                
                        response = {'status': 'success','message':'submitted task successfully', 'data':{'evaluated': True, 'score':submission.score}}
                        return Response(response, status=status.HTTP_201_CREATED)
                    else:
                        response = {'status': 'failed','message':'something went wrong', 'data':{}}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                else:
                    response = {'status': 'failed','message':'Invalid participant', 'data':{}}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'status': 'failed','message':'participant is not provided', 'data':{}}
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            response = {'status': 'failed','message':'Challenge not found', 'data':{}}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

class Round2ViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, challenge_no):
        try:
            participant_id = request.data.get('participant')
            if participant_id:
                participant = validate_participation(participant_id)
                if participant is not None:
                    event = participant.event
                    if event.round1_status() != "Finished":
                        response = {'status': 'failed','message':"wait till round 1 finished",'qualified': None, 'data':[]}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    elif participant.round1_status != "qualified":
                        response = {'status': 'failed','message':"You Haven't qualified Round 1",'qualified': False, 'data':[]}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    
                    if event.round2_status() == "Upcoming":
                        response = {'status': 'failed','message':'Round 2 not started yet','qualified': True, 'data':[]}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)

                    
                    tasks = EventRound2.objects.filter(event=event)
                    serializer = Round2Serializer(tasks, many=True)
                    response = {'status': 'success','message':'all tasks for round 2', 'data':serializer.data}
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = {'status': 'failed','message':'Invalid participant', 'data':[]}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'status': 'failed','message':'participant is not provided', 'data':[]}
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            response = {'status': 'failed','message':'Challenge not found', 'data':{}}
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class SubmissionR2ViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, challenge_no, task_id):
        try:
            participant_id = request.data.get('participant')
            if participant_id:
                participant = validate_participation(participant_id)
                if participant is not None:
                    event = participant.event
                    if event.round1_status() != "Finished":
                        response = {'status': 'failed','message':"wait till round 1 finished",'qualified': None, 'data':[]}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    elif participant.round1_status != "qualified":
                        response = {'status': 'failed','message':"You Haven't qualified Round 1",'qualified': False, 'data':[]}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    
                    if event.round2_status() == "Upcoming":
                        response = {'status': 'failed','message':'Round 2 not started yet','qualified': True, 'data':[]}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)

                    submission = Round2Submission.objects.get(round2_task__id=task_id, participant__user=request.user, participant__event=event)
                    # submission['task_id'] = task_id
                    serializer = Round2SubmissionSerializer(submission)

                    response = {'status': 'success','message':'submitted task', 'data':serializer.data}
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = {'status': 'failed','message':'Invalid participant', 'data':[]}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'status': 'failed','message':'participant is not provided', 'data':[]}
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Round1Submission.DoesNotExist:
            print(e)
            response = {'status': 'failed','message':'Submission not found', 'data':{}}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            response = {'status': 'failed','message':'Challenge not found', 'data':{}}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, challenge_no, task_id):
        try:
            participant_id = request.data.get('participant')
            submission = None
            if participant_id:
                participant = validate_participation(participant_id)
                if participant is not None:
                    event = participant.event
                    if event.round1_status() != "Finished":
                        response = {'status': 'failed','message':"wait till round 1 finished",'qualified': None, 'data':{}}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    elif participant.round1_status != "qualified":
                        response = {'status': 'failed','message':"You Haven't qualified Round 1",'qualified': False, 'data':{}}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    
                    if event.round2_status() == "Upcoming":
                        response = {'status': 'failed','message':'Round 2 not started yet','qualified': True, 'data':{}}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    elif event.round2_status() == "Finished":
                        response = {'status': 'failed','message':'Round 2 already finished', 'data':{}}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)

                    try:
                        submission = Round2Submission.objects.get(round2_task__id=task_id, participant__user=request.user, participant__event=event)
                        if submission.evaluated:
                            response = {'status': 'failed','message':'Image already submitted', 'data':{}}
                            return Response(response, status=status.HTTP_400_BAD_REQUEST)
                        
                    except Round2Submission.DoesNotExist:
                        image = request.FILES.get('image', None)
                        if image is None:
                            response = {'status': 'failed','message':'Generated image is not uploaded', 'data':{}}
                            return Response(response, status=status.HTTP_400_BAD_REQUEST)

                        submission = Round2Submission(participant=participant, round2_task=EventRound2.objects.get(pk=task_id), generated_image=image)
                        submission.save()

                    # evaluate new submission or old submission is not not evaluated yet
                    success = evaluate_round2(submission)
                    if success:
                        now = dt.datetime.now(dt.timezone.utc)
                        participant.round2_finish_time = min(now, event.round2_end_ts)
                        participant.finished_at = min(now, event.round2_end_ts)
                        participant.save()
                
                        response = {'status': 'success','message':'submitted task successfully', 'data':{'evaluated': True, 'score':submission.score}}
                        return Response(response, status=status.HTTP_201_CREATED)
                    else:
                        response = {'status': 'failed','message':'something went wrong', 'data':{}}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                else:
                    response = {'status': 'failed','message':'Invalid participant', 'data':{}}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'status': 'failed','message':'participant is not provided', 'data':{}}
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            response = {'status': 'failed','message':'Challenge not found', 'data':{}}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

@login_required(login_url="login")
def get_round1_score(request, challenge_no):
    try:        
        event = get_challenge(challenge_no)
        if event.round1_status() == "Upcoming":
            return JsonResponse({"error": "Round 1 not started yet"}, status=405)
            
        submission = Round1Submission.objects.filter(participant__event=event, submitted_at__lte=event.round1_end_ts, participant__user=request.user, evaluated=True)
        if submission.exists():
            data = submission.aggregate(score=Sum('score'))
            data['score'] = round(data['score'], 2)
            data['detailed_score'] = {f'task{i}': s.score for i, s in enumerate(submission, 1)}
            
            # update participant score if the event is ongoing
            if event.round1_status() == "Ongoing":
                participant = submission.first().participant
                if participant.round1_score != data['score']:
                    participant.round1_score = data['score']
                    participant.save()

            return JsonResponse(data)
        else:
            return JsonResponse({"error":"No Submission found"}, status=400)
    except Event.DoesNotExist:
        return JsonResponse({"error":"Invalid Challenge"}, status=404)

@login_required(login_url="login")
def get_round1_submission(request, challenge_no):
    try:
        event = get_challenge(challenge_no)
        if event.round1_status() == "Upcoming":
            return JsonResponse({"error": "Round 1 not started yet"}, status=405)

        fields = ('prompt', 'clarity', 'creativity', 
                  'relavance', 'optimization', 'evaluated',
                  'submitted_at','last_updated','score')

        submission = Round1Submission.objects.filter(participant__event=event, submitted_at__lte=event.round1_end_ts, participant__user=request.user).values(*fields)
        submission = submission.annotate(id=F('round1_task__id')).order_by('submitted_at')
        if submission.exists():
            return JsonResponse(list(submission), safe=False)
        else:
            return JsonResponse({"error":"No Submission found"}, status=400)
    except Event.DoesNotExist:
        return JsonResponse({"error":"Invalid Challenge"}, status=404)


@login_required(login_url="login")
def get_leaderboard(request, challenge_no):
    return render(request, 'rounds/leaderboard.html', {"challenge_no": challenge_no})

@login_required(login_url="login")
def get_round1_leaderboard(request, challenge_no):
    try:       
        event = get_challenge(challenge_no)
        if event.round1_status() == "Upcoming":
            return HttpResponse("Round 1 not started yet")

        submissions = Round1Submission.objects.filter(participant__event=event, submitted_at__lte=event.round1_end_ts, evaluated=True).values('participant')
        leaderboard = submissions.annotate(attempted_task=Count('participant'), 
                                       submission_time = Max('submitted_at'), 
                                       score = Sum('score'), 
                                       email = F('participant__user__email'),
                                       name = Concat('participant__user__first_name', Value(' '), 'participant__user__last_name'),
                                    ).order_by('-score','-submission_time')

        return render(request, 'rounds/leaderboard.html', {"challenge_no": challenge_no, "user_ranking":leaderboard, "round":1})
    # return JsonResponse(list(leaderboard), safe=False)
    except Event.DoesNotExist:
        return HttpResponse("Invalid Challenge")


## round 2
@login_required(login_url="login")
def get_round2(request, challenge_no):
    try:
        event = get_challenge(challenge_no)
        if event.round2_status() == "Upcoming":
            return HttpResponse("Round 2 not started yet")

        tasks = EventRound2.objects.filter(event=event)
        
        return render(request, 'rounds/round2.html', {"tasks": tasks, "challenge": event, "total_score": 100 * len(tasks)})
    except Event.DoesNotExist:
        return HttpResponse("Invalid Challenge")

@login_required(login_url="login")
def get_round2_task_submission(request, challenge_no, task_id):
    try:
        event = get_challenge(challenge_no)
        if event.round2_status() == "Upcoming":
            return JsonResponse({"error":"Round 2 not started yet"}, status=405)
    
    
        fields = ('generated_image', 'evaluated', 
                'clarity', 'creativity', 'relavance', 
                'authenticity', 'similarity', 'watermark_detection', 
                'score', 'plagrism_detected', 'plagrism_result', 
                'submitted_at','last_updated')

        submission = Round2Submission.objects.filter(round2_task__id=task_id, submitted_at__lte=event.round2_end_ts, participant__user=request.user, participant__event=event).values(*fields)
        if submission.exists():
            data = submission.first()
            data['task_id'] = task_id
            return JsonResponse(data)
        else:
            return JsonResponse({"error":"No Submission found"}, status=400)
    except Event.DoesNotExist:
        return JsonResponse({"error":"Invalid Challenge"}, status=404)


@login_required(login_url="login")
def get_round2_score(request, challenge_no):
    try:
        event = get_challenge(challenge_no)
        if event.round2_status() == "Upcoming":
            return JsonResponse({"error":"Round 2 not started yet"}, status=405)

                
        submission = Round2Submission.objects.filter(participant__event=event, submitted_at__lte=event.round2_end_ts, participant__user=request.user, evaluated=True)
        if submission.exists():
            data = submission.aggregate(score=Sum('score'))
            data['score'] = round(data['score'], 2)
            data['detailed_score'] = {f'task{i}': s.score for i, s in enumerate(submission, 1)}
            
            
            # update participant score if the event is ongoing
            if event.round2_status() == "Ongoing":
                participant = submission.first().participant
                if participant.round2_score != data['score']:
                    participant.round2_score = data['score']
                    participant.save()

            return JsonResponse(data)
        else:
            return JsonResponse({"error":"No Submission found"}, status=400)
    except Event.DoesNotExist:
        return JsonResponse({"error":"Invalid Challenge"}, status=404)


@login_required(login_url="login")
def get_round2_submission(request, challenge_no):
    try:
        event = get_challenge(challenge_no)
        if event.round2_status() == "Upcoming":
            return JsonResponse({"error":"Round 2 not started yet"}, status=405)

                
        fields = ('generated_image', 'evaluated', 
                'clarity', 'creativity', 'relavance', 
                'authenticity', 'similarity', 'watermark_detection', 
                'score', 'plagrism_detected', 'plagrism_result', 
                'submitted_at','last_updated')

        submission = Round2Submission.objects.filter(participant__event=event, submitted_at__lte=event.round1_end_ts, participant__user=request.user).values(*fields)
        submission = submission.annotate(id=F('round2_task__id')).order_by('submitted_at')
       
        if submission.exists():
            return JsonResponse(list(submission), safe=False)
        else:
            return JsonResponse({"error":"No Submission found"}, status=400)

    except Event.DoesNotExist:
        return JsonResponse({"error":"Invalid Challenge"}, status=404)


@login_required(login_url="login")
def get_round2_leaderboard(request, challenge_no):
    try:
        event = get_challenge(challenge_no)
        if event.round2_status() == "Upcoming":
            return HttpResponse("Round 2 not started yet")
                
        submissions = Round2Submission.objects.filter(participant__event=event, submitted_at__lte=event.round2_end_ts, evaluated=True).values('participant')
        leaderboard = submissions.annotate(attempted_task=Count('participant'), 
                                        submission_time = Max('submitted_at'), 
                                        score = Sum('score'), 
                                        email = F('participant__user__email'),
                                        name = Concat('participant__user__first_name', Value(' '), 'participant__user__last_name')).order_by('-score','-submission_time')
        return render(request, 'rounds/leaderboard.html', {"challenge_no": challenge_no, "user_ranking":leaderboard, "round":2})
        # return JsonResponse(list(leaderboard), safe=False)
    except Event.DoesNotExist:
        return HttpResponse("Invalid Challenge")