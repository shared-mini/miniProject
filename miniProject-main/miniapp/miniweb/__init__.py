from flask import Flask, render_template
from .views import main_view, auth_view, charts_view, tables_view

def create_app(): # Flask가 웹 애플리케이션을 시작할 때 자동으로 호출하는 함수
    app = Flask(__name__) # web application 만들기

    app.config['SECRET_KEY'] = 'humanda5-secret-key' # 세션(session) 등을 사용하기 위한 설정

    app.register_blueprint(main_view.main_bp)
    app.register_blueprint(auth_view.auth_bp)
    app.register_blueprint(charts_view.charts_bp)
    app.register_blueprint(tables_view.tables_bp)
        
    return app