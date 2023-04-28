import os
import logging
import random
from flask import abort, Flask, jsonify, request
import functions_framework

def is_request_valid(request):
    slack_request_cleint_token=request.form.get("token")
    slack_client_token=os.environ['SLACK_VERIFICATION_TOKEN']
    return slack_request_cleint_token == slack_client_token

@functions_framework.http
def new_game(request, methods=['POST']):

    if not is_request_valid(request):
        abort(400)

    request_json = request.get_json(silent=True)
    request_args = request.args

    players=set(request.form.get("text").split())

    team1 =  set(random.sample(sorted(players), 2))
    team2 = players - team1

    logging.info(team1)
    logging.info(team2)

    return jsonify(
        response_type='in_channel',
        text=f'Spiel startet zwischen Team_rot {team1} und Team_blau {team2}',
    )