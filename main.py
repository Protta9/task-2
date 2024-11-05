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

def updatedb(data):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute('UPDATE Users SET name = ?, age = ? WHERE id = ?', (data['name'], data['age'], data['id']))
    conn.commit()

def deletedb(data):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute('DELETE FROM Users WHERE id = ?', (data['id']))
    conn.commit()

app = FastAPI()
 
@app.get("/index")
def read_root():
    html_content = """<button onclick="window.location.href='/add';">Добавить человека в список</button>
    <button onclick="window.location.href='/read';">Список людей</button>
    <button onclick="window.location.href='/update';">Изменить</button>
    <button onclick="window.location.href='/delete';">Удалить</button>"""
    return HTMLResponse(content=html_content)

@app.get('/add')
def add():
    html_content = """<button onclick="window.location.href='/index';">Обратно</button><br>
    <form action="/addapi" method="post">
        <label for="name">Имя:</label><br>
        <input type="text" id="name" name="name"><br>
        <label for="userage">Возраст:</label><br>
        <input type="number" id="age" name="age"><br><br>
        <input type="submit" value="Добавить">
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
<table border="1">
    <tr>
        <th>Id</th>
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

@app.get('/update')
def update():
    html_content = """<button onclick="window.location.href='/index';">Обратно</button><br>
    <form action="/updateapi" method="post">
        <label for="id">Айди:</label><br>
        <input type="text" id="id" name="id"><br>
        <label for="name">Имя:</label><br>
        <input type="text" id="name" name="name"><br>
        <label for="userage">Возраст:</label><br>
        <input type="number" id="age" name="age"><br><br>
        <input type="submit" value="Изменить">
    </form>"""
    return HTMLResponse(content=html_content)

@app.post('/updateapi')
def updateapi(data = Body()):
    data = parse_qs(data.decode('utf-8'))
    data = {key: value[0] for key, value in data.items()}

    updatedb(data)
    return HTMLResponse(content="""<button onclick="window.location.href='/index';">Обратно</button><br>Готово!""")

@app.get('/delete')
def delete():
    html_content = """<button onclick="window.location.href='/index';">Обратно</button><br>
    <form action="/deleteapi" method="post">
        <label for="id">Айди:</label><br>
        <input type="text" id="id" name="id"><br><br>
        <input type="submit" value="Удалить">
    </form>"""
    return HTMLResponse(content=html_content)

@app.post('/deleteapi')
def deleteapi(data = Body()):
    data = parse_qs(data.decode('utf-8'))
    data = {key: value[0] for key, value in data.items()}

    deletedb(data)
    return HTMLResponse(content="""<button onclick="window.location.href='/index';">Обратно</button><br>Готово!""")