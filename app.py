# --- Backend (Flask - app.py) ---
from flask import Flask, render_template, request, jsonify
import datetime
import json

app = Flask(__name__)

# Data storage (in-memory, for simplicity. Consider a database for production)
activities = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_activity', methods=['POST'])
def add_activity():
    data = request.get_json()
    date_str = data.get('date')
    activity = data.get('activity')
    duration = data.get('duration')

    if not date_str or not activity or not duration:
        return jsonify({'error': 'Missing data'}), 400

    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        duration = int(duration)
    except ValueError:
        return jsonify({'error': 'Invalid date or duration'}), 400

    if date not in activities:
        activities[date] = []

    activities[date].append({'activity': activity, 'duration': duration})
    return jsonify({'message': 'Activity added successfully'})

@app.route('/get_activities', methods=['GET'])
def get_activities():
    date_str = request.args.get('date')

    if not date_str:
        return jsonify({'error': 'Missing date'}), 400

    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date'}), 400

    if date in activities:
        return jsonify(activities[date])
    else:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
