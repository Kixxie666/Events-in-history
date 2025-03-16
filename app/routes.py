from flask import Blueprint, render_template, request
import requests
from datetime import datetime

main = Blueprint("main", __name__)  # Define the Blueprint

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/search', methods=['POST'])
def search():
    date = request.form.get("date")

    # Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return render_template('index.html', events=[], error="Invalid date format! Use YYYY-MM-DD.")

    events = []  # Placeholder for API response
    try:
        response = requests.get(f"https://history.muffinlabs.com/date/{date.split('-')[1]}/{date.split('-')[2]}")
        if response.status_code == 200:
            data = response.json()
            events = data.get("data", {}).get("Events", [])
        else:
            return render_template('index.html', events=[], error="Failed to fetch events. Try again.")
    except requests.exceptions.RequestException as e:
        return render_template('index.html', events=[], error=f"Network error: {str(e)}")

    return render_template('index.html', events=events)
