from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
import re
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

import telebot
from telebot import types
from telebot.types import InlineKeyboardButton
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
telebot_token = config.get('data', 'telebot_token')
cod = config.get('data', 'cod')
chat_id1 = config.get('data', 'chat_id1')
chat_id2 = config.get('data', 'chat_id2')
secret_key = config.get('data', 'secret_key')

app = Flask(__name__)
app.secret_key = secret_key
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):

    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    con = sqlite3.connect('base.db')
    cur = con.cursor()
    cur.execute("SELECT user_name FROM users WHERE user_name = ?", (username,))
    user = cur.fetchone()
    con.close()

    if user:
        return User(username)
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        if re.fullmatch(r'.+@.+\..+', email):
            con = sqlite3.connect('base.db')
            cur = con.cursor()
            cur.execute(f"""SELECT * FROM visitors WHERE email = '{email}'""")
            if cur.fetchone() != None:
                error = "Такой email уже присутствует"
                flash(error, 'danger')
                return redirect('/')
            else:
                cur.execute(f"""INSERT INTO visitors(name, email, message)
                VALUES('{name}','{email}','{message}')""")
                con.commit()
                con.close()
                try:
                    bot = telebot.TeleBot(telebot_token)
                    bot.send_message(chat_id1, f'Гости {name} присоединились к нашей свадьбе \n И оставили сообщение: \n {message}')
                    bot.send_message(chat_id2,f'Гости {name} присоединились к нашей свадьбе \n И оставили сообщение: \n {message}')
                except:...
        else:
            error = "Введите корректный email"
            flash(error, 'danger')
            return redirect('/')
        return redirect('/thanks')
    return render_template('index.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        email = request.form['email']
        cod = request.form['cod']

        if cod == '':
            con = sqlite3.connect('base.db')
            cur = con.cursor()
            cur.execute(f"""DELETE FROM visitors WHERE email='{email}'""")
            con.commit()
            con.close()
            return redirect(url_for("admin"))

    con = sqlite3.connect('base.db')
    cur = con.cursor()
    cur.execute("""SELECT * FROM visitors""")
    visitors = cur.fetchall()
    amount = len(visitors)
    return render_template('admin.html', visitors = visitors, amount = amount)

@app.route("/login", methods=["GET", "POST"])
def login():
    con = sqlite3.connect('base.db')
    cur = con.cursor()
    cur.execute("""SELECT user_name, password FROM users""")
    users = cur.fetchall()[0]
    my_user = users[0]
    my_password = users[1]

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == my_user and my_password == password:
            user = User(username)
            login_user(user)  # Авторизуем пользователя
            flash("Вы успешно вошли!", "success")
            return redirect(url_for("admin"))
        else:
            flash("Неверный логин или пароль", "danger")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "info")
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    'app.run(debug=True)'
