from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent
from dotenv import load_dotenv
import os

# 加載環境變數
load_dotenv()

# 從環境變數獲取 LINE 的 Channel Access Token 和 Channel Secret
LINE_ACCESS_TOKEN = os.getenv('LINE_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

if LINE_ACCESS_TOKEN is None or LINE_CHANNEL_SECRET is None:
    raise ValueError("LINE_ACCESS_TOKEN or LINE_CHANNEL_SECRET not set. Please check your environment variables.")

# 設定 LINE SDK
line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    # 驗證簽名是否正確
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 取得用戶發送的訊息
    user_message = event.message.text
    reply_message = f"Hello! 你說的是: {user_message}"
    
    # 回覆訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=reply_message)
    )

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))  # 默認端口
    app.run(host='0.0.0.0', port=port)
