from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',  
        user='root',       
        password='root', 
        database='To_do' 
    )

app = Flask(__name__, template_folder="templates", static_folder="statics")
app.secret_key = 'secret_key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        usr = request.form['usr']
        pwd = request.form['pwd']
        pwd2 = request.form['pwd2']
        
        if pwd != pwd2:
            return render_template("register.html", message="Passwords don't match")
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                query = f"INSERT INTO users (username, name, password) VALUES ('{usr}', '{name}','{pwd}')"
                cursor.execute(query)
                conn.commit()
                conn.close()
                return render_template("register.html", message="Registered successfully!")
            except mysql.connector.IntegrityError:
                return render_template("register.html", message="Username already exists")
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        usr = request.form['usr']
        pwd = request.form['pwd']
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = f"SELECT id, username, password FROM users WHERE password = '{pwd}' AND username = '{usr}'"
            cursor.execute(query)
            user = cursor.fetchone()
            user_id = user[0]
            if user:
                conn.close()
                session['user_id'] = user_id
                return redirect(url_for('main')) 
            
        except Exception as e:
            conn.close()
            return render_template('login.html', message = "Wrong username or password")
        

    return render_template('login.html')

@app.route('/main', methods=['GET','POST'])
def main():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM tasks WHERE user_id = '{user_id}'")
    tasks = cursor.fetchall()  
    
    conn.close()
    return render_template('main.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    title = request.form['title']
    description = request.form.get('description', '')
    user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (user_id, title, description) VALUES (%s, %s, %s)", 
                   (user_id, title, description))
    conn.commit()
    conn.close()
    
    return redirect(url_for('main'))

@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE tasks SET completed = NOT completed WHERE id = '{task_id}'")

    conn.commit()
    conn.close()
    
    return redirect(url_for('main')) 

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login')) 
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM tasks WHERE id = '{task_id}'")
    conn.commit()
    conn.close()
    
    return redirect(url_for('main')) 



    

if __name__ == '__main__':
    app.run(debug=True)
