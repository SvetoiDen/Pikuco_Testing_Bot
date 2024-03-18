import mysql.connector as connect
from typing import Any

class BD_Bot():
    def __init__(self):
        self.mysql = connect.connect(
            host='81.31.246.83',
            user='gen_user',
            password='y8FfoHm>\:-EV5',
            database='default_db',
            port=3306
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