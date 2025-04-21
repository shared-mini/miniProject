from flask import Blueprint
from flask import render_template, redirect, url_for
from flask import request, session

import os
import math
from pathlib import Path

import pandas as pd

import yfinance as yf

from ..db import data_util

tables_bp = Blueprint('tables', __name__, url_prefix="/tables")


####################################### kyoungbow area Start #######################################


@tables_bp.route("/kbTables", methods=['GET'])
def kbTables():
    return render_template('tables/kbTables.html')


@tables_bp.route("/kbTables-init", methods=['GET'])
def kbTables_init():

    data_util.create_table()

    bp_path = tables_bp.root_path # 현재 blueprint의 경로 ( 여기서는 views )
    root_path = Path(bp_path).parent #  부모 경로 (여기서는 demoweb )

    file_path_populationByYear = os.path.join(root_path, 'data_files', '연도별인구통계.csv')
    file_path_diseaseByPopulation = os.path.join(root_path, 'data_files', '연도별지역별인구별질병통계.csv')
    file_path_diseaseByAge = os.path.join(root_path, 'data_files', '질병성별연령별통계.csv')
    file_path_diseaseByMedical = os.path.join(root_path, 'data_files', '질병의료기관종별통계.csv')
    file_path_diseaseByRegion = os.path.join(root_path, 'data_files', '질병의료기관지역별통계.csv')
    file_path_diseaseByVisitType = os.path.join(root_path, 'data_files', '질병입원외래별통계.csv')
    file_path_area = os.path.join(root_path, 'data_files', '지역별토지면적.csv')
    file_path_diseaseByArea = os.path.join(root_path, 'data_files', '면적별인구별질병통계.csv')


    df_populationByYear = pd.read_csv(file_path_populationByYear)
    df_diseaseByPopulation = pd.read_csv(file_path_diseaseByPopulation)
    df_diseaseByAge = pd.read_csv(file_path_diseaseByAge)
    df_diseaseByMedical = pd.read_csv(file_path_diseaseByMedical)
    df_diseaseByRegion = pd.read_csv(file_path_diseaseByRegion)
    df_diseaseByVisitType = pd.read_csv(file_path_diseaseByVisitType)
    df_area = pd.read_csv(file_path_area)
    df_area = df_area[['PRD_DE','lcName','DT','UNIT_NM_ENG']]
    df_diseaseByArea = pd.read_csv(file_path_diseaseByArea)

    
    df_list = [
                {'df_populationByYear' : df_populationByYear},
                {'df_diseaseByPopulation' : df_diseaseByPopulation},
                {'df_diseaseByAge' : df_diseaseByAge},
                {'df_diseaseByMedical' : df_diseaseByMedical},
                {'df_diseaseByRegion' : df_diseaseByRegion},
                {'df_diseaseByVisitType' : df_diseaseByVisitType},
                {'df_area' : df_area},
                {'df_diseaseByArea' : df_diseaseByArea},
                ]
    
    for data in df_list:
        data_util.insert_data(data)
        
    # data = df_diseaseByPopulation.values.tolist() # pymysql ... executemany가 list, tuple 만 처리

    return redirect(url_for('main.index'))

@tables_bp.route('/kbTables-with-page', methods=['GET'])

def kbTables_with_page():

    tableNm = request.args.get('tableNm')
    rows = data_util.select_by_page(tableNm)
    columns = [col[0] for col in data_util.select_column(tableNm)]
    df = pd.DataFrame(rows,columns=columns)

    # 템플릿으로 이동 ( 위에서 읽은 데이터 전달 )
    return render_template('tables/kbTables.html',df=df,tableNm=tableNm)


####################################### kyoungbow area End #######################################



####################################### Yeongseo's  Start ########################################

@tables_bp.route("/ysTables", methods=['GET'])
def ysTables():
    return render_template('tables/ysTables.html')


