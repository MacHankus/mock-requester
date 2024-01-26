from starlette_testclient import TestClient

from app import app

client = TestClient(app)
