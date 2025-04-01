import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor

def evaluate_round1(submission):
    data = {
        "task": submission.round1_task.task.detail,
        "prompt": submission.prompt
    }

    with ThreadPoolExecutor() as executor:
        future = executor.submit(requests.post, os.getenv('ROUND1_EVAL_API'), json=data)
        response = future.result()

    if response.status_code == 200:
        scores = response.json()
        submission.creativity = scores.get('creativity', 0)
        submission.clarity = scores.get('clarity', 0)
        submission.relavance = scores.get('relevance', 0)
        submission.optimization = scores.get('optimization', 0)
        submission.evaluated = True
        submission.save()
        return True
    return False

def check_plagrism(image):
    data = {"images": [image]}
    
    with ThreadPoolExecutor() as executor:
        future = executor.submit(requests.post, os.getenv('REVERSE_SEARCH_API'), json=data)
        response = future.result()

    if response.status_code == 200:
        plagrism = response.json()[0]
        if plagrism.get('success') and (
            plagrism['data'].get('full_matching_images') or 
            plagrism['data'].get('pages_with_matching_images')
        ):
            return {
                "full_match": [i['url'] for i in plagrism['data']['full_matching_images']],
                "partial_match": [i['url'] for i in plagrism['data']['pages_with_matching_images']]
            }
    return None

def evaluate_round2(submission):
    data = {
        "task": submission.round2_task.task.detail,
        "ref_image": submission.round2_task.task.ref_image.url,
        "generated_image": submission.generated_image.url
    }

    with ThreadPoolExecutor() as executor:
        future = executor.submit(requests.post, os.getenv('ROUND2_EVAL_API'), json=data)
        response = future.result()

    if response.status_code == 200:
        scores = response.json()
        submission.clarity = scores.get('clarity', 0)
        submission.creativity = scores.get('creativity', 0)
        submission.relavance = scores.get('relevance', 0)
        submission.authenticity = scores.get('authenticity', 0)
        submission.similarity = scores.get('similarity', 0)
        submission.watermark_detection = scores.get('watermark_detection', 0)

        if submission.getscore() > 45:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(check_plagrism, submission.generated_image.url)
                plagrism = future.result()

            submission.plagrism_checked = True
            if plagrism:
                submission.plagrism_detected = True
                submission.plagrism_result = json.dumps(plagrism)

        submission.evaluated = True
        submission.save()
        return True
    return False
