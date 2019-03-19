from flask import Flask, url_for, render_template, request, Response, session, jsonify, make_response, redirect, flash, json

app = Flask(__name__)
app.debug = True

@app.route('/boo')
def main():
    return render_template('ecom_main.html')



  