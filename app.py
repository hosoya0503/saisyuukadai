from flask import Flask, render_template, request, redirect, url_for, session
import db, bookdb, string, random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    
    if msg == None:
        return render_template('index.html')
    else:
        return render_template('index.html', msg=msg)

@app.route('/list')
def books_list():
    # books_list = [
    #     (default, 'よく分かるPython', '佐々木 磨生', 'MCL出版', 1),
    #     (default, 'LinuC 詳解', '細川 潤哉', 'MCL出版', 2),
    #     (default, 'Servlet 入門', '高橋 洋平', 'ジョビ出版', 3),
    #     (default, 'Flask 入門', '高橋 洋平', 'ジョビ出版', 4),
    #     (default, 'よく分かるUML', '細川 潤哉', 'MCL出版', 5),
    #     (default, 'Django 入門', '佐々木 磨生', '龍澤出版', 6),
    #     (default, '今から始める仮想通過', '高橋 洋平', '龍澤出版', 7),
    #     (default, 'heroku 入門', '細川 潤哉', 'MCL出版', 8),
    # ]
    books_list = bookdb.select_all_books()
    return render_template('books_list.html', books=books_list)

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('text')
    if keyword:
        results = db.search_books(keyword)
        return render_template('search_results.html', results=results)
    else:
        return redirect(url_for('mypage'))

@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')

    if db.login(user_name, password):
        session['user'] = True
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        return redirect(url_for('mypage'))
    else :
        error = 'ログインに失敗しました。'
        input_data = {
            'user_name': user_name,
            'password': password
        }
        return render_template('index.html', error=error, data=input_data)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html')
    else:
        return redirect(url_for('index'))


@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    password = request.form.get('password')
    
    if user_name == '':
        error = 'ユーザ名が未入力です。'
        return render_template('register.html', error=error)
    
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register.html', error=error)
    
    count = db.insert_user(user_name, password)
    
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error='登録に失敗しました。'
        return render_template('register.html',error=error)

if __name__ == '__main__':
    app.run(debug=True)
    
