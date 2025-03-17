import os
import json
import requests

def evaluate_round1(submission):
    data = {"task":submission.round1_task.task.detail, "prompt": submission.prompt }
    response = requests.post(os.getenv('ROUND1_EVAL_API'), json=data)

    if response.status_code == 200:
        scores = response.json()
        print(scores)
        submission.creativity = scores['creativity']
        submission.clarity = scores['clarity']
        submission.relavance = scores['relevance']
        submission.optimization = scores['optimization']
        submission.evaluated = True
        submission.save()
        return True