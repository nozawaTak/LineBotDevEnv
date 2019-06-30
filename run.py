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
    doList = ["ECHO", "USERID"]
    reply = makeReply(event, doList)
    line_bot_api.reply_message(
        event.reply_token,
        reply)


def makeReply(event, doList):
    reply = []
    for do in doList:
        if do == "ECHO":
            print(getUserMessage(event))
            reply.append(TextSendMessage(text=getUserMessage(event)))
        elif do == "USERID":
            reply.append(TextSendMessage(text=getUserId(event)))
    return reply


def getUserMessage(event):
    return event.message.text

def getUserId(event):
    return event.source.user_id

if __name__ == "__main__":
    app.run()