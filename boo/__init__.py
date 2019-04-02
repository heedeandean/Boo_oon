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

@app.route('/regist')
def login():
    u = User.query.filter(User.id == username).first()
    if len(u) > 0 :
        return True
    else : return False
    

@app.route('/boo')
def main():
    return render_template('ecom_main.html')

# 회원가입.
@app.route('/boo', methods=['GET','POST'])
def regist_post():
    username = request.form.get('username')
    pw = request.form.get('pw')
    pw2 = request.form.get('pw2')
    birthyear = request.form.get('birthyear')
    birthmonth = request.form.get('birthmonth')
    birthday = request.form.get('birthday')
    birthdate = birthyear + getzero(birthmonth) + getzero(birthday)
    sidogun = request.form.get('sidogun')
    city = request.form.get('city')
    addr = sidogun + ' ' + city
    gender = request.form.get('gender')
    job = request.form.get('job')
    email = request.form.get('email')

    u = Users(username, generate_password_hash(pw), birthdate, addr, gender, job, email)

    check = Users.query.filter(Users.username == username).first()

    

    if check == None :
        print('실패실패')
        return jsonify(username='가입 가능')

    else : 
        # response = make_response(render_template('ecom_main.html'))
        # response.headers['Content-Type'] = '  application/x-www-form-urlencoded; charset=UTF-8'
        # print('플라스크 ㅊㅊㅊㅊㅊㅊ')
        print('성공성공')
        return jsonify(username='이미 있음')

      
    
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


def getzero(md):
    if len(md) == 2 :
        return md
    else :
        return '0' + md