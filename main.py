from flask import Flask,render_template,request,redirect,session
import mysql.connector
from sentiments import second
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)
app.register_blueprint(second)

@app.route('/')
def home():
    return render_template('home.html')



if __name__=="__main__":
    app.run(debug=True)