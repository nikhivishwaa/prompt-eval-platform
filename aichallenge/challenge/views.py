from django.shortcuts import render, redirect
from challenge.models import Event, Participation
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from temp.cache import get_challenge
import datetime as dt

def list_challenges(request):
    # if not request.user.is_authenticated():
    # events = Event.objects.filter(open_event=True, round1_end_ts__gt=dt.datetime.now(dt.timezone.utc))
    events = Event.objects.filter(open_event=True)
    return render(request, 'challenge/index.html', {"challenges": events})

    # else:
    #     events = Event.objects.filter
    # return render(request, 'challenge/index.html', {"challenges": events})



@login_required(login_url="login")
def get_challenge_home(request, challenge_no):
    try:
        event = get_challenge(challenge_no)
        if not event.open_event:
            return HttpResponse("Challenge not available")
        participation = Participation.objects.filter(event=event, user=request.user)
        
        if participation.exists():
            participant = participation.first()
            context = {"challenge": event, "participation": participant}
            return render(request, 'challenge/home.html', context)
        else:
            return HttpResponse("You haven't participated in the challenge")

    except Event.DoesNotExist:
        return HttpResponse("Challenge not found")



@login_required(login_url="login")
def participate(request, challenge_no):
    """take participation in challenge"""
    try:
        event = get_challenge(challenge_no)

        if event.open_event == False:
            messages.error(request, "Challenge is not open for participation")
            return redirect('challenge:all_challenge')

        elif event.event_status() == "Finished":
            messages.warning(request, "Challenge has already finished")
            return redirect('challenge:all_challenge')

        elif event.round2_status() == "Ongoing":
            messages.warning(request, "You are not Allowed to Participate! Round1 has already finished")
            return redirect('challenge:all_challenge')

        participaint = Participation.objects.filter(event=event, user=request.user)

        if participaint.exists():
            messages.info(request, "You have already participated in this challenge")
            return redirect('challenge:challenge_detail', challenge_no=challenge_no)

        else:
            participation = Participation(event=event, user=request.user)
            participation.save()
            messages.success(request, f"You have successfully participated in '{participation.event.event_name}' challenge")
            return redirect('challenge:challenge_detail', challenge_no=challenge_no)

    except Event.DoesNotExist:
        messages.error(request, "Challenge not found")
        return redirect('challenge:all_challenge')

def get_leaderboard(request, challenge_no):
    """show leaderboard of a challenge"""
    try:
        event = get_challenge(challenge_no)
        leaderboard = Participation.objects.filter(event = event)
        
        return render(request, 'challenge/leaderboard.html', {"leaderboard": leaderboard})

    except Event.DoesNotExist:
        return HttpResponse("Challenge not found")