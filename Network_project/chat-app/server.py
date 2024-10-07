# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.secret_key = "supersecretkey"
socketio = SocketIO(app)

# Ana sayfa yönlendirme
@app.route('/')
def home():
    session.pop('username', None)  # Oturum bilgisi varsa temizle
    return redirect(url_for("login"))

# Kullanıcı adı giriş ekranı
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('chat'))  # Giriş yaptıktan sonra sohbet ekranına yönlendir
    return render_template('login.html')

# Sohbet sayfası
@app.route('/chat')
def chat():
    if "username" in session:
        return render_template('index.html', username=session["username"])
    return redirect(url_for("login"))  # Oturum açılmadıysa tekrar giriş sayfasına yönlendir

# WebSocket üzerinden mesaj alıp gönderme
@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    print(f'{username} dedi ki: {message}')
    send(f'{username}: {message}', broadcast=True)  # Mesajı tüm istemcilere yayınla

if __name__ == '__main__':
    socketio.run(app, debug=True)
