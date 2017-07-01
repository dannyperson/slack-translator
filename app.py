from requests_toolbelt.adapters import appengine

appengine.monkeypatch()
import os

from flask import Flask, request
import requests

def make_app(env):
    app = Flask(__name__)
    app.debug = 'DEBUG' in os.environ
    return app

app = make_app(os.environ)

def translate(text, from_, to):
    return requests.get(
        'https://www.googleapis.com/language/translate/v2',
        params=dict(
            format='text',
            key=os.environ['GOOGLE_API_KEY'],
            q=text,
            source=from_, target=to
        ),
	timeout=5
    ).json()['data']['translations'][0]['translatedText']


def get_user(user_id):
    return requests.get(
        'https://slack.com/api/users.info',
        params=dict(
            token=os.environ['SLACK_API_TOKEN'],
            user=user_id
        ),
	timeout=5
    ).json()['user']


def translate_and_send(user_id, user_name, channel_name, text, from_, to):
    translated = translate(text, from_, to)
    user = get_user(user_id)

    for txt in (text, translated):
        response = requests.post(
            os.environ['SLACK_WEBHOOK_URL'],
            json={
                "username": user_name,
                "text": txt,
                "mrkdwn": True,
                "parse": "full",
                "channel": '#'+channel_name,
                "icon_url": user['profile']['image_72']
            },
	    timeout=5
        )
    return response.text


@app.route('/<string:from_>/<string:to>', methods=['GET', 'POST'])
def index(from_, to):
    translate_and_send(
        request.values.get('user_id'),
        request.values.get('user_name'),
        request.values.get('channel_name'),
        request.values.get('text'),
        from_,
        to
    )
    return ('', 200)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
