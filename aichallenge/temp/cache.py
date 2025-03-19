from challenge.models import Event

challenge_list = dict()

def get_challenge(id):
    try:
        return challenge_list[id]
    except KeyError:
        challenge = Event.objects.get(id=id)
        challenge_list[id] = challenge
        return challenge

def remove_challenge(challenge_no):
    try:
        del challenge_list[challenge_no]
    except KeyError:
        pass

def update_challenge(challenge):
    try:
        challenge_list[challenge.id] = challenge
        print("cache updates")
    except Exception as e:
        pass