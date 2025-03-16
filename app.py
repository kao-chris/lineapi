from flask import Flask, request, abort
from linebot.v3.messaging import MessagingApi, Configuration
from linebot.v3.webhooks import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.models import ReplyMessageRequest, TextMessage

app = Flask(__name__)

# 設定你的 LINE API Token & Secret
LINE_ACCESS_TOKEN = "你的 LINE Channel Access Token"
LINE_CHANNEL_SECRET = "你的 LINE Channel Secret"

# 設定 LINE SDK 3.0+ 的 Configuration
config = Configuration(access_token=LINE_ACCESS_TOKEN)
line_bot_api = MessagingApi(configuration=config)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return "OK"

@handler.add("message")
def handle_message(event):
    if event.message.type == "text":
        user_message = event.message.text
        reply_message = f"Hello! 你說的是: {user_message}"
        
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )

if __name__ == "__main__":
    app.run(port=5000, debug=True)
