from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)


line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

@app.route("/", methods=["GET"])
def home():
    return "OK"

@app.route("/callback", methods=["GET", "POST"])
def callback():

    if request.method == "POST":
        signature = request.headers.get("X-Line-Signature")
        body = request.get_data(as_text=True)
        try:
            handler.handle(body, signature)
        except Exception as e:
            print("Webhook error:", e)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"你輸入的是：{event.message.text}")
    )


