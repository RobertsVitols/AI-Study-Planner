import pytest
from app import app, db, History
from datetime import datetime

# Setup fixture for testing environment and database
@pytest.fixture(scope="module")
def client():
    """Setup a test client for Flask application."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_history.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Create the database tables for testing inside an application context
    with app.app_context():
        db.create_all()  # Create the database tables for testing
    
    # Provide the test client
    with app.test_client() as client:
        yield client

    # Clean up after tests by dropping all tables inside an application context
    with app.app_context():
        db.drop_all()


def test_generate_study_plan(client):
    """Test generating a study plan with valid input."""
    response = client.post("/", data={
        "syllabus": "Math, Physics, Chemistry",
        "deadlines": "2025-05-01, 2025-05-15, 2025-06-01",
        "available_time": 5
    })

    # Assert that the study plan is generated correctly
    assert response.status_code == 200
    assert b'Your Study Plan:' in response.data
    assert b'Math' in response.data  # Ensure the subjects are in the study plan

    # Check if the study plan is saved to the database
    with app.app_context():
        history_entry = History.query.first()
        assert history_entry is not None
        assert history_entry.syllabus == "Math, Physics, Chemistry"
        assert history_entry.deadlines == "2025-05-01, 2025-05-15, 2025-06-01"
        assert history_entry.available_time == 5
        assert history_entry.study_plan is not None


def test_empty_input(client):
    """Test the case when user inputs empty fields."""
    response = client.post("/", data={
        "syllabus": "",
        "deadlines": "",
        "available_time": ""
    })

    # Assert that the response contains an error message
    assert response.status_code == 200
    assert b'Please fill in all fields' in response.data


def test_incorrect_data_format(client):
    """Test the case when the deadlines are in an incorrect format."""
    response = client.post("/", data={
        "syllabus": "Math, Physics",
        "deadlines": "invalid-date-format",
        "available_time": 5
    })

    # Check that an error message is shown for incorrect date format
    assert response.status_code == 200
    assert b'Error in deadlines format' in response.data


def test_history_section(client):
    """Test that history can be toggled correctly."""
    # Create some history entries manually for the test
    new_entry = History(
        syllabus="Biology, Chemistry",
        deadlines="2025-06-15, 2025-07-01",
        available_time=4,
        study_plan="Study plan generated for Biology and Chemistry",
        timestamp=datetime(2025, 3, 24, 14, 30, 0)
    )
    with app.app_context():
        db.session.add(new_entry)
        db.session.commit()

    # Make a GET request to load the page and check if history is displayed
    response = client.get("/")
    assert response.status_code == 200
    assert b"History" in response.data
    assert b"Biology, Chemistry" in response.data


def test_empty_ai_response(client, monkeypatch):
    """Test the scenario where the AI returns an empty response."""
    def mock_generate_study_plan(syllabus, deadlines, available_time):
        return ""  # Simulating an empty AI response

    # Only patch for this test to avoid global side effects
    monkeypatch.setattr("app.generate_study_plan", mock_generate_study_plan)

    # Make a valid POST request
    response = client.post("/", data={
        "syllabus": "Math, Physics",
        "deadlines": "2025-05-01, 2025-05-15",
        "available_time": 5
    })

    # Check that the AI response is empty
    assert response.status_code == 200
    assert b'Error: AI response was empty' in response.data


def test_sqlite_database(client):
    """Test that the database properly stores and retrieves data."""
    with app.app_context():
        db.session.query(History).delete()
        db.session.commit()
    # Add a new entry to the database
    new_entry = History(
        syllabus="Math, Physics",
        deadlines="2025-05-01, 2025-05-15",
        available_time=5,
        study_plan="Study plan generated for Math and Physics"
    )
    with app.app_context():
        db.session.add(new_entry)
        db.session.commit()

    # Check that the entry is saved correctly
    with app.app_context():
        history_entry = History.query.first()
        assert history_entry.syllabus == "Math, Physics"
        assert history_entry.deadlines == "2025-05-01, 2025-05-15"
        assert history_entry.study_plan == "Study plan generated for Math and Physics"
        assert history_entry.timestamp is not None


if __name__ == "__main__":
    pytest.main()
