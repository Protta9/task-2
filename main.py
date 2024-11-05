from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Body
from urllib.parse import parse_qs
import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()

cur.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER)
        ''')

def adddb(data):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute('INSERT INTO Users (name, age) VALUES (?, ?)', (data['name'], data['age']))
    conn.commit()

def readdb():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute('SELECT * FROM Users')
    return cur.fetchall()

app = FastAPI()
 
@app.get("/index")
def read_root():
    html_content = """<button onclick="window.location.href='/add';">Добавить человека в список</button>
    <button onclick="window.location.href='/read';">Список людей</button>"""
    return HTMLResponse(content=html_content)

@app.get('/add')
def add():
    html_content = """
    <form action="/addapi" method="post">
        <label for="name">Имя:</label><br>
        <input type="text" id="name" name="name"><br>
        <label for="userage">Возраст:</label><br>
        <input type="number" id="age" name="age"><br><br>
        <input type="submit" value="Отправить">
    </form>"""
    return HTMLResponse(content=html_content)

@app.post('/addapi')
def addapi(data = Body()):
    data = parse_qs(data.decode('utf-8'))
    data = {key: value[0] for key, value in data.items()}
    adddb(data)
    return HTMLResponse(content="""<button onclick="window.location.href='/index';">Обратно</button><br>
    Готово!""")

@app.get('/read')
def read():
    users = readdb()
    print(users)
    html_content = """<button onclick="window.location.href='/index';">Обратно</button><br>
<table>
    <tr>
        <th>Номер</th>
        <th>Имя</th>
        <th>Количество лет</th>
    </tr>
    """
    for i in range(len(users)):
        html_content = html_content + f"""
        <tr>
        <td>{users[i][0]}</td>
        <td>{users[i][1]}</td>
        <td>{users[i][2]}</td>
        </tr>
        """
    return HTMLResponse(content= html_content+'</table>')