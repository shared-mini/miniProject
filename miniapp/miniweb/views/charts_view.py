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









@charts_bp.route("/ysCharts", methods=['GET'])
def ys():
    return render_template('charts/ysCharts.html')


@charts_bp.route("/yhCharts", methods=['GET'])
def yh():
    return render_template('charts/yhCharts.html')


####################################### chart end #######################################

