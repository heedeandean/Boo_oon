from flask import Flask, url_for, render_template, request, Response, session, jsonify, make_response, redirect, flash, json
from boo.db_class import Users, Cmt, Lists, Follow, Ranking, Likecnt, DM, db_session
from datetime import date, datetime, timedelta
from werkzeug import generate_password_hash

app = Flask(__name__)
app.debug = True
app.jinja_env.trim_blocks = True

app.config.update(
	SECRET_KEY='X1243yRH!mMwf',
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days
)

@app.route('/boo')
def main():
    return render_template('ecom_main.html')

# 회원가입.
@app.route('/boo', methods=['GET'])
def regist():
    return render_template("ecom_main.html")

@app.route('/boo', methods=['POST'])
def regist_post():
    username = request.values.get('username')
    pw = request.values.get('pw')
    pw2 = request.values.get('pw2')
    birthdate = request.values.get('birthdate')
    city = request.values.get('city')
    gender = request.values.get('gender')
    job = request.values.get('job')
    email = request.values.get('email')

    if pw != pw2:
        flash("암호를 정확히 입력하세요!!")
        return render_template("ecom_main.html", email=email, username=username)
    else:
        u = Users(username, generate_password_hash(pw), birthdate, city, gender, job, email)
        try:
            db_session.add(u)
            db_session.commit()

            flash("%s 님, 가입을 환영합니다!" % username)
            
            
        except Exception as err:
            print("Error on users>>>", err)
            db_session.rollback()
        
        return render_template("ecom_main.html")
        




@app.teardown_appcontext
def teardown_context(exception):
    print(">>> teardown context!!", exception)
    db_session.remove() 