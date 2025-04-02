from django.db import connection
from aichallenge.settings import MEDIA_URL as path

def round1_report(challenge_no):
    q = f"""
    SELECT u.first_name ||' '|| u.last_name AS name, u.email, u.phone, p.id AS participant_id, p.round1_evaluated, p.round1_status, p.round1_rank, 
    s.round1_task_id AS task_id, s.clarity, s.creativity, s.relavance, 
    s.optimization, s.score, s.submitted_at, s.evaluated AS task_evaluated  
    FROM "rounds_round1submission" AS s 
    JOIN "challenge_participation" AS p ON s.participant_id=p.id AND p.event_id={challenge_no}
    JOIN "Users" AS u ON u.id=p.user_id
    ORDER BY p.round1_rank, task_id
    """

    with connection.cursor() as cursor:
        cursor.execute(q)
        columns = [col[0] for col in cursor.description]  # Extract column names
        results = [row for row in cursor.fetchall()]  # get entries

    # create dictionary with column and data
    return {'columns':columns,'data': results}

def round2_report(challenge_no):
    q = f"""
    SELECT u.first_name ||' '|| u.last_name AS name, u.email, u.phone, p.id AS participant_id, p.round2_evaluated, p.round2_status, p.round2_rank, 
    s.round2_task_id AS task_id, 
    '{path}'||s.generated_image AS image, s.clarity, s.creativity, s.relavance AS relevance, s.watermark_detection AS watermark,
    s.similarity, s.authenticity, s.plagrism_detected AS plagiarism,
    s.score, s.submitted_at, s.evaluated AS task_evaluated  
    FROM "rounds_round2submission" AS s 
    JOIN "challenge_participation" AS p ON s.participant_id=p.id AND p.event_id={challenge_no}
    JOIN "Users" AS u ON u.id=p.user_id
    ORDER BY p.round2_rank, task_id
    """

    with connection.cursor() as cursor:
        cursor.execute(q)
        columns = [col[0] for col in cursor.description]  # Extract column names
        results = [row for row in cursor.fetchall()]  # get entries

    # create dictionary with column and data
    return {'columns':columns,'data': results}
