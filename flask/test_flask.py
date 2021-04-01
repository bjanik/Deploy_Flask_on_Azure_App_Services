import flask
import pytest
import time

from contextlib import contextmanager
from flask import (
    request,
    template_rendered
)

from .app import app, submit
from .db import DB


@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

class ConnectionDBException(Exception):
    pass

class MockDB:
    def __enter__(self):
        self._connection_opened = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._connection_opened = False

    def set_fake_db(self, now):
        self._fakeDB = [
            ['anecdote1', now - 180],
            ['anecdote2', now - 180],
            ['anecdote3', now - 360],
            ['anecdote4', now - 360],
            ['anecdote5', now - 3600],
            ['anecdote6', now - 3600],
            ['anecdote7', now - 7200],
            ['anecdote8', now - 7200],
            ['anecdote9', now - 86400],
            ['anecdote10', now - 86400 * 10],
        ]

    def get_last_anecdotes(self, time_interval):
        if self._connection_opened is False:
            raise ConnectionDBException
        now = round(time.time())
        self.set_fake_db(now)
        interval = now - time_interval
        return [a[0] for a in self._fakeDB if a[1] >= interval]

def test_db_connection():
    with MockDB() as db:
        assert db._connection_opened is True
    assert db._connection_opened is False

def test_db_get_anecdotes():
    with MockDB() as db:
        
        # Get anecdotes recorded less than one minute ago
        anecdotes = db.get_last_anecdotes(60)
        assert anecdotes == []

        # Get anecdotes recorded less than one day ago
        anecdotes = db.get_last_anecdotes(86400)
        assert anecdotes == [a[0] for a in db._fakeDB[:-1]]

        # Get anecdotes recorded less than 6 hours ago
        anecdotes = db.get_last_anecdotes(3600 * 6)
        assert anecdotes == [a[0] for a in db._fakeDB[:-2]]
        assert len(anecdotes) == 8

        # Get anecdotes recorded less than a week ago
        anecdotes = db.get_last_anecdotes(86400 * 7)
        assert len(anecdotes) == 9

def test_db_connection_fails():
    # Exception raised because connection is down when trying to access to DB
    with MockDB() as db:
        db._connection_opened = False
    with pytest.raises(ConnectionDBException) as exc:
        anecdotes = db.get_last_anecdotes(3600)
    exc.type == ConnectionDBException

def test_home_route(mocker):
    with captured_templates(app) as templates:
        rv = app.test_client().get('/')
        assert rv.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'index.html'


def test_submit_route(mocker):
    with captured_templates(app) as templates:
        rv = app.test_client().post('/submit', data={'email': 'bart@gmail.com', 'time': '86400'})
        assert rv.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'feedback.html'