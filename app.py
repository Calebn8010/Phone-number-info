from flask import Flask, render_template, redirect, request, session
from flask_session import Session
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def hello_world():
    
    return render_template("index.html")