@tables_bp.route("/ysTables-init", methods=['GET'])
def ysTables_init():

    data_util.create_ColdandTem_table()

    bp_path = tables_bp.root_path # 현재 blueprint의 경로 ( 여기서는 views )
    root_path = Path(bp_path).parent #  부모 경로 (여기서는 demoweb )

    file_path_ColdandTempDif = os.path.join(root_path, 'data_files', '202403_08_감기와일교차.csv')
    file_path_ColdandAirPo = os.path.join(root_path, 'data_files', '202305_09_감기와대기오염.csv')
    file_path_AsthmaandAirPo = os.path.join(root_path, 'data_files', '202305_09_천식과대기오염.csv')
    file_path_EyeandAirPo = os.path.join(root_path, 'data_files', '202305_09_눈병과대기오염.csv')
    file_path_DermaandAirPo = os.path.join(root_path, 'data_files', '202305_09_피부염과대기오염.csv')


    df_ColdandTempDif = pd.read_csv(file_path_ColdandTempDif)
    df_ColdandAirPo = pd.read_csv(file_path_ColdandAirPo)
    df_AsthmaandAirPo = pd.read_csv(file_path_AsthmaandAirPo)
    df_EyeandAirPo = pd.read_csv(file_path_EyeandAirPo)
    df_DermaandAirPo = pd.read_csv(file_path_DermaandAirPo)

    df_list = [
                {'df_ColdandTempDif' : df_ColdandTempDif},
                {'df_ColdandAirPo' : df_ColdandAirPo},
                {'df_AsthmaandAirPo' : df_AsthmaandAirPo},
                {'df_EyeandAirPo' : df_EyeandAirPo},
                {'df_DermaandAirPo' : df_DermaandAirPo}
                ]
    
    for data in df_list:
        data_util.insert_ColdandTem_data(data)
        
    # data = df_diseaseByPopulation.values.tolist() # pymysql ... executemany가 list, tuple 만 처리

    return redirect(url_for('main.index'))


@tables_bp.route('/ysTables-with-page', methods=['GET'])
def ysTables_with_page():

    tableNm = request.args.get('tableNm')
    rows = data_util.select_by_page(tableNm)
    columns = [col[0] for col in data_util.select_column(tableNm)]
    df = pd.DataFrame(rows,columns=columns)

    # 템플릿으로 이동 ( 위에서 읽은 데이터 전달 )
    return render_template('tables/ysTables.html',df=df,tableNm=tableNm)



####################################### Yeongseo's  End ##########################################
















########################################## yun start #######################################
@tables_bp.route("/yhTables", methods=['GET'])
def yhTables():
    tableNm = "covid_age_gender"  # ← DB에 이미 들어간 테이블명

    rows = data_util.select_by_page(tableNm)  # DB에서 데이터 가져오기
    columns = [col[0] for col in data_util.select3_column(tableNm)]  # 컬럼명 가져오기
    df = pd.DataFrame(rows, columns=columns)
    return render_template('tables/yhTables.html', df=df,tableNm=tableNm )



@tables_bp.route("/yhTables-init", methods=['GET'])
def yhTables_init():


    bp_path = tables_bp.root_path # 현재 blueprint의 경로 ( 여기서는 views )
    root_path = Path(bp_path).parent #  부모 경로 (여기서는 demoweb )
    file_path_covid_age_gender = os.path.join(root_path, 'data_files', '코로나성별연령현황.csv')
    df_covid_age_gender = pd.read_csv(file_path_covid_age_gender)

    df_covid_age_gender = df_covid_age_gender.fillna('')


    data_util.create_covid_age_gender_table()
    data = df_covid_age_gender.values.tolist()
    data_util.insert_covid_age_gender_data(data)
        
    # data = df_diseaseByPopulation.values.tolist() # pymysql ... executemany가 list, tuple 만 처리

    return redirect(url_for('main.index'))

@tables_bp.route('/yhTables-with-page', methods=['GET'])

def yhTables_with_page():

    tableNm = request.args.get('tableNm')
    rows = data_util.select_covid_age_gender_by_page(tableNm)
    columns = [col[0] for col in data_util.select_column(tableNm)]
    df = pd.DataFrame(rows, columns=columns)
    # 템플릿으로 이동 ( 위에서 읽은 데이터 전달 )
    return render_template('tables/yhTables.html',df=df,tableNm=tableNm)



############yun end############################################


####################################### table end #######################################