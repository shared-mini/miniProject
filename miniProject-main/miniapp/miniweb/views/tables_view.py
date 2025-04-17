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


    df_populationByYear = pd.read_csv(file_path_populationByYear)
    df_diseaseByPopulation = pd.read_csv(file_path_diseaseByPopulation)
    df_diseaseByAge = pd.read_csv(file_path_diseaseByAge)
    df_diseaseByMedical = pd.read_csv(file_path_diseaseByMedical)
    df_diseaseByRegion = pd.read_csv(file_path_diseaseByRegion)
    df_diseaseByVisitType = pd.read_csv(file_path_diseaseByVisitType)

    df_list = [
                {'df_populationByYear' : df_populationByYear},
                {'df_diseaseByPopulation' : df_diseaseByPopulation},
                {'df_diseaseByAge' : df_diseaseByAge},
                {'df_diseaseByMedical' : df_diseaseByMedical},
                {'df_diseaseByRegion' : df_diseaseByRegion},
                {'df_diseaseByVisitType' : df_diseaseByVisitType}
                ]
    
    for data in df_list:
        data_util.insert_data(data)
        
    # data = df_diseaseByPopulation.values.tolist() # pymysql ... executemany가 list, tuple 만 처리

    return redirect(url_for('main.index'))

# @tables_bp.route('/kbTables-with-page', methods=['GET'])
# def kbTables_with_page():

#     tableNm = request.args.get('tableNm')
#     page_no = request.args.get('page_no','1')
#     page_no = int(page_no)

#     pager = {
#         "page_no" : page_no,
#         "page_size" : 10, # 한 페이지에 표시 할 행의 수
#         "pager_size" : 5 # 페이지 번호 표시 갯수
#     }

#     # 전체 테이터 갯수
#     data_cnt = data_util.select_count(tableNm) # 전체 데이터 갯수

#     pager['page_cnt'] = math.ceil(data_cnt / pager['page_size']) # 나눗셈 + 올림
#     pager['page_start'] = ( (pager['page_no'] - 1) // pager['pager_size'] ) * pager['pager_size'] + 1
#     pager['page_stop'] =  pager['page_start'] + pager['pager_size']
#     page_start = (page_no - 1) * 10 # 현재 페이지에서 보여줄 데이터의 시작 번호

#     rows = data_util.select_by_page(tableNm, page_start, pager['page_size'])

#     columns = [col[0] for col in data_util.select_column(tableNm)]
    
#     print("columns===", columns)
#     df = pd.DataFrame(rows,columns=columns)


#     # 템플릿으로 이동 ( 위에서 읽은 데이터 전달 )
#     return render_template('tables/kbTables.html',df=df, pager=pager)

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













@tables_bp.route("/yhTables", methods=['GET'])
def yhTables():
    return render_template('tables/yhTables.html')



####################################### table end #######################################