from flask import Flask, request
import requests
import nltk
from nltk.chat.util import Chat, reflections

app = Flask(__name__)

# Twilio API URL for sending messages
TWILIO_SEND_MESSAGE_URL = "https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages"

# Twilio API credentials
TWILIO_ACCOUNT_SID = "YOUR_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "+1XXXYYYYYYY"

# NLTK chatbot pairs
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How are you today?"]
    ],
    
    [
        r"hi|hey|hello",
        ["Hello", "Hey there"]
    ],
    
    [
        r"what is your name ?",
        ["I am a chatbot created with NLTK and Flask"]
    ],
    
    [
        r"how are you ?",
        ["I am doing good", "I am fabulous"]
    ],
    
    [
        r"sorry (.*)",
        ["Its alright", "Its OK, never mind"]
    ],
    
    [
        r"i am fine",
        ["Great to hear that", "Awesome, glad to hear that"]
    ],
    
    [
        r"quit",
        ["Bye bye take care. See you soon :) "]
    ]
]

# NLTK chatbot instance
chatbot = Chat(pairs, reflections)

# Flask route for incoming WhatsApp messages
@app.route("/whatsapp", methods=["POST"])
def incoming_whatsapp_message():
    # Retrieve incoming message data
    message_data = request.values

    # Extract message text
    incoming_message_text = message_data.get("Body", "")
    
    # Use the NLTK chatbot to generate a response
    response = chatbot.respond(incoming_message_text)

    # Send the response back to the sender via Twilio API
    send_message(response, message_data.get("From"))
    
    return "", 200

# Function to send message via Twilio API
def send_message(message_body, to_number):
    message_data = {
        "To": to_number,
        "From": TWILIO_PHONE_NUMBER,
        "Body": message_body
    }
    
    response = requests.post(
        TWILIO_SEND_MESSAGE_URL.format(account_sid=TWILIO_ACCOUNT_SID),
        auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
        data=message_data
    )
    
    if response.status_code != 201:
        print("Failed to send message: {}".format(response.text))

if __name__ == "__

