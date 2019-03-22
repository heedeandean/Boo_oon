from flask import Flask, url_for, render_template, request, Response, session, jsonify, make_response, redirect, flash, json
from boo.db_class import User, Comment, List, Follow, Ranking, Likecnt, DM

app = Flask(__name__)
app.debug = True

@app.route('/boo')
def main():
    return render_template('ecom_main.html')


@app.route('/comment', methods=['GET'])
def comment():
    cmts = Comment.query.all()
    return jsonify([s.json() for s in cmts])
  
  