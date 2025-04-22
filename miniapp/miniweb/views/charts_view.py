from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify
from flask import request, session

import os
import math
from pathlib import Path

import pandas as pd

import yfinance as yf

from ..db import data_util

charts_bp = Blueprint('charts', __name__, url_prefix="/charts")


####################################### chart start #######################################


####################################### kyoungbow chart start #######################################
@charts_bp.route("/kbCharts", methods=['GET'])
def kb():
    years = data_util.select_chart_years()
        
    return render_template('charts/kbCharts.html',years=years)

@charts_bp.route('/kbCharts-async', methods=['GET'])
def kbCharts_async():
    
    type = request.args.get('type')
    year = request.args.get('years')
    rows = data_util.select_chart_data(type,year)

    return jsonify(rows)



####################################### kyoungbow chart end #######################################









###################################### Yeongseo's AREA Start #####################################

from pathlib import Path
import pandas as pd

@charts_bp.route("/ysCharts", methods=['GET'])
def ys():
    base_dir = Path(__file__).resolve().parents[1]
    data_dir = base_dir / "data_files"

    cold_path = data_dir / "감기_lag_상관관계.csv"
    asthma_path = data_dir / "천식_lag_상관관계.csv"
    day_path = data_dir / "감기천식일교차.csv"

    if not all([cold_path.exists(), asthma_path.exists(), day_path.exists()]):
        return "하나 이상의 파일이 존재하지 않습니다.", 500

    # 기본 상관관계
    df_cold = pd.read_csv(cold_path).round(2)
    df_asthma = pd.read_csv(asthma_path).round(2)
    day_df = pd.read_csv(day_path)

    corr_df = day_df[['감기발생건수', '천식발생건수', '일교차']].corr().round(2)
    x_labels = corr_df.columns.tolist()
    y_labels = corr_df.index.tolist()
    z_values = corr_df.values.tolist()

    labels = df_cold.columns.tolist()
    cold_corr = df_cold.corr().round(2).values.tolist()
    asthma_corr = df_asthma.corr().round(2).values.tolist()

    # 감기 lag
    cold_lags = {}
    cold_axis_labels = []
    for i in range(6):
        lag_file = data_dir / f"감기_lag{i}_대기오염.csv"
        if not lag_file.exists():
            return f"감기 lag{i} 파일이 없습니다.", 500
        df = pd.read_csv(lag_file).round(2)
        corr = df.corr().round(2)
        cold_lags[f"cold_lag{i}"] = corr.values.tolist()
        if i == 0:
            cold_axis_labels = corr.columns.tolist()

    # 천식 lag
    asthma_lags = {}
    asthma_axis_labels = []
    for i in range(7):
        lag_file = data_dir / f"천식_lag{i}_대기오염.csv"
        if not lag_file.exists():
            return f"천식 lag{i} 파일이 없습니다.", 500
        df = pd.read_csv(lag_file).round(2)
        df.columns.values[0] = f"천식_lag{i}"
        corr = df.corr().round(2)
        asthma_lags[f"asthma_lag{i}"] = corr.values.tolist()
        if i == 0:
            asthma_axis_labels = corr.columns.tolist()

    # 눈병 lag
    eyedis_lags = {}
    eyedis_axis_labels = []
    for i in range(7):
        lag_file = data_dir / f"눈병_lag{i}_대기오염.csv"
        if not lag_file.exists():
            return f"눈병 lag{i} 파일이 없습니다.", 500
        df = pd.read_csv(lag_file).round(2)
        df.columns.values[0] = f"눈병_lag{i}"
        corr = df.corr().round(2)
        eyedis_lags[f"eyedis_lag{i}"] = corr.values.tolist()
        if i == 0:
            eyedis_axis_labels = corr.columns.tolist()

    # 피부염 lag
    dermati_lags = {}
    dermati_axis_labels = []
    for i in range(7):
        lag_file = data_dir / f"피부염_lag{i}_대기오염.csv"
        if not lag_file.exists():
            return f"피부염 lag{i} 파일이 없습니다.", 500
        df = pd.read_csv(lag_file).round(2)
        df.columns.values[0] = f"피부염_lag{i}"
        corr = df.corr().round(2)
        dermati_lags[f"dermati_lag{i}"] = corr.values.tolist()
        if i == 0:
            dermati_axis_labels = corr.columns.tolist()

    return render_template('charts/ysCharts.html',
                           x_labels=x_labels,
                           y_labels=y_labels,
                           z_values=z_values,
                           labels=labels,
                           cold_corr=cold_corr,
                           asthma_corr=asthma_corr,
                           cold_axis_labels=cold_axis_labels,
                           asthma_axis_labels=asthma_axis_labels,
                           eyedis_axis_labels=eyedis_axis_labels,
                           dermati_axis_labels=dermati_axis_labels,
                           axis_labels=cold_axis_labels,
                           cold_lag0=cold_lags['cold_lag0'],
                           cold_lag1=cold_lags['cold_lag1'],
                           cold_lag2=cold_lags['cold_lag2'],
                           cold_lag3=cold_lags['cold_lag3'],
                           cold_lag4=cold_lags['cold_lag4'],
                           cold_lag5=cold_lags['cold_lag5'],
                           asthma_lag0=asthma_lags['asthma_lag0'],
                           asthma_lag1=asthma_lags['asthma_lag1'],
                           asthma_lag2=asthma_lags['asthma_lag2'],
                           asthma_lag3=asthma_lags['asthma_lag3'],
                           asthma_lag4=asthma_lags['asthma_lag4'],
                           asthma_lag5=asthma_lags['asthma_lag5'],
                           asthma_lag6=asthma_lags['asthma_lag6'],
                           eyedis_lag0=eyedis_lags['eyedis_lag0'],
                           eyedis_lag1=eyedis_lags['eyedis_lag1'],
                           eyedis_lag2=eyedis_lags['eyedis_lag2'],
                           eyedis_lag3=eyedis_lags['eyedis_lag3'],
                           eyedis_lag4=eyedis_lags['eyedis_lag4'],
                           eyedis_lag5=eyedis_lags['eyedis_lag5'],
                           eyedis_lag6=eyedis_lags['eyedis_lag6'],
                           dermati_lag0=dermati_lags['dermati_lag0'],
                           dermati_lag1=dermati_lags['dermati_lag1'],
                           dermati_lag2=dermati_lags['dermati_lag2'],
                           dermati_lag3=dermati_lags['dermati_lag3'],
                           dermati_lag4=dermati_lags['dermati_lag4'],
                           dermati_lag5=dermati_lags['dermati_lag5'],
                           dermati_lag6=dermati_lags['dermati_lag6']
                           )




