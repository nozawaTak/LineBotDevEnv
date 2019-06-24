from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('FePtkG7zKRo1Ln6EetEhTlokYX++0Cda52bbe91/SK11Y09EeYNUxLmSGKJgQVF5FPff/iANOE1UpBhMHvWF4k4VUaupEcv4rBpi9zI4EYCEMZ1l7EJmXAJ0M+sKebGf38Uav3Biipend0ZSGmxYHAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('cd4e2c8ca25810a3f250df277ee6527f')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()