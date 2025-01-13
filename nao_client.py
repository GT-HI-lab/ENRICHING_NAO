import websocket
from naoqi import ALProxy
import speech_recognition as sr

# NAOqi Proxies need to get this going via python 2.7
tts = ALProxy("ALTextToSpeech", "<NAO_IP>", 9559)
animated_speech = ALProxy("ALAnimatedSpeech", "<NAO_IP>", 9559)

# WebSocket Client Callbacks
def on_message(ws, message):
    print(f"LLM Response: {message}")
    # animated_response(message)

def on_error(ws, error):
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed")

def on_open(ws):
    print("Connected to WebSocket Server")
    # Capture speech and send it to the server
    user_input = listen_to_user()
    if user_input:
        ws.send(user_input)

# Speech-to-Text Function
def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except Exception as e:
            print(f"Error during speech recognition: {e}")
            return None

# Animated Speech Function
'''
def animated_response(text):
    config = {"bodyLanguageMode": "contextual"}
    animated_speech.say(text, config)
'''

# WebSocket Connection
ws = websocket.WebSocketApp("ws://<SERVER_IP>:8765",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.on_open = on_open
ws.run_forever()
