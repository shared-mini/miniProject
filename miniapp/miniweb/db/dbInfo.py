import pymysql
## 중복 아이디 체크

dbInfo =  pymysql.connect(
                        host = "localhost",
                        user = "humanda5",
                        password = "humanda5",
                        database = "miniwebs")