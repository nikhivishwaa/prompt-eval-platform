from django.shortcuts import render, redirect
from rounds.models import Task, EventRound1, EventRound2, Round1Submission, Round2Submission, ImageTask
from challenge.models import Event, Participation
from django.http import HttpResponse, JsonResponse
from worker.evaluator import evaluate_round1, evaluate_round2
import datetime as dt
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Min, Max, Count, F, Value
from django.db.models.functions import Concat
from temp.cache import get_challenge

# Create your views here.

@login_required(login_url="login")
def get_round1(request, challenge_no):
    try:
        event = get_challenge(challenge_no)
        if event.round1_status() == "Upcoming":
            return HttpResponse("Round 1 not started yet")
        tasks = EventRound1.objects.filter(event=event)
       
        return render(request, 'rounds/round1.html', {"tasks": tasks, "challenge": event, "total_score": 100 * len(tasks)})
    except Event.DoesNotExist:
        return HttpResponse("Invalid Challenge")

@login_required(login_url="login")
def get_round1_task_submission(request, challenge_no, task_id):
    try:
        event = get_challenge(challenge_no)
        if event.round1_status() == "Upcoming":
            return JsonResponse({"error": "Round 1 not started yet"}, status=405)
        submission = Round1Submission.objects.filter(round1_task__id=task_id, participant__user=request.user, participant__event=event).values('prompt', 'clarity', 'creativity', 'evaluated', 'relavance', 'optimization', 'submitted_at','last_updated','score')
        if submission.exists():
            data = submission.first()
            data['task_id'] = task_id
            return JsonResponse(data)
        else:
            return JsonResponse({"error":"No Submission found"}, status=400)
    except Event.DoesNotExist:
        return JsonResponse({"error":"Invalid Challenge"}, status=404)


@login_required(login_url="login")
def get_round1_score(request, challenge_no):
    try:        
        event = get_challenge(challenge_no)
        if event.round1_status() == "Upcoming":
            return JsonResponse({"error": "Round 1 not started yet"}, status=405)
        submission = Round1Submission.objects.filter(participant__event=event, participant__user=request.user, evaluated=True)
        if submission.exists():
            data = submission.aggregate(score=Sum('score'))
            data['score'] = round(data['score'], 2)
            data['detailed_score'] = {f'task{i}': s.score for i, s in enumerate(submission, 1)}
            # print(data)
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

        submission = Round1Submission.objects.filter(participant__event=event, participant__user=request.user).values(*fields)
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

        submissions = Round1Submission.objects.filter(participant__event=event, evaluated=True).values('participant')
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


@login_required(login_url="login")
def submit_round1_task(request, challenge_no, task_id):
    if request.method == 'POST':
        try:
            event = get_challenge(challenge_no)
            if event.round1_status() == "Upcoming":
                return JsonResponse({"error": "Round 1 not started yet"}, status=405)
            elif event.round2_status() == "Finished":
                return JsonResponse({"error": "Round 1 had finished!"}, status=405)

            prompt = request.POST['prompt']
            entry = Round1Submission.objects.filter(round1_task__id=task_id, participant__user=request.user, participant__event=event)
            # print(entry)
            if entry.exists():
                if entry.first().evaluated:
                    return redirect('challenge:get_task_submission_r1', challenge_no=challenge_no, task_id=task_id)
                else:
                    submission = entry.first()
                    submission.update(prompt=prompt)
                    success = evaluate_round1(submission)
                    if success:
                        return redirect('challenge:get_task_submission_r1', challenge_no=challenge_no, task_id=task_id)
                    else:
                        return JsonResponse({"error":"failed to evaluate"}, status=500)

            else:
                participant = Participation.objects.filter(event__id=challenge_no, user=request.user).first()
                task = EventRound1.objects.get(pk=task_id)
                submission = Round1Submission(participant=participant, round1_task=task, prompt=prompt)
                submission.save()
                success = evaluate_round1(submission)
                if success:
                    # return JsonResponse({"message":"submitted", "score": submission.getscore()})
                    return redirect('challenge:get_task_submission_r1', challenge_no=challenge_no, task_id=task_id)
                else:
                    return JsonResponse({"error":"failed to evaluate"}, status=500)

            # to do propogate score to all participants

        except Task.DoesNotExist:
            JsonResponse({"error":"Invalid Task"}, status=404)
        except Event.DoesNotExist:
            return JsonResponse({"error":"Invalid Challenge"}, status=404)


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

        submission = Round2Submission.objects.filter(round2_task__id=task_id, participant__user=request.user, participant__event=event).values(*fields)
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

                
        submission = Round2Submission.objects.filter(participant__event=event, participant__user=request.user, evaluated=True)
        if submission.exists():
            data = submission.aggregate(score=Sum('score'))
            data['score'] = round(data['score'], 2)
            data['detailed_score'] = {f'task{i}': s.score for i, s in enumerate(submission, 1)}
            # print(data)
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

        submission = Round2Submission.objects.filter(participant__event=event, participant__user=request.user).values(*fields)
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
                
        submissions = Round2Submission.objects.filter(participant__event=event, evaluated=True).values('participant')
        leaderboard = submissions.annotate(attempted_task=Count('participant'), 
                                        submission_time = Max('submitted_at'), 
                                        score = Sum('score'), 
                                        email = F('participant__user__email'),
                                        name = Concat('participant__user__first_name', Value(' '), 'participant__user__last_name')).order_by('-score','-submission_time')
        return render(request, 'rounds/leaderboard.html', {"challenge_no": challenge_no, "user_ranking":leaderboard, "round":2})
        # return JsonResponse(list(leaderboard), safe=False)
    except Event.DoesNotExist:
        return HttpResponse("Invalid Challenge")

@login_required(login_url="login")
def submit_round2_task(request, challenge_no, task_id):
    if request.method == 'POST':
        try:
            event = get_challenge(challenge_no)
            if event.round2_status() == "Upcoming":
                return JsonResponse({"error":"Round 2 not started yet"}, status=405)
            elif event.round2_status() == "Finished":
                return JsonResponse({"error":"Round 2 had finished!"}, status=405)

            image = request.FILES['generated_image']
            entry = Round2Submission.objects.filter(round2_task__id=task_id, participant__user=request.user, participant__event=event)
            print(entry)
            if entry.exists():
                if entry.first().evaluated:
                    redirect('challenge:get_task_submission_r2', challenge_no=challenge_no, task_id=task_id)
                else:
                    submission = entry.first()
                    submission.generated_image = image
                    submission.save()
                    success = evaluate_round2(submission)
                    if success:
                        return redirect('challenge:get_task_submission_r2', challenge_no=challenge_no, task_id=task_id)
                    else:
                        return JsonResponse({"error":"failed to evaluate"}, status=500)

            else:
                participant = Participation.objects.filter(event__id=challenge_no, user=request.user).first()
                task = EventRound2.objects.get(pk=task_id)
                submission = Round2Submission(participant=participant, round2_task=task, generated_image=image)
                submission.save()
                success = evaluate_round2(submission)
                if success:
                    return redirect('challenge:get_task_submission_r2', challenge_no=challenge_no, task_id=task_id)
                else:
                    return JsonResponse({"error":"failed to evaluate"}, status=500)

            # to do propogate score to all participants
            print("reason 123")
        except Task.DoesNotExist:
            return JsonResponse({"error":"Invalid Task"}, status=404)
        except Event.DoesNotExist:
            return JsonResponse({"error":"Invalid Challenge"}, status=404)