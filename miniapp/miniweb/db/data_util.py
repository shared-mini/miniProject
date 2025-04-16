
import pymysql


###################################### kyoungbow area Start ######################################

def create_table():
    try:
        conn = pymysql.connect(host="localhost", 
                               database='miniwebs', 
                               user='humanda5', 
                               password='humanda5')
        
        cursor = conn.cursor()

        sql = """drop table if exists populationByYear"""
        cursor.execute(sql)
        sql = """drop table if exists diseaseByPopulation"""
        cursor.execute(sql)
        sql = """drop table if exists diseaseByAge"""
        cursor.execute(sql)
        sql = """drop table if exists diseaseByMedical"""
        cursor.execute(sql)
        sql = """drop table if exists diseaseByRegion"""
        cursor.execute(sql)
        sql = """drop table if exists diseaseByVisitType"""
        cursor.execute(sql)

        # 연도별인구통계
        sql = """create table if not exists populationByYear
                (
                    years int not null
                    ,seq int not null
                    ,lcName varchar(100) not null
                    ,populationTot int not null
                    ,populationMan int not null
                    ,populationFemale int not null
                    ,houshol int not null
                );"""
        cursor.execute(sql)

        # 연도별지역별인구별질병통계
        sql = """create table if not exists diseaseByPopulation
                (
                    years int not null
                    ,lcName varchar(100) not null
                    ,populationTot int not null
                    ,ptntCnt int not null
                    ,incidenceRate float not null
                    ,label varchar(500) not null
                );"""
        cursor.execute(sql)

        # 질병성별연령별통계
        sql = """create table if not exists diseaseByAge
                (
                    years int not null
                    ,age varchar(100) not null
                    ,ptntCnt int not null
                    ,rvdInsupBrdnAmt int not null
                    ,rvdRpeTamtAmt int not null
                    ,sex varchar(100) not null
                    ,sickCd varchar(100) not null
                    ,sickNm varchar(500) not null
                    ,specCnt int not null
                    ,vstDdcnt int not null
                );"""
        cursor.execute(sql)

        # 질병의료기관종별통계
        sql = """create table if not exists diseaseByMedical
                (
                    years int not null
                    ,grade varchar(100) not null
                    ,ptntCnt int not null
                    ,rvdInsupBrdnAmt int not null
                    ,rvdRpeTamtAmt int not null
                    ,sickCd varchar(100) not null
                    ,sickNm varchar(500) not null
                    ,specCnt int not null
                    ,vstDdcnt int not null
                );"""
        cursor.execute(sql)

        # 질병의료기관지역별통계
        sql = """create table if not exists diseaseByRegion
                (
                    years int not null
                    ,lcName varchar(100) not null
                    ,ptntCnt int not null
                    ,rvdInsupBrdnAmt int not null
                    ,rvdRpeTamtAmt int not null
                    ,sickCd varchar(100) not null
                    ,sickNm varchar(500) not null
                    ,specCnt int not null
                    ,vstDdcnt int not null
                );"""
        cursor.execute(sql)

        # 질병입원외래별통계
        sql = """create table if not exists diseaseByVisitType
                (
                    years int not null
                    ,inpatOpat varchar(100) not null
                    ,ptntCnt int not null
                    ,rvdInsupBrdnAmt int not null
                    ,rvdRpeTamtAmt int not null
                    ,sex varchar(100) not null
                    ,sickCd varchar(100) not null
                    ,sickNm varchar(500) not null
                    ,specCnt int not null
                    ,vstDdcnt int not null
                );"""
        cursor.execute(sql)
    except Exception as e:
        print('테이블 생성 실패', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_data(data):
    try:
        conn = pymysql.connect(host="localhost", 
                               database='miniwebs', 
                               user='humanda5', 
                               password='humanda5')
        
        cursor = conn.cursor()

        if 'df_populationByYear' in data: 
            sql = "insert into populationByYear values (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, data.get('df_populationByYear').values.tolist())

        if 'df_diseaseByPopulation' in data:
            sql = "insert into diseaseByPopulation values (%s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, data.get('df_diseaseByPopulation').values.tolist())

        if 'df_diseaseByAge' in data:
            sql = "insert into diseaseByAge values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, data.get('df_diseaseByAge').values.tolist())

        if 'df_diseaseByMedical' in data:
            sql = "insert into diseaseByMedical values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, data.get('df_diseaseByMedical').values.tolist())

        if 'df_diseaseByRegion' in data:
            sql = "insert into diseaseByRegion values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, data.get('df_diseaseByRegion').values.tolist())

        if 'df_diseaseByVisitType' in data:
            sql = "insert into diseaseByVisitType values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, data.get('df_diseaseByVisitType').values.tolist())


        
        conn.commit()
    except Exception as e:
        print('데이터 저장 실패', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# 테이블 데이터 조회
def select_by_page(tableNm):
    rows = None
    try:
        conn = pymysql.connect(host="localhost", 
                               database='miniwebs', 
                               user='humanda5', 
                               password='humanda5')
        
        cursor = conn.cursor()

        sql = f"select * from {tableNm}"
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        print('데이터 저장 실패', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return rows

# 전체 데이터 조회
# def select_count(tableNm):
#     cnt = None
#     try:
#         conn = pymysql.connect(host="localhost", 
#                                database='miniwebs', 
#                                user='humanda5', 
#                                password='humanda5')
        
#         cursor = conn.cursor()

#         sql = f"select count(*) from {tableNm}"
#         cursor.execute(sql)
#         rows = cursor.fetchone()
#     except Exception as e:
#         print('조회 실패', e)
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()

#     return rows[0]


def select_column(tableNm):
    rows = None
    try:
        conn = pymysql.connect(host="localhost", 
                               database='miniwebs', 
                               user='humanda5', 
                               password='humanda5')
        
        cursor = conn.cursor()

        sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s"
        cursor.execute(sql,(tableNm))
        rows = cursor.fetchall()
    except Exception as e:
        print('데이터 저장 실패', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return rows

###################################### kyoungbow area End ######################################

