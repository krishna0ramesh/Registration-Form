
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Backend microservice URL
BACKEND_URL = "http://127.0.0.1:5001"


# Display the form
@app.route('/')
def home():
    return render_template('index.html')


# Handle form submission
@app.route('/submit', methods=['POST'])
def submit():

    name = request.form.get('name')
    email = request.form.get('email')

    data = {
        "name": name,
        "email": email
    }

    try:
        # Send data to backend
        response = requests.post(
            f"{BACKEND_URL}/submit",
            json=data,
            timeout=10
        )

        # Check backend response
        if response.status_code == 201:
            return redirect(url_for('success'))

        error = response.json().get(
            "error", "Something went wrong"
        )

    except requests.RequestException:
        error = "Unable to connect to backend service"

    except ValueError:
        error = "Invalid response received from backend"

    return render_template('index.html', error=error), 500


# Success page
@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/todo')
def todo():
    return render_template('todo.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
