from django.shortcuts import render
from rounds.models import Task, EventRound1, EventRound2, Round1Submission
from challenge.models import Event, Participation
from django.http import HttpResponse, JsonResponse
from worker.evaluator import evaluate_round1
import datetime as dt

# Create your views here.
def get_task(request, challenge_no):
    tasks = Task.objects.all()
    print(challenge_no)
    # return HttpResponse(tasks)
    return render(request, 'rounds/round1.html', {"tasks": tasks, "challenge_no": challenge_no})


def get_leaderboard(request, challenge_no):
    return render(request, 'rounds/leaderboard.html', {"challenge_no": challenge_no})

def submit_task(request, challenge_no, task_id):
    if request.method == 'POST':
        try:
            prompt = request.POST['prompt']
            entry = Submission.objects.filter(task__id=task_id, participant__id=challenge_no)
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
                participant = Challenge.objects.get(pk=challenge_no)
                task = Task.objects.get(pk=task_id)
                submission = Submission.objects.create(participant=participant, task=task, prompt=prompt)
                success = evaluate_round1(submission)
                if success:
                    return JsonResponse({"message":"submitted", "score": submission.getscore()})
                else:
                    return JsonResponse({"message":"failed to evaluate"})

            # to do propogate score to all participants

            return HttpResponse("submitted")
        except Task.DoesNotExist:
            return HttpResponse("invalid task")