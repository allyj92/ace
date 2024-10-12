from flask import Flask, redirect, render_template, request, url_for
import os

app = Flask(__name__)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Perform login logic here
        return "Login successful!"
    return render_template('login.html')  # Render your HTML login form here

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Perform signup logic here
        return "Signup successful!"
    return render_template('signup.html')  # Render your HTML signup form here

# Main route for the Streamlit app
@app.route('/')
def index():
    # Run the Streamlit app
    os.system("streamlit run client/app2.py")  # Assumes Streamlit app is located at client/app2.py
    return redirect('http://localhost:8501')  # Redirect to Streamlit

if __name__ == '__main__':
    app.run(port=5000)