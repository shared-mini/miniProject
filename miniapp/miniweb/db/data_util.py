
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
        sql = """drop table if exists area"""
        cursor.execute(sql)
        sql = """drop table if exists diseaseByArea"""
        cursor.execute(sql)
        sql = """drop table if exists riskByArea"""
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
        
        # 지역별토지면적
        sql = """create table if not exists area
                (
                    years int not null
                    ,lcName varchar(100) not null
                    ,dt BIGINT not null
                    ,unit varchar(100) not null
                );"""
        cursor.execute(sql)

        # 면적별발병률
        sql = """create table if not exists diseaseByArea
                (
                    years int not null
                    ,lcName varchar(100) not null
                    ,ptntCnt int not null
                    ,dt BIGINT not null
                    ,unit varchar(100) not null
                    ,area TEXT
                    ,incidenceRate float not null
                );"""
        cursor.execute(sql)

        # 밀집도별위험도
        sql = """create table if not exists riskByArea
                (
                    years int not null
                    ,lcName varchar(100) not null
                    ,populationTot int not null
                    ,ptntCnt int not null
                    ,dt BIGINT not null
                    ,populationDensity float not null
                    ,incidenceRate float not null
                    ,risk float
                );"""
        cursor.execute(sql)

    except Exception as e:
        print('테이블 생성 실패', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# 데이터 삽입
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

        if 'df_area' in data:
            sql = "insert into area values (%s, %s, %s, %s)"
            cursor.executemany(sql, data.get('df_area').values.tolist())

        if 'df_diseaseByArea' in data:
            sql = "insert into diseaseByArea values (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, data.get('df_diseaseByArea').values.tolist())

        if 'df_riskByArea' in data:
            sql = "insert into riskByArea values (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, data.get('df_riskByArea').values.tolist())

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
        print('데이터 조회 실패', e)
        print("tableNm=="+tableNm)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return rows


# 컬럼 조회
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
        print('데이터 조회 실패', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return rows

def select_chart_years():
    rows = None
    try:
        conn = pymysql.connect(host="localhost", 
                               database='miniwebs', 
                               user='humanda5', 
                               password='humanda5')
        
        cursor = conn.cursor()
        sql = "SELECT distinct years FROM diseasebypopulation"
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        print('데이터 조회 실패', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return rows


def select_chart_data(type,year,radio):
    rows = None
    try:
        conn = pymysql.connect(host="localhost", 
                               database='miniwebs', 
                               user='humanda5', 
                               password='humanda5')
        
        cursor = conn.cursor()
        print("radio==" , radio)
        print("type==" , type)
        print("year==" , year)

        if radio == "population":
            if type == "heatmap":
                if year != 'all':
                    sql = f"SELECT * FROM diseasebypopulation where years = {year} order by populationTot"
                if year == 'all':
                    sql = "SELECT * FROM diseasebypopulation order by populationTot"
            if type == "bar":
                if year != 'all':
                    sql = f"SELECT * FROM diseasebypopulation where years = {year} order by populationTot desc"
                if year == 'all':
                    sql = "SELECT 1, 2, sum(populationTot), sum(ptntCnt), (sum(ptntCnt)/sum(populationTot)), lcName FROM diseasebypopulation group by lcName order by sum(populationTot) desc"


        if radio == "area":
            if type == "heatmap":
                if year != 'all':
                    sql = f"SELECT years,lcName,dt,2,incidenceRate,concat(lcName,' ',area) FROM diseasebyarea where years = {year} order by dt"
                if year == 'all':
                    sql = "SELECT years, lcName, round(avg(ptntCnt)), round(avg(dt)), round(avg(ptntCnt)/avg(dt),6) FROM diseasebyarea group by years,lcName order by round(avg(dt))"
            if type == "bar":
                if year != 'all':
                    sql = f"SELECT * FROM diseasebyarea where years = {year} order by dt"
                if year == 'all':
                    # sql = "SELECT 1,lcName, round(avg(ptntCnt)), round(avg(dt)),2, concat(round(avg(dt)), '㎡'), round(avg(ptntCnt)/avg(dt),6) FROM diseasebyarea group by lcName"
                    sql = "SELECT * FROM diseasebyarea"

        if radio == "risk":
            if type == "heatmap":
                if year != 'all':
                    sql = f"select years,lcName,1,2,risk,concat(lcName,' ',populationDensity) from riskbyarea where years = {year} order by populationDensity"
                if year == 'all':
                    sql = """
                            SELECT 
                            A.years,
                            concat(A.lcName,' ',ROUND(B.avg_density,6)),
                            A.populationTot,
                            A.populationDensity,
                            A.risk,
                            A.dt,
                            B.avg_density
                        FROM riskbyarea A
                        JOIN (
                            SELECT 
                                lcName,
                                AVG(populationDensity) AS avg_density
                            FROM riskbyarea
                            GROUP BY lcName
                        ) B ON A.lcName = B.lcName
                        ORDER BY B.avg_density
                        """
            if type == "bar":
                if year != 'all':
                    sql = f"SELECT * FROM riskbyarea where years = {year}"
                if year == 'all':
                    sql = "SELECT * FROM riskbyarea"


        print(sql)
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        print('데이터 조회 실패', e)
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
        print('데이터 조회 실패', e)
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
        print('데이터 조회(카운터) 실패', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


##################################### Yeongseo's area End #######################################

###################################### yunhwan area start ######################################

import pymysql

def create_covid_age_gender_table():
    try:
        conn = pymysql.connect(host="localhost", 
                               db='miniwebs', 
                               user='humanda5', 
                               password='humanda5')
        
        cursor = conn.cursor()

        sql = """drop table if exists covid_age_gender"""
        cursor.execute(sql)

        # 코로나 성별, 연령 현황
        sql = """create table if not exists covid_age_gender
                (
                    치명률 float 
                    ,사망자수 int 
                    ,사망률 float 
                    ,확진률 float 
                    ,등록일자 varchar(50)
                    ,확진자수 int 
                    ,연령 varchar(50) 
                    ,성별 varchar(50) 
                );"""
        cursor.execute(sql)

    
    except Exception as e:
        print('테이블 조회 실패', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_covid_age_gender_data(data):
    try:
        conn = pymysql.connect(host="localhost", 
                               db='miniwebs', 
                               user='humanda5', 
                               password='humanda5')
        
        cursor = conn.cursor()


        # df= df.fillna(None)
        # values = df.values.tolist()

        # if 'covid_age_gender' in data: 
        sql = "insert into covid_age_gender values (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, data)


        
        conn.commit()
    except Exception as e:
        print('데이터 저장 실패2', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# 테이블 데이터 조회
def select_covid_age_gender_by_page(tableNm):
    rows = None
    try:
        conn = pymysql.connect(host="localhost", 
                               db='miniwebs', 
                               user='humanda5', 
                               password='humanda5')
        
        cursor = conn.cursor()

        sql = f"select * from {tableNm}"
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        print('데이터 저장 실패3', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return rows


def select_column3(tableNm):
    rows = None
    try:
        conn = pymysql.connect(
            host="localhost",
            db="miniwebs",
            user="humanda5",
            password="humanda5"
        )
        cursor = conn.cursor()
        sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s"
        cursor.execute(sql, (tableNm,))
        rows = cursor.fetchall()
    except Exception as e:
        print("컬럼 조회 실패", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows



###################################### yunhwan area end ######################################

###################################### 회원 테이블 생성 ######################################
def create_member_table():
    try:
        conn = pymysql.connect(host="localhost", 
                               database='miniwebs', 
                               user='humanda5', 
                               password='humanda5')
        
        cursor = conn.cursor()

        sql = """drop table if exists member"""
        cursor.execute(sql)
        

        # 멤버 테이블 생성
        sql = """create table member
                (
                    email varchar(100) primary key,
                    passwd varchar(200) not null,
                    username varchar(20),
                    usertype varchar(20) default('user'),
                    deleted boolean default(false),
                    regdate date default(now())
                );"""
        cursor.execute(sql)
        

    except Exception as e:
        print('테이블 생성 실패', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
###################################### 회원 테이블 생성 ######################################