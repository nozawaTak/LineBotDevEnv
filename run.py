from flask import Flask, request, abort
import config

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

line_bot_api = LineBotApi(config.getAccessToken())
handler = WebhookHandler(config.getChannelSecret())


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
    echo(event)

def echo(event):
    multi_reply = [TextMessage(text=event.message.text), TextMessage(text=event.source.user_id)]
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(multi_reply))

def get_user_id(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.source.user_id))


def get_user_message(event):
    return event.message.text


if __name__ == "__main__":
    app.run()