from django.shortcuts import render, redirect
from challenge.models import Event, Participation
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def list_challenges(request):
    events = Event.objects.all()

    return render(request, 'challenge/index.html', {"challenges": events})
    # return HttpResponse(events)


def get_challenge(request, challenge_no):
    try:
        print(challenge_no)
        event = Event.objects.get(pk=challenge_no)
        # return HttpResponse(event)
        return render(request, 'challenge/home.html', {"challenge": event})

    except Event.DoesNotExist:
        return HttpResponse("Challenge not found")



@login_required(login_url="login")
def participate(request, challenge_no):
    """take participation in challenge"""
    try:
        print(challenge_no)
        participaint = Participation.objects.filter(event__id=challenge_no, user=request.user)

        if participaint.exists():
            messages.info(request, "You have already participated in this challenge")
            return redirect('challenge:all_challenge')

        else:
            event = Event.objects.get(pk=challenge_no)
            participation = Participation(event=event, user=request.user)
            participation.save()
            messages.success(request, "You have successfully participated in this challenge")
            return redirect('all_challenge')

        # return HttpResponse(event)
        return render(request, 'challenge/index.html', {"challenge_no": challenge_no})

    except Event.DoesNotExist:
        return HttpResponse("Challenge not found")

def get_leaderboard(request, challenge_no):
    """show leaderboard of a challenge"""
    try:
        print(challenge_no)
        leaderboard = Participation.objects.filter(event__id = challenge_no)
        # return HttpResponse(event)
        return render(request, 'challenge/leaderboard.html', {"leaderboard": leaderboard})

    except Event.DoesNotExist:
        return HttpResponse("Challenge not found")