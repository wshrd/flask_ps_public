import subprocess
from flask import Flask, request, Response, render_template, jsonify, g, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '!#1q2w3e4r5t6y#!'
# для проверки аутентификации
def check_auth(username, password):
    return username == 'petrov' and password == '123456' or username == 'ivanov' and password == '654321'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Получаем данные из формы входа
        username = request.form['username']
        password = request.form['password']

        # Проверяем данные для входа
        if check_auth(username, password):
            # Если данные верны, сохраняем имя пользователя в сессии
            session['username'] = username
            # Перенаправляем пользователя на главную страницу
            return redirect(url_for('index'))
        else:
            # Если данные неверны, возвращаем сообщение об ошибке
            return 'Invalid username or password'
    else:
        # Если это запрос GET, просто отображаем форму входа
        return render_template('login.html')

@app.route('/')
def index():
    # Проверяем, вошел ли пользователь в систему
    if 'username' not in session:
        # Если нет, перенаправляем на страницу входа
        return redirect(url_for('login'))

    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    mailbox = request.form['mailbox']
    cmd = f'pwsh -Command "& /home/adm1n/py_scripts/flask_ps/static/exp_mbox.ps1 {mailbox}"'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        return f'An error occurred: {error.decode()}'
    else:
        return output.decode()
    
@app.route('/check', methods=['POST'])
def check():
    cmd = f'pwsh -Command "& /home/adm1n/py_scripts/flask_ps/static/exp_stat.ps1"'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        return f'An error occurred: {error.decode()}'
    else:
        return render_template('output.html', output=output.decode())
    
@app.route('/api/options', methods=['POST'])
def options():
    if request.is_json:
        options_list = request.get_json()
        response = jsonify(options_list)
        return response, 200
    else:
        return jsonify({"error": "Request body is not JSON"}), 400

@app.route('/logout', methods=['POST'])
def logout():
    # Удаляем данные пользователя из сессии
    session.pop('username', None)
    # Перенаправляем пользователя на страницу входа
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
