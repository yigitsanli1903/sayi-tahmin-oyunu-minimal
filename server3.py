from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

secret_number = random.randint(1, 100)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('guess')
def handle_guess(guess):
    global secret_number
    try:
        guess = int(guess)
    except ValueError:
        emit('message', "⚠️ Geçerli bir sayı girin!")
        return

    if guess == secret_number:
        emit('message', f"🎉 Doğru tahmin! Sayı {secret_number} idi!")
        secret_number = random.randint(1, 100)
    elif guess < secret_number:
        emit('message', "🔼 Daha büyük bir sayı girin!")
    else:
        emit('message', "🔽 Daha küçük bir sayı girin!")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
