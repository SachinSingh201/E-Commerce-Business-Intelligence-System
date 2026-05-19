from flask import Flask, render_template
import requests

app = Flask(__name__)

API_URL = "http://localhost:8000/api"

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/customers')
def customers():
    return render_template('customers.html')

@app.route('/forecast')
def forecast():
    return render_template('forecast.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
