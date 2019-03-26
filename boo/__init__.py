from flask import Flask, url_for, render_template, request, Response, session, jsonify, make_response, redirect, flash, json
# from boo.db_class import User, Comment, List, Follow, Ranking, Likecnt, DM, db_session
from boo.db_class import User, Follow, db_session
from datetime import date, datetime, timedelta

app = Flask(__name__)
app.debug = True

app.config.update(
	SECRET_KEY='X1243yRH!mMwf',
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days
)

@app.route('/boo')
def main():
    return render_template('ecom_main.html')

@app.route('/boo', methods=['GET'])
def regist():
    return render_template("ecom_main.html")

@app.route('/boo', methods=['POST'])
def regist_post():
    email = request.values.get('email')
    passwd = request.values.get('passwd')
    passwd2 = request.values.get('passwd2')
    username = request.values.get('username')
    birth = request.values.get('birth')
    gender = request.values.get('gender')
    city = request.values.get('addr')
    job = request.values.get('job')

    if passwd != passwd2:
        flash("암호를 정확히 입력하세요!!")
        return render_template("ecom_main.html", email=email, username=username)
    else:
        u = User( username, passwd, birth, city, gender, job, email)
        try:
            db_session.add(u)
            db_session.commit()

        except Exception as err:
            print("Erroir on user>>>", err)
            db_session.rollback()

        flash("%s 님, 가입을 환영합니다!" % username)
        return redirect("/boo")
  
  