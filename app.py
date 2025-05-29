import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "SL Jujuy Tours Bot está activo en Heroku."

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_token = "SL_JUJUY_TOUR_VERIF"
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode and token:
            if mode == 'subscribe' and token == verify_token:
                return challenge, 200
            else:
                return 'Token inválido', 403

    elif request.method == 'POST':
        data = request.json

        # Reenvía todo lo recibido a Make
        requests.post(
            'https://hook.us2.make.com/pbg4flgenfwwomjdmxwvd2evpft9gke4',
            json=data
        )

        return 'EVENT_RECEIVED', 200

    return 'Método no permitido', 405

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
