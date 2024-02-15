from flask import Flask, request
import telebot

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram Bot token
bot_token = "6702864472:AAEONifUZKck1AYDE7lX-_F9JPJIHKix1Ck"
bot = telebot.TeleBot(bot_token)

# Initialize Flask app
app = Flask(__name__)

# Define the route for setting webhook using GET method
@app.route('/', methods=['GET'])
def index():
    return '''
    <h1>Welcome to my Telegram Bot</h1>
    <p>This is a simple Flask app to handle a Telegram bot webhook.</p>
    <p>You can set the webhook <a href="/webhook">here</a>.</p>
    '''

# Define the route for setting webhook using GET method
@app.route('/webhook', methods=['GET'])
def set_webhook():
    global webhook_url
    webhook_url = f"{request.url}"
    if webhook_url:
        bot.remove_webhook()  # Remove any existing webhook
        bot.set_webhook(url=webhook_url)
        return f'Webhook URL: {webhook_url} has been set successfully!<br><br><a href="/">Go back to home</a>', 200
    

# Define the route for Telegram webhook using POST method
@app.route('/webhook', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

# Handle /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, f"Welcome! You can set the webhook by sending a GET request to /setwebhook with your desired URL.")

# Handle all other messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "I received your message.")

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
