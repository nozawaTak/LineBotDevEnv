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

line_bot_api = LineBotApi('6AcDr4HJnpA21YxGDX65w5PxyU4UAfFHzZzi84uogbsBmfjE0vKQQ8Iw5ICNdFk8FPff/iANOE1UpBhMHvWF4k4VUaupEcv4rBpi9zI4EYDM12RWxs2CO5Z8wXLP7rXKD2WVdwhR0e7hn1XIRXYSpQdB04t89/1O/w1cDnyilFU=')
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
        TextSendMessage(text=event.message.text+"plus Text"))


if __name__ == "__main__":
    app.run()