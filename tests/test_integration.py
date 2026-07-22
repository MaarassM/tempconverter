import os

# app.py cita env varijable pri importu, pa ih moramo postaviti PRIJE importa
os.environ.setdefault("STUDENT", "Test Student")
os.environ.setdefault("COLLEGE", "Test College")

import pytest
from app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # bez CSRF tokena u testu
    with app.app_context():
        db.create_all()
    with app.test_client() as c:
        yield c


def test_index_shows_student_and_college(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Test Student" in resp.data
    assert b"Test College" in resp.data


def test_conversion_is_stored(client):
    resp = client.post("/", data={"celsius": "100"}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"212" in resp.data
