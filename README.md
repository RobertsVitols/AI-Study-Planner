# 🧠 AI Study Planner

AI Study Planner is a Flask-based web application that uses OpenAI's GPT model to generate personalized study plans based on a student's syllabus, deadlines, and daily availability. Designed for simplicity and utility, the app helps students stay organized and study smarter.

---

## 🌟 Features

- Input your syllabus, exam deadlines, and available study time per day
- Get a tailored study plan using GPT-4o-mini
- Clean and responsive UI with Bootstrap
- Markdown-generated output rendered in HTML
- Plans to store and view past plans (History) using MySQL

---

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-study-planner.git
cd ai-study-planner
```

### 2. Install Dependencies

Install all required Python libraries using pip:
```bash
pip install -r requirements.txt
```
### 3. Set Up Environment Variables

Create a .env file in the root directory of the project and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```
✅ Make sure the .env file is in the same directory as app.py.
### 4. Run the App

Start the Flask development server using:
```bash
python app.py
```
Once running, open your browser and visit:
```bash
http://127.0.0.1:5000
```

## 🖼 Screenshots
Will be added later...  

## 📚 Libraries Used
- Flask – Web framework
- OpenAI – GPT language model interaction
- python-dotenv – For loading environment variables
- markdown – For rendering markdown response to HTML
- Bootstrap 5 – Frontend styling and layout

## 🏗 Architecture Diagram
Will be added later...  

## 🧪 Test Cases Overview

This project includes test cases to verify both the Flask app and the AI logic, including edge cases and failure scenarios.

| **Test Name**                        | **Type**       | **What It Verifies**                                             |
|-------------------------------------|----------------|------------------------------------------------------------------|
| `test_home_page_loads`              | Flask route    | Checks if the homepage loads successfully                        |
| `test_form_submission_valid`        | Flask route    | Valid form data submission returns a generated study plan        |
| `test_generate_study_plan_normal`   | AI Logic       | Standard input generates a correct response                      |
| `test_generate_study_plan_empty_input` | Edge case   | Ensures AI responds appropriately to empty inputs                |
| `test_generate_study_plan_api_failure` | Failure     | Simulates API failure and tests system's error-handling behavior |

To run the test cases:
```bash
python -m pytest test_app.py
```

## 💡 Future Updates
✅ SQLite Integration: Store user input and generated study plans  
✅ History Page: Add a route and button to view saved plans  
⏳ User Accounts: Enable login and personal study history  
⏳ Progress Tracker: Mark topics as completed  
⏳ Study Reminders: Integrate with Discord API  
⏳ Multi-language Support  

## 👨‍💻 Authors
Roberts Vītols & Renārs Ričards Hartmanis  
© 2025 AI Study Planner. All Rights Reserved.  
