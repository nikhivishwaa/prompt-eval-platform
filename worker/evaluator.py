import os
import json
import requests

def evaluate_round1(submission):
    data = {"task":submission.round1_task.task.detail, "prompt": submission.prompt }
    response = requests.post(os.getenv('ROUND1_EVAL_API'), json=data)

    if response.status_code == 200:
        scores = response.json()
        # print(scores)
        submission.creativity = scores['creativity']
        submission.clarity = scores['clarity']
        submission.relavance = scores['relevance']
        submission.optimization = scores['optimization']
        submission.evaluated = True
        submission.save()
        return True


def check_plagrism(image):
    data = {"images": [image]}
    response = requests.post(os.getenv('REVERSE_SEARCH_API'), json=data)
    if response.status_code == 200:
        plagrism = response.json()[0]

        if plagrism['success'] and len(plagrism['data']['full_matching_images']) or len(plagrism['data']['pages_with_matching_images']):
            result = {}
            result['full_match'] = [i['url'] for i in plagrism['data']['full_matching_images'] ]
            result['partial_match'] = [i['url'] for i in plagrism['data']['pages_with_matching_images'] ]
            # print(result)

            return result
    return None

def evaluate_round2(submission):
    data = {
            "task":submission.round2_task.task.detail, 
            "ref_image": submission.round2_task.task.ref_image.url, 
            "generated_image": submission.generated_image.url 
        }

    # print(data)
    response = requests.post(os.getenv('ROUND2_EVAL_API'), json=data)

    if response.status_code == 200:
        scores = response.json()
        # print(scores)
        submission.clarity = scores['clarity']
        submission.creativity = scores['creativity']
        submission.relavance = scores['relevance']
        submission.authenticity = scores['authenticity']
        submission.similarity = scores['similarity']
        submission.watermark_detection = scores['watermark_detection']
        submission.save()

        if submission.getscore() > 45:
            plagrism = check_plagrism(submission.generated_image.url)
            submission.plagrism_checked = True
            if plagrism is not None:
                submission.plagrism_detected = True
                submission.plagrism_result = json.dumps(plagrism)
        
        submission.evaluated = True
        submission.save()
        return True
        



