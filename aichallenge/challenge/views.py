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
        participation = Participation.objects.filter(event=event, user=request.user)
        
        if participation.exists():
            participant = participation.first()
        # return HttpResponse(event)
        context = {"challenge": event, "participation": participant}
        return render(request, 'challenge/home.html', context)

    except Event.DoesNotExist:
        return HttpResponse("Challenge not found")



@login_required(login_url="login")
def participate(request, challenge_no):
    """take participation in challenge"""
    try:
        print(challenge_no)
        event = Event.objects.get(pk=challenge_no)
        if event.event_status() == "Finished":
            messages.warning(request, "Challenge has already finished")
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
        print(challenge_no)
        leaderboard = Participation.objects.filter(event__id = challenge_no)
        # return HttpResponse(event)
        return render(request, 'challenge/leaderboard.html', {"leaderboard": leaderboard})

    except Event.DoesNotExist:
        return HttpResponse("Challenge not found")