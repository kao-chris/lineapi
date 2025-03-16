from flask import Flask, request, abort
from linebot.v3.messaging import MessagingApi, Configuration
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.v3.exceptions import InvalidSignatureError
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
app = Flask(__name__)

# 從環境變數獲取 LINE 的 Channel Access Token 和 Channel Secret
LINE_ACCESS_TOKEN = os.getenv('0yzpqMd2ecAgeXIpRni1NcHtGLhYdVGJ/DbegKTZ+YoTx9SMR5T2JX/1IWRl75hvNuySF6GorTFF+MY+FO7rQVHhZT4bz9fT8XsJZiEInYa9yRjhTnVFcxvYb3oavk0T0M1sh5mqTyTdXmnjou8iGAdB04t89/1O/w1cDnyilFU=')
LINE_CHANNEL_SECRET = os.getenv('32863e4522fb44c95d3c752734223067')

# 設定 LINE SDK 3.0+ 的 Configuration
config = Configuration(access_token=LINE_ACCESS_TOKEN)
line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    # 驗證簽名是否正確
    try:
        # 檢查是否為有效的事件
        events = line_bot_api.parse_events_from(body)
        for event in events:
            if isinstance(event, MessageEvent):
                handle_message(event)
    except InvalidSignatureError:
        abort(400)

    return "OK"

def handle_message(event):
    # 取得用戶發送的訊息
    user_message = event.message.text
    reply_message = f"Hello! 你說的是: {user_message}"
    
    # 回覆訊息
    line_bot_api.reply_message(
        event.reply_token,
        [TextMessage(text=reply_message)]
    )

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))  # 默認端口
    app.run(host='0.0.0.0', port=port)
