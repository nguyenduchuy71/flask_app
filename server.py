import os
import json
import smtplib, ssl
from flask import Flask, request 
from celery_utils import get_celery_app_instance
from settings import SENDER_EMAIL, SMTP_SERVER, SMTP_PORT, EMAIL_PASSWORD

app = Flask(__name__)
celery = get_celery_app_instance(app)

@celery.task
def send_mail_celery(data):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host=SMTP_SERVER, port=SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, data['receiver_email'], data['message'])


@app.route('/', methods = ['GET'])
def index():
    return '<b>This is RPC service for sending mail!</b>'
 
@app.route('/send_mail', methods = ['GET', 'POST'])
def send_mail():
    if request.method == 'POST':
        try:
            data = request.data.decode('utf-8')
            send_mail_celery.delay(json.loads(data))
            return {'status_code': 200}
        except Exception as e:
            return {'status_code': 400}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5555))
    app.run(debug=True, host='0.0.0.0', port=port)
