import pymysql
from . import dbInfo
## 중복 아이디 체크

def chk_primary(userName):
    row = None
    try:
        # conn =  dbInfo.dbInfo
        conn =  pymysql.connect(
                                host = "localhost",
                                user = "humanda5",
                                password = "humanda5",
                                database = "miniwebs")
        cursor = conn.cursor()
        sql = """select count(*) from member 
                where email = %s and deleted = FALSE"""
        cursor.execute(sql,(userName))
        row =  cursor.fetchone()

    except Exception as e :
        print(f"오류발생 = {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()
    
    return row

## 회원가입

def insert_member(eMail, passwd, userName):
    try:

        # conn =  dbInfo.dbInfo
        conn =  pymysql.connect(
                                host = "localhost",
                                user = "humanda5",
                                password = "humanda5",
                                database = "miniwebs")
        cursor = conn.cursor()
        sql = "insert into member (email, passwd, username) values (%s, %s, %s)"
        cursor.execute(sql,(eMail, passwd, userName))
        conn.commit()
    except Exception as e :
        print(f"오류발생 = {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()

## 로그인

def select_member_by_email(eMail):
    row = None
    try:
        # conn =  dbInfo.dbInfo
        conn =  pymysql.connect(
                                host = "localhost",
                                user = "humanda5",
                                password = "humanda5",
                                database = "miniwebs")
        cursor = conn.cursor()
        sql = """select 
                    email, passwd, username, usertype, regdate 
                from member 
                where email = %s and deleted = FALSE"""
        cursor.execute(sql,(eMail))
        row =  cursor.fetchone()

    except Exception as e :
        print(f"오류발생 = {e}")
        if conn: # DML 구문에서는 넣어줘야 함
            conn.rollback()
    finally:
        if cursor :
            cursor.close()
        if conn :
            conn.close()
    
    return row

