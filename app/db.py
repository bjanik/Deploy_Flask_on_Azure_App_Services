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
        self._dbcon = None

    def create_table(self):
        self._cursor.execute("CREATE TABLE IF NOT EXISTS TRIVIA (\
                                ID SERIAL,\
                                anecdotes varchar(1024),\
                                recording_time int,\
                                UNIQUE (anecdotes))")
        self._dbcon.commit()

    def add_entry_to_trivia(self, anecdote, time):
        try:
            self._cursor.execute("""INSERT INTO TRIVIA (anecdotes, recording_time) VALUES (%s, %s)""", [anecdote, time])
            self._dbcon.commit()
        except psycopg2.errors.UniqueViolation as e:
            pass
  