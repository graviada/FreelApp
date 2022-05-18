from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'

DB_HOST = "localhost"
DB_NAME = "freelance_app"
DB_USER = "postgres"
DB_PASS = "1234"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route('/')
def home():
    if 'logged_in' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor.execute('SELECT * FROM user_pers_acc WHERE user_login = %s', (username,))
        account = cursor.fetchone()
        cursor.execute('END TRANSACTION;')

        if account:
            password_rs = account['user_password']

            if password_rs == password:
                session['logged_in'] = True
                session['id'] = account['user_id']
                session['username'] = account['user_login']
                return redirect(url_for('home'))
            else:
                flash('Неверный логин/пароль')
        else:
            flash('Неверный логин/пароль')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if 'logged_in' in session:
        cursor.execute('SELECT * FROM user_pers_acc WHERE user_id = %s', [session['id']])
        account = cursor.fetchone()
        cursor.execute('END TRANSACTION;')
        cursor.execute('SELECT * FROM key_access WHERE user_id = %s', [session['id']])
        access = cursor.fetchall()
        print(access)
        return render_template('profile.html', account=account, access=access)
    return redirect(url_for('login'))


@app.route('/search', methods=['POST', 'GET'])
def search():
    return render_template('search.html')


# Documents
@app.route('/documents')
def doc_Read():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute('SELECT * FROM doc_download')
    docs = cursor.fetchall()
    cursor.execute('END TRANSACTION;')
    return render_template('documents.html', docs=docs)


@app.route('/documents/add', methods=['POST', 'GET'])
def doc_Add():
    return render_template('doc_add.html')


@app.route('/documents/create', methods=['POST'])
def doc_Create():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        task_id = request.form["task_id"]
        doc_name = request.form["doc_name"]
        doc_extension = request.form["doc_extension"]
        active_link = request.form["active_link"]
        download_date = request.form["download_date"]

        cur.execute("""INSERT INTO doc_download (task_id, doc_name, doc_extension, active_link, download_date)
         VALUES (%s, %s, %s, %s, %s)""", (task_id, doc_name, doc_extension, active_link, download_date))
        cur.execute('END TRANSACTION;')

        conn.commit()
        # flash('Документ добавлен в каталог')

        return redirect(url_for('doc_Read'))


@app.route('/documents/edit/<int:doc_id>', methods=['POST', 'GET'])
def doc_Edit(doc_id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT * FROM doc_download WHERE doc_id = %s', (doc_id, ))
    data = cur.fetchall()
    cur.execute('END TRANSACTION;')
    cur.close()
    # print(data[0])
    return render_template('doc_edit.html', doc=data[0])


@app.route('/documents/update/<int:doc_id>', methods=['POST'])
def doc_Update(doc_id):
    if request.method == 'POST':
        task_id = request.form["task_id"]
        doc_name = request.form["doc_name"]
        doc_extension = request.form["doc_extension"]
        active_link = request.form["active_link"]
        download_date = request.form["download_date"]

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute("""UPDATE doc_download SET task_id = %s, 
        doc_name = %s, doc_extension = %s, 
        active_link = %s, download_date = %s 
        WHERE doc_id = %s""", (task_id, doc_name, doc_extension, active_link, download_date, str(doc_id)))
        cur.execute('END TRANSACTION;')

        # flash('Документ изменен')
        conn.commit()
        return redirect(url_for('doc_Read'))


@app.route("/docDelete/<int:doc_id>")
def doc_Delete(doc_id):
    # create delete query as string
    strSQL = "DELETE FROM doc_download WHERE doc_id=" + str(doc_id)

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(strSQL)
    conn.commit()
    # flash('Запись успешно удалена')
    return redirect(url_for('doc_Read'))


# Tasks
@app.route('/tasks')
def task_Read():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute('SELECT * FROM task_info')
    tasks = cursor.fetchall()
    cursor.execute('END TRANSACTION;')
    return render_template('tasks.html', tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)