###################################### Yeongseo's AREA End #######################################


####################### yunhwan chart ################################################################
@charts_bp.route("/yhCharts", methods=['GET'])
def yh():
    return render_template('charts/yhCharts.html')  # 여기서는 HTML만 반환


# 상관계수 히트맵
@charts_bp.route('/api/correlation-data-2')
def correlation_data_2():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # zminiweb/views
    csv_path = os.path.join(base_dir, '..', 'data_files', '코로나성별연령현황.csv')  # ✅ 수정된 경로

    csv_path = os.path.abspath(csv_path)  # 절대 경로로 바꿔줌
    print("✅ CSV 경로:", csv_path)  # 경로 디버깅 확인

    df = pd.read_csv(csv_path, encoding='utf-8')  # 또는 encoding='cp949' 도 시도해볼 수 있음
    df_numeric = df.select_dtypes(include='number')
    corr = df_numeric.corr().round(2)

    series = []
    for row in corr.index:
        series.append({
            "name": row,
            "data": [{"x": col, "y": corr.loc[row, col]} for col in corr.columns]
        })

    return jsonify(series)

 
# 연령별 평균 사망률
@charts_bp.route('/api/age-mortality')
def age_mortality_api():
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, '..', 'data_files', '코로나성별연령현황.csv')

    df = pd.read_csv(csv_path, encoding='utf-8')
    df_age_mortality = df[['연령', '사망률']].groupby('연령').mean().reset_index()
    df_age_mortality = df_age_mortality.sort_values(by='연령')

    categories = df_age_mortality['연령'].tolist()
    data = df_age_mortality['사망률'].round(2).tolist()  

    return jsonify({
        "categories": categories,
        "data": data
    })

# 연령별 평균 확진률 
@charts_bp.route('/api/age-infection-rate')
def age_infection_rate_api():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, '..', 'data_files', '코로나성별연령현황.csv')

    df = pd.read_csv(csv_path, encoding='utf-8')
    df.columns = df.columns.str.strip()  # 혹시 모를 공백 제거

    # 연령 정보가 존재하는 행만 필터링
    df_age = df[df['연령'].notna()].copy()

    # 연령별 확진률 평균 계산
    age_confirm_rate = df_age.groupby('연령')['확진률'].mean().reset_index()
    age_confirm_rate = age_confirm_rate.sort_values(by='연령')

    return jsonify({
        'categories': age_confirm_rate['연령'].tolist(),
        'data': age_confirm_rate['확진률'].round(2).tolist()
    })

# 성별 사망률, 확진률 
@charts_bp.route('/api/gender-stats')
def gender_stats_api():
    # 성별 비율 수치
    gender_data = {
        "labels": ["여성", "남성"],
        "infection_rate": [54, 46],
        "death_rate": [50.6, 49.4]
    }
    return jsonify(gender_data)

#######################yunhwan end #####################################################################