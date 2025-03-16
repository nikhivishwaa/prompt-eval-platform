from django.shortcuts import render
from .models import Event
from django.http import HttpResponse

# Create your views here.
def list_challenges(request):
    events = Event.objects.all()

    # return render(request, 'challenge/index.html', {"challeneges": events})
    return HttpResponse(events)


def get_challenge(request, challenge_no):
    try:
        print(challenge_no)
        event = Event.objects.get(pk=challenge_no)
        return HttpResponse(event)

    except Event.DoesNotExist:
        return HttpResponse("Challenge not found")

