import mysql.connector as connect
from typing import Any

class BD_Bot():
    def __init__(self):
        self.mysql = connect.connect(
            host='host',
            user='user',
            password='password',
            database='database',
        )
        self.cursor = self.mysql.cursor(dictionary=True, buffered=True)

    def commit_(self, execute: str):
        self.cursor.execute(execute)
        self.mysql.commit()

    def get_(self, execute: str) -> Any:
        self.cursor.execute(execute)
        return self.cursor.fetchone()

    def gets_(self, execute: str) -> Any:
        self.cursor.execute(execute)
        return self.cursor.fetchall()

    def close_(self):
        self.mysql.close()
