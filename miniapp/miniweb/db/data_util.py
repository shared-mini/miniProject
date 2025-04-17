
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


##################################### Yeongseo's area Start #######################################

import pymysql

def create_ColdandTem_table():
    try:
        conn = pymysql.connect(host="localhost", 
                               database='miniwebs', 
                               user='humanda5', 
                               password='humanda5')

        cursor = conn.cursor()

        sql="""drop table if exists ColdandTem"""
        cursor.execute(sql)
        
        # 감기와 천식의 일교차와 연관성
        sql="""create table  if not exists ColdandTem
               (
                   날짜 varchar(20) not null
                   ,감기발생건수 int null
                   ,천식발생건수 int null
                   ,일교차 float null
                );"""
        cursor.execute(sql)

        # 대기오염수치와 감기의 연관성
        sql="""create table  if not exists ColdandAirPo
               (
                   날짜 varchar(20) not null
                   ,시군구명 varchar(20) null
                   ,발생건수 int null
                   ,이산화질소농도 float null
                   ,오존농도 float null
                   ,일산화탄소농도 float null
                   ,아황산가스농도 float null
                   ,미세먼지농도 float null
                   ,초미세먼지농도 float null
                );"""
        cursor.execute(sql)

        # 대기오염수치와 천식의 연관성
        sql="""create table  if not exists AsthmaandAirPo
               (
                   날짜 varchar(20) not null
                   ,시군구명 varchar(20) null
                   ,발생건수 int null
                   ,이산화질소농도 float null
                   ,오존농도 float null
                   ,일산화탄소농도 float null
                   ,아황산가스농도 float null
                   ,미세먼지농도 float null
                   ,초미세먼지농도 float null
                );"""
        cursor.execute(sql)

        # 대기오염수치와 눈병의 연관성
        sql="""create table  if not exists EyeandAirPo
               (
                   날짜 varchar(20) not null
                   ,시군구명 varchar(20) null
                   ,발생건수 int null
                   ,이산화질소농도 float null
                   ,오존농도 float null
                   ,일산화탄소농도 float null
                   ,아황산가스농도 float null
                   ,미세먼지농도 float null
                   ,초미세먼지농도 float null
                );"""
        cursor.execute(sql)

        # 대기오염수치와 피부염의 연관성
        sql="""create table  if not exists DermaandAirPo
               (
                   날짜 varchar(20) not null
                   ,시군구명 varchar(20) null
                   ,발생건수 int null
                   ,이산화질소농도 float null
                   ,오존농도 float null
                   ,일산화탄소농도 float null
                   ,아황산가스농도 float null
                   ,미세먼지농도 float null
                   ,초미세먼지농도 float null
                );"""
        cursor.execute(sql)

    except Exception as e:
        print('테이블 생성 실패', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_ColdandTem_data(data):
    try:
        conn = pymysql.connect(host="localhost", 
                            database='miniwebs', 
                            user='humanda5', 
                            password='humanda5')

        cursor = conn.cursor()

        if 'df_ColdandTempDif' in data: 
            sql = "insert into ColdandTem values (%s, %s, %s, %s)"
            cursor.executemany(sql, data.get('df_ColdandTempDif').values.tolist())

        if 'df_ColdandAirPo' in data: 
            sql = "insert into ColdandAirPo values (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
            cursor.executemany(sql, data.get('df_ColdandAirPo').values.tolist())

        if 'df_AsthmaandAirPo' in data: 
            sql = "insert into AsthmaandAirPo values (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
            cursor.executemany(sql, data.get('df_AsthmaandAirPo').values.tolist())

        if 'df_DermaandAirPo' in data: 
            sql = "insert into DermaandAirPo values (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
            cursor.executemany(sql, data.get('df_DermaandAirPo').values.tolist())

        if 'df_EyeandAirPo' in data: 
            sql = "insert into EyeandAirPo values (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
            cursor.executemany(sql, data.get('df_EyeandAirPo').values.tolist())

        conn.commit()
    except Exception as e:
        print('데이터 저장 실패', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def select_ColdandTem():
    rows = None
    try:
        conn = pymysql.connect(host="localhost", 
                            database='miniwebs', 
                            user='humanda5', 
                            password='humanda5')

        cursor = conn.cursor()

        sql="select * from ColdandTem"
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


def select_ColdandTem_by_page(offset, limit):
    try:
        conn = pymysql.connect(host="localhost", 
                                database='miniwebs', 
                                user='humanda5', 
                                password='humanda5')
        cursor = conn.cursor()

        sql = f"SELECT * FROM ColdandTem LIMIT {offset}, {limit}"  # offset, limit을 이용하여 페이지네이션
        cursor.execute(sql)
        rows = cursor.fetchall()

        return rows
    except Exception as e:
        print(f"Error in select_ColdandTem_by_page: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()




def select_ColdandTem_count():
    cnt = None
    try:
        conn = pymysql.connect(host="localhost", 
                               database='miniwebs', 
                               user='humanda5', 
                               password='humanda5')

        cursor = conn.cursor()

        sql = "select count(*) from ColdandTem"
        cursor.execute(sql)
        cnt = cursor.fetchone()
        
        if cnt:
            return cnt[0]
        return 0
    except Exception as e:
        print('데이터 조회 실패', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


##################################### Yeongseo's area End #######################################