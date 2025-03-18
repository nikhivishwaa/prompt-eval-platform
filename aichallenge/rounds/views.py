from django.shortcuts import render
from rounds.models import Task, EventRound1, EventRound2, Round1Submission
from challenge.models import Event, Participation
from django.http import HttpResponse, JsonResponse
from worker.evaluator import evaluate_round1
import datetime as dt
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Min, Max, Count, F, Value
from django.db.models.functions import Concat


# Create your views here.

@login_required(login_url="login")
def get_round1(request, challenge_no):
    tasks = EventRound1.objects.filter(event__id=challenge_no)
    print(tasks)
    print(challenge_no)
    # return HttpResponse(tasks)
    return render(request, 'rounds/round1.html', {"tasks": tasks, "challenge_no": challenge_no})


@login_required(login_url="login")
def get_round1_submission(request, challenge_no, task_id):
    submission = Round1Submission.objects.filter(round1_task__id=task_id, participant__user=request.user).values('prompt', 'clarity', 'creativity', 'evaluated', 'relavance', 'optimization', 'submitted_at','last_updated','score')
    if submission.exists():
        data = submission.first()
        data['task_id'] = task_id
        return JsonResponse(data)
    else:
        return JsonResponse({"error":"No Submission found"})

@login_required(login_url="login")
def get_round1_score(request, challenge_no):
    submission = Round1Submission.objects.filter(participant__event__id=challenge_no, participant__user=request.user, evaluated=True)
    if submission.exists():
        data = submission.aggregate(score=Sum('score'))
        data['detailed_score'] = {f'task{i}': s.score for i, s in enumerate(submission, 1)}
        print(data)
        # data['task_id'] = task_id
        return JsonResponse(data)
    else:
        return JsonResponse({"error":"No Submission found"})

@login_required(login_url="login")
def get_round1_submission(request, challenge_no):
    submission = Round1Submission.objects.filter(participant__event__id=challenge_no, participant__user=request.user).values('id','prompt', 'clarity', 'creativity',  'relavance', 'optimization', 'evaluated', 'submitted_at','last_updated','score')
    if submission.exists():
        return JsonResponse(list(submission), safe=False)
    else:
        return JsonResponse({"error":"No Submission found"})


@login_required(login_url="login")
def get_leaderboard(request, challenge_no):
    return render(request, 'rounds/leaderboard.html', {"challenge_no": challenge_no})

@login_required(login_url="login")
def get_round1_leaderboard(request, challenge_no):
    submissions = Round1Submission.objects.filter(participant__event__id=challenge_no, evaluated=True).values('participant')
    leaderboard = submissions.annotate(attempted_task=Count('participant'), 
                                       submission_time = Max('submitted_at'), 
                                       score = Sum('score'), 
                                       email = F('participant__user__email'),
                                       name = Concat('participant__user__first_name', Value(' '), 'participant__user__last_name')).order_by('-score','-submission_time')
    return render(request, 'rounds/leaderboard.html', {"challenge_no": challenge_no, "user_ranking":leaderboard})
    # return JsonResponse(list(leaderboard), safe=False)


@login_required(login_url="login")
def submit_round1_task(request, challenge_no, task_id):
    if request.method == 'POST':
        try:
            prompt = request.POST['prompt']
            entry = Round1Submission.objects.filter(round1_task__id=task_id, participant__user=request.user)
            print(entry)
            if entry.exists():
                if entry.first().evaluated:
                    return JsonResponse({"messsage":"task already evaluated"})
                else:
                    submission = entry.first()
                    submission.update(prompt=prompt)
                    success = evaluate_round1(submission)
                    if success:
                        return JsonResponse({"message":"submitted", "score": submission.getscore()})
                    else:
                        return JsonResponse({"message":"failed to evaluate"})

            else:
                participant = Participation.objects.filter(event__id=challenge_no, user=request.user).first()
                task = EventRound1.objects.get(pk=task_id)
                submission = Round1Submission(participant=participant, round1_task=task, prompt=prompt)
                submission.save()
                success = evaluate_round1(submission)
                if success:
                    return JsonResponse({"message":"submitted", "score": submission.getscore()})
                else:
                    return JsonResponse({"message":"failed to evaluate"})

            # to do propogate score to all participants

            return HttpResponse("submitted")
        except Task.DoesNotExist:
            return HttpResponse("invalid task")