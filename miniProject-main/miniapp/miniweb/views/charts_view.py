from flask import Blueprint
from flask import render_template, redirect, url_for
from flask import request, session


charts_bp = Blueprint('charts', __name__, url_prefix="/charts")


####################################### chart start #######################################

@charts_bp.route("/kbCharts", methods=['GET'])
def kb():
    return render_template('charts/kbCharts.html')


@charts_bp.route("/ysCharts", methods=['GET'])
def ys():
    return render_template('charts/ysCharts.html')


@charts_bp.route("/yhCharts", methods=['GET'])
def yh():
    return render_template('charts/yhCharts.html')


####################################### chart end #######################################

