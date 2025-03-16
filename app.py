from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 環境變數
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("0yzpqMd2ecAgeXIpRni1NcHtGLhYdVGJ/DbegKTZ+YoTx9SMR5T2JX/1IWRl75hvNuySF6GorTFF+MY+FO7rQVHhZT4bz9fT8XsJZiEInYa9yRjhTnVFcxvYb3oavk0T0M1sh5mqTyTdXmnjou8iGAdB04t89/1O/w1cDnyilFU=")
LINE_CHANNEL_SECRET = os.getenv("32863e4522fb44c95d3c752734223067")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/")
def home():
    return "LINE Bot is running"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text
    reply_msg = f"你說了: {user_msg}"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_msg))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
