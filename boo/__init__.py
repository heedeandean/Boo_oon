from flask import Flask, url_for, render_template, request, Response, session, jsonify, make_response, redirect, flash, json, g
from boo.db_class import Users, Cmt, Lists, Follow, Ranking, Likecnt, DM, db_session
from datetime import date, datetime, timedelta
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy import update
from sqlalchemy.orm import relationship, backref, joinedload



app = Flask(__name__)
app.debug = True
app.jinja_env.trim_blocks = True

app.config.update(
	SECRET_KEY='X1243yRH!mMwf',
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days
)

islogin = False
user = ''

@app.route('/boo', methods=['GET','POST'])
def main():
    global islogin, user

    session['islogin'] = {'islogin' : islogin}
    islogin = session.get('islogin')['islogin']

    if islogin == False :
        user = ''
    elif user != "" :
        user = session.get('loginUser')['username']
    
    return render_template('ecom_main.html', islogin = islogin, user = user)


@app.route('/boo/sub', methods=['GET','POST'])
def sub():

    kw = request.form.get('keyword')
    
    
    if kw != None :
        kw = '%' + kw +'%'
        
        # lists = Lists.query.options(joinedload(Lists.fk_users))
        lists = Users.query.filter(Users.city.like(kw)).all()

        # lists = Users.query.filter(Users.city == kw).all()

        print('#@@@@@@@@@@@@@@@@@@@',lists)
        for l in lists :
            lists = Lists.query.filter(Lists.userno == l.userno).all()

            return jsonify( [l.json() for l in lists])

    return render_template('boo_sub.html')



# 가입시 아이디, 이메일 중복 체크.
@app.route('/boo/idcheck', methods=['GET','POST'])
def ifexists():
    username = request.form.get('username')

    checkid = Users.query.filter(Users.username == username).first()
    checkem = Users.query.filter(Users.email == username).first()
    
    if checkid == None and checkem == None :
        return jsonify(username='가입 가능')

    elif checkid == None and checkem != None : 
        return jsonify(username='이메일 있음')

    else : 
        return jsonify(username='이미 있음')


# 회원가입.
@app.route('/boo/regist', methods=['GET','POST'])
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
    
    # return render_template("ecom_main.html")
    return redirect('/boo')
    

# 로그인.
@app.route('/boo/login', methods=['GET','POST'])
def login_post():
    global islogin, user

    username = request.form.get('username')
    pw = request.form.get('pw')

    u = Users.query.filter(Users.username == username).first()

    print('login의 첫번째 islogin >>>???>>>>', islogin)
    if u is not None:
    
        if check_password_hash(u.pw, pw) == True:

            islogin = True
            user = u.username

            session['loginUser'] = { 'username': u.username }

            return redirect("/boo")
            
        else:
            return jsonify(login='비밀번호 오류')

    else:  
        return jsonify(login='아이디 오류')  # if u is None
        print(">>>>>>>>>>>로그인 실패<<<<<<<<<<<<")  
        


# 로그아웃.
@app.route('/boo/logout')
def logout():
    
    global islogin

    if session.get('loginUser'):
        del session['loginUser']

        islogin = False

    return redirect('/boo')


# 글쓰기.
@app.route('/boo/write', methods=['GET', 'POST'])
def write():
    global user

    list_title = request.form.get('list_title')
    list_txt = request.form.get('list_txt')
    public = request.form.get('public')
    (cmt_count, like_cnt, hate_cnt, list_date, isdelete) = (None, None, None, None, None)

    print('확인확인확인', user, list_title, list_txt, public)
    u = Users.query.filter(Users.username == user).first()
    print("UUUUUUUUU", u)

    lists = Lists( u.userno, list_title, list_txt, cmt_count, like_cnt, hate_cnt, public, list_date, isdelete)
    print("U리스트리스트시르트시읗ㅁ", lists)

    try:
        db_session.add(lists)
        db_session.commit()
        
    except Exception as err:
        print("Error on users>>>", err)
        db_session.rollback()
    
    return redirect('/boo')
    

# 뜬구름 좋아요, 싫어요 수 조정
@app.route('/boo/like_hate', methods=['GET', 'POST'])
def hate():
    l_id = request.values.get('list_id')
    num = request.values.get('num')
    feel = request.values.get('feel')

    lst = Lists.query.filter(Lists.list_id == l_id).first()

    try:
        if feel == 'like' :
            if num == 'add' :
                lst.likecnt += 1
            else :
                lst.likecnt -= 1

        elif feel == 'hate':
            if num == 'add' :
                lst.hatecnt -= 1
            else :
                lst.hatecnt += 1

        db_session.commit()

    except Exception as err:
        print("Error on users>>>", err)
        db_session.rollback()
    
    return redirect('/boo')


# 뜬구름 좋아요, 싫어요 수 조정
@app.route('/boo/cmt_like_hate/<list_id>', methods=['POST'])
def cmt_like(list_id):
    
    num = request.values.get('num')
    cmt_id = request.values.get('cmt_id')

    cmt = Cmt.query.filter('list_id=:list_id and cmt_id=:cmt_id').params(
        list_id=list_id, cmt_id=cmt_id).first()

    try:
       
        if num == 'add' :
            cmt.cmt_like += 1
        else :
            cmt.cmt_hate -= 1

        db_session.commit()

    except Exception as err:
        print("Error on users>>>", err)
        db_session.rollback()
    
    return redirect('/boo')


### 댓글 ####
@app.route('/boo/comment', methods=['GET','POST'])
def comment():
    global user
    u = Users.query.filter(Users.username == user).first()
    

    list_id = request.values.get('list_id')
    cmt_txt = request.values.get('cmt_txt')
    ( cmt_date, cmt_like, cmt_hate ) = (None, None, None)

    c = Cmt(u.userno, cmt_txt, cmt_date, list_id, cmt_like, cmt_hate)

    try:
        db_session.add(c)
        db_session.commit()
        
        
    except Exception as err:
        print("Error on users>>>", err)
        db_session.rollback()

    return redirect('/boo')


@app.route('/boo/comment/<list_id>', methods=['GET'])
def comment_get(list_id):

    cmts = Cmt.query.filter('list_id=:list_id').params(
        list_id=list_id).order_by(Cmt.cmt_id.desc()).all()

    return jsonify([c.json() for c in cmts])


@app.route('/boo/comment/<cmt_id>', methods=['DELETE'])
def comment_delete(cmt_id):

    print("DDDDDDDDDDDDDDDDD>>>", cmt_id)

    try:
        Cmt.query.filter(Cmt.cmt_id == cmt_id).delete()
        db_session.commit()

    except SQLAlchemyError as err:
        db_session.rollback()
        print("Error!!", err)

    return jsonify({"result": 'OK'})


# 카드 
@app.route('/boo/lists', methods=['GET'])
def cards():

    lists = Lists.query.order_by(Lists.list_id.desc())
    lists = lists.filter(Lists.public == 1).all()

    return jsonify( [l.json() for l in lists] )


# 랭크
@app.route('/boo/rank', methods=['GET'])
def rank():

    lists = Lists.query.order_by(Lists.likecnt.desc())
    lists = lists.filter(Lists.public == 1).all()

    return jsonify( [l.json() for l in lists] )
    


@app.teardown_appcontext
def teardown_context(exception):
    print(">>> teardown context!!", exception)
    db_session.remove() 


def getzero(md):
    if len(md) == 2 :
        return md
    else :
        return '0' + md