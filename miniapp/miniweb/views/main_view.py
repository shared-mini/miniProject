
from flask import Blueprint
from flask import render_template

main_bp = Blueprint('main', __name__, url_prefix="/")

@main_bp.route("/", methods=['GET'])
def index():
    # 요청 데이터 읽기
    # 요청 처리
    # 응답 컨텐츠 생산
    return render_template('index.html')

@main_bp.route("/wizard", methods=['GET'])
def wizard():
    # 요청 데이터 읽기
    # 요청 처리
    # 응답 컨텐츠 생산
    return render_template('wizard.html')

