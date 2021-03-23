import psycopg2
import os
import sys
import time

class DB:
    def __init__(self):
        self._dbcon = None

    def __enter__(self):
        try:
            self._dbcon = psycopg2.connect(
                host=os.environ['PG_HOST'],
                user=os.environ['PG_USER'],
                password=os.environ['PG_PASSWORD'],
                database=os.environ['PG_DATABASE'],
                port=os.environ['PG_PORT']
            )
            self._cursor = self._dbcon.cursor()
            return self
        except:
            raise
    
    def __exit__(self, exc_type, exc_val, traceback):
        self._dbcon.close()

    def get_last_anecdotes(self, limit=5):
        query = "SELECT anecdotes FROM TRIVIA ORDER BY ID DESC LIMIT %s"
        self._cursor.execute(query, [limit])
        anecdotes = self._cursor.fetchall()
        anecdotes = [a[0] for a in anecdotes]
        return anecdotes
  