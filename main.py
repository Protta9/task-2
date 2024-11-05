from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Body
from urllib.parse import parse_qs
import sqlite3

def database(data):
    con = sqlite3.connect("users.db")
    cur = con.cursor()

    cur.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER)
    ''')

    cur.execute('INSERT INTO Users (name, age) VALUES (?, ?)', (data['name'], data['age']))
    con.commit()

app = FastAPI()
 
@app.get("/index")
def read_root():
    html_content = """<button onclick="window.location.href='/add';">Добавить человека в список</button>"""
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
    print(data)

    database(data)