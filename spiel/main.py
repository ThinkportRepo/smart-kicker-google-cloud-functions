import os
import logging
import json
import random
from flask import abort, Flask, jsonify, request
import functions_framework
import requests


def is_request_valid(request):
    slack_request_cleint_token=request.form.get("token")
    slack_client_token=os.environ['SLACK_VERIFICATION_TOKEN']
    

    return slack_request_cleint_token == slack_client_token

@functions_framework.http
def new_game(request, methods=['POST']):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """

    if not is_request_valid(request):
       abort(400)

    request_json = request.get_json(silent=True)
    request_args = request.args

    logging.warn(request_json)
    logging.warn(request.form.get("token"))

    players=set(request.form.get("text").split())

    team1 =  set(random.sample(sorted(players), 2))
    team2 = players - team1

    team1list = list(team1)
    team2list = list(team2)

    logging.info(team1)
    logging.info(team2)

    db = {
            "team-red": {"player1": team1list[0], "player2": team1list[1]},
            "team-blue": {"player1": team2list[0], "player2": team2list[1]}
        }

    logging.warn(db)
    headers = {
        'Content-Type': 'text/plain',
        'Solace-delivery-mode': 'direct',
    }

    data = json.dumps(db, default=tuple)

    response_solace = requests.post('https://mr-connection-3u9jr7lv79y.messaging.solace.cloud:9443/new/game/start', headers=headers, data=data, auth=('solace-cloud-client', 'sf08sq808ebt8rb4sqplfstso8'))
    logging.warn(response_solace)
   

    return jsonify(
        response_type='in_channel',
        text=f'Spiel startet zwischen Team_rot {team1} und Team_blau {team2}',
    )