from flask import Blueprint
from flask import render_template, redirect, url_for
from flask import request, session

from ..db import member_util

from werkzeug.security import generate_password_hash, check_password_hash
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# 로그인
@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method.lower() == 'get':
        return render_template("auth/login-register.html")
    else:
        # 1. 요청 데이터 읽기
        eMail = request.form.get('eMail', 'noeMail')
        password = request.form.get('password', 'noPW')
        chkRemember = request.form.get('chkRemember', 'off')
        # ## 테이블 생성 후 주석 해제
        row = member_util.select_member_by_email(eMail) 
        if not row:
            return render_template("auth/login-register.html",
                                   message="잘못된 회원 정보입니다") 

        # 2. 요청 처리
        if check_password_hash(row[1], password): # 로그인 성공
            session['loginuser'] = eMail
            return redirect(url_for('main.index')) 
        else:   # 로그인 실패
            return render_template("auth/login-register.html",
                                   message="잘못된 회원 정보입니다") 

# 로그아웃
@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear() # session의 모든 데이터 제거
    return redirect(url_for('main.index'))

# 회원가입
@auth_bp.route('/register', methods=['POST'])
def register():
    userName = request.form.get('userName')
    eMail = request.form.get('eMail')
    password = request.form.get('password')
    passwd_hash = generate_password_hash(password)
    try:
        chk = int(member_util.chk_primary(eMail)[0])
        if chk > 0 :
            return render_template("auth/login-register.html",
                                   message="이미 등록된 이메일 입니다.") 
        else:
            member_util.insert_member(eMail, passwd_hash, userName)
            return render_template("auth/login-register.html",
                                   message="가입 되었습니다.") 
    except Exception as e :
        print(f"오류발생 = {e}")
        return render_template("auth/login-register.html",
                                   message="오류가 발생했습니다. 관리자에게 문의하세요.") 
        