from flask import Flask, render_template, redirect, url_for, request, session, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import Extensions.title_calculation

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Use an absolute path for the database file
DATABASE = os.path.join(app.root_path, 'users.db')

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            score TEXT NOT NULL,
            totalQuestionsAnswered TEXT NOT NULL,
            totalQuestions TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('phishing_gamified.html', username=session['username'], )
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' in session:
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (session['username'],))
        user = cur.fetchone()
        
        totalQuestionsAnswered = float(user[7])
        totalQuestions = int(user[8])
        
        setTitle = Extensions.title_calculation.title(totalQuestions, totalQuestionsAnswered)
        
        cur.execute('UPDATE users SET title = ? WHERE username = ?', (setTitle, session['username']))
        conn.commit()
        conn.close()
        
        
        return render_template('profile.html', user=user)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect(url_for('phishing_gamified'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        score = 0.0
        title = " "
        totalQuestionsAnswered = 0
        totalQuestions = 0
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password, email, name, title, score, totalQuestionsAnswered, totalQuestions) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (username, hashed_password, email, name, title, score, totalQuestionsAnswered, totalQuestions))
            conn.commit()
            flash('Registration successful, please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError as e:
            flash('Username already exists', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/phishing_gamified', methods=['GET', 'POST'])
def phishing_gamified():
    if 'username' in session:
        if request.method == 'POST':
            new_score = float(request.form['score'])
            new_totalQuestionsAnswered = int(request.form['totalQuestionsAnswered'])
            totalQuestions = int(request.form['totalQuestions'])
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            # Retrieve the current score and totalQuestionsAnswered from the database
            c.execute('SELECT score, totalQuestionsAnswered FROM users WHERE username = ?', (session['username'],))
            current_score, current_totalQuestionsAnswered = c.fetchone()
            # Add the new values to the current values
            updated_score = float(current_score) + new_score
            updated_totalQuestionsAnswered = int(current_totalQuestionsAnswered) + new_totalQuestionsAnswered
            # Update the database with the new totals
            c.execute('UPDATE users SET score = ?, totalQuestionsAnswered = ?, totalQuestions = ? WHERE username = ?', (updated_score, updated_totalQuestionsAnswered, totalQuestions, session['username']))
            conn.commit()
            conn.close()
            return redirect(url_for('leaderboard'))
        return render_template('phishing_gamified.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/leaderboard')
def leaderboard():
    if 'username' in session:
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute('SELECT username, score, title, totalQuestionsAnswered, totalQuestions FROM users ORDER BY score DESC')
        leaderboard_data = cur.fetchall()
        conn.close()

        # Creating a rank list for the leaderboard
        ranked_leaderboard = [{'rank': i+1, 'username': row[0], 'points': row[1], 'title': row[2], 'totalQuestionsAnswered': row[3], 'totalQuestions': row[4]} for i, row in enumerate(leaderboard_data)]

        return render_template('leaderboard.html', username=session['username'], leaderboard=ranked_leaderboard)
    return redirect(url_for('login'))


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(port=5000)