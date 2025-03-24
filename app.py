from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os
import markdown
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'  # Use SQLite or MySQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your_secret_key')  # Set secret key for flash messages
db = SQLAlchemy(app)

# Database model
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    syllabus = db.Column(db.Text, nullable=False)
    deadlines = db.Column(db.Text, nullable=False)
    available_time = db.Column(db.Integer, nullable=False)
    study_plan = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Function to generate the study plan
def generate_study_plan(syllabus, deadlines, available_time):
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    prompt = f"""
    I am a student. I need to create a personalized study plan. 
    My syllabus includes the following subjects: {syllabus}.
    I have the following deadlines: {deadlines}.
    I can study for {available_time} hours per day.
    Today's date and time is: {today}.
    Please format the response using Markdown for easy readability.
    Do not generate tables in your response.
    Please generate a study plan that helps me prepare for my exams based on these details.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7
    )

    

    try:
        message_content = response.choices[0].message.content.strip()
        if not message_content:  # Ja AI neatgriež atbildi
            return None
        return markdown.markdown(message_content).strip()
    except (KeyError, AttributeError):
        return None  # Kļūdas gadījumā atgriež `None`

@app.route("/", methods=["GET", "POST"])
def index():
    study_plan = None
    if request.method == "POST":
        syllabus = request.form["syllabus"]
        deadlines = request.form["deadlines"]
        available_time = request.form["available_time"]

        # Check for empty fields
        if not syllabus or not deadlines or not available_time:
            flash("Please fill in all fields", "error")
            return render_template("index.html", study_plan=study_plan)

        # Validate the deadlines format
        try:
            # Convert deadlines to list of datetime objects
            deadlines = [datetime.strptime(date.strip(), "%Y-%m-%d") for date in deadlines.split(",")]
            
            # Serialize deadlines to a comma-separated string
            deadlines_str = ", ".join([date.strftime('%Y-%m-%d') for date in deadlines])
        except ValueError:
            flash("Error in deadlines format", "error")
            return render_template("index.html", study_plan=study_plan)

        # Generate study plan
        study_plan = generate_study_plan(syllabus, deadlines, available_time)

        if not study_plan:
            flash("Error: AI response was empty", "error")
            return render_template("index.html", study_plan=None)

        # Save to database with serialized deadlines string
        new_entry = History(
            syllabus=syllabus,
            deadlines=deadlines_str,  # Save as string
            available_time=available_time,
            study_plan=study_plan
        )
        db.session.add(new_entry)
        db.session.commit()

        # Fetch updated history
        history = History.query.order_by(History.timestamp.desc()).all()
        return render_template("index.html", study_plan=study_plan, history=history)

    # Fetch history for GET requests
    history = History.query.order_by(History.timestamp.desc()).all()
    return render_template("index.html", study_plan=None, history=history)

if __name__ == "__main__":
    app.run(debug=True)
