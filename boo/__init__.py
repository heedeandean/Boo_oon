from flask import Flask, url_for, render_template, request, Response, session, jsonify, make_response, redirect, flash, json
from boo.db_class import Users, Cmt, Lists, Follow, Ranking, Likecnt, DM, db_session
from datetime import date, datetime, timedelta
from werkzeug import generate_password_hash, check_password_hash


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

@app.route('/boo/idcheck', methods=['GET','POST'])
def ifexists():
    username = request.form.get('username')

    checkid = Users.query.filter(Users.username == username).first()

    checkem = Users.query.filter(Users.email == username).first()
    
    if checkid == None and checkem == None :
        print('실패실패', username)
        return jsonify(username='가입 가능')

    elif checkid == None and checkem != None :
        print('이메일은 있음', username)
        return jsonify(username='이메일 있음')

    else : 
        # response = make_response(render_template('ecom_main.html'))
        # response.headers['Content-Type'] = '  application/x-www-form-urlencoded; charset=UTF-8'
        print('성공성공')
        return jsonify(username='이미 있음')

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

    try:
        db_session.add(u)
        db_session.commit()

        flash("%s 님, 가입을 환영합니다!" % username)
        
    except Exception as err:
        print("Error on users>>>", err)
        db_session.rollback()
    
    return render_template("ecom_main.html")

# 로그인.
@app.route('/boo/login', methods=['GET', 'POST'])
def login_post():
    username = request.form.get('loginUsername')
    pw = request.form.get('loginPw')

    # u = Users.query.filter(Users.username == username, Users.pw == pw).params(username=username, pw=pw).first()

    u = Users.query.filter(Users.username == username).first()
    
    if u is not None:
        if check_password_hash(u.pw, pw) == True:
            session['loginUser'] = { 'username': u.username }
            
            if session.get('next'):
                next = session.get('next')
                del session['next']
                return redirect(next)

            flash("안녕하세요. %s 님" % username)
            return redirect('/boo')

        else:
            flash("비밀번호가 올바르지 않습니다!!")
            return redirect('/boo')
    else:
        flash("아이디가 올바르지 않습니다!!")
        return redirect('/boo')



# 로그아웃
@app.route('/logout')
def logout():
    if session.get('loginUser'):
        del session['loginUser']

    return redirect('/')
    


@app.teardown_appcontext
def teardown_context(exception):
    print(">>> teardown context!!", exception)
    db_session.remove() 


def getzero(md):
    if len(md) == 2 :
        return md
    else :
        return '0' + md