import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="127.0.0.1",   # IP del master o del balanceador
            user="root",
            password="root",
            database="taskdb",
            port=3307
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def fetch(self):
        self.cursor.execute("SELECT * FROM tasks ORDER BY id")
        return self.cursor.fetchall()

    def insert(self, titulo, descripcion, estado):
        sql = "INSERT INTO tasks (titulo, descripcion, estado) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (titulo, descripcion, estado))
        self.conn.commit()

    def update(self, id, titulo, descripcion, estado):
        sql = "UPDATE tasks SET titulo=%s, descripcion=%s, estado=%s WHERE id=%s"
        self.cursor.execute(sql, (titulo, descripcion, estado, id))
        self.conn.commit()

    def delete(self, id):
        sql = "DELETE FROM tasks WHERE id=%s"
        self.cursor.execute(sql, (id,))
        self.conn.commit()
