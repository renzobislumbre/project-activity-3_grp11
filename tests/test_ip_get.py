# test_ip_get.py
import pytest
from ip_get import app  # Import your Flask app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test the index route."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Utility Dashboard' in rv.data

def test_get_ip_info(client):
    """Test the /get_ip_info route."""
    rv = client.get('/get_ip_info')
    assert rv.status_code == 200
    assert b'ipv4' in rv.data  # Expecting "ipv4" in the JSON response

def test_check_speed(client):
    """Test the /check_speed route."""
    rv = client.get('/check_speed')
    assert rv.status_code == 200
    assert b'download_speed' in rv.data  # Expecting "download_speed" in the JSON response

def test_get_datetime(client):
    """Test the /get_datetime route."""
    rv = client.get('/get_datetime')
    assert rv.status_code == 200
    assert b'datetime' in rv.data  # Expecting "datetime" in the JSON response
