from flask import Flask, redirect, url_for, request, render_template
import requests
import json

app = Flask(__name__, template_folder= 'Templates')
context_set = ""

@app.route('/', methods = ['POST', 'GET'])
def index():

    return render_template('home.html')

if __name__ == '__main__':
  app.run(debug=True)