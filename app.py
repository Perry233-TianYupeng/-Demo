"""
app.py — Flask 应用工厂

职责：
  1. 创建 Flask 应用实例
  2. 配置模板/静态文件目录
  3. 注册路由
  4. 启动开发服务器

所有图表处理逻辑已移至 routes/chart_routes.py。
"""

import os
import sys
from flask import Flask, render_template

from config import HOST, PORT, DEBUG


def resource_path(relative_path):
    """
    获取资源文件的绝对路径，兼容 PyInstaller 打包和开发环境。
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def create_app():
    """
    Flask 应用工厂函数。
    创建并配置 Flask 实例、注册蓝图或路由。
    """
    app = Flask(
        __name__,
        template_folder=resource_path('templates'),
        static_folder=resource_path('static')
    )

    # ---------- 注册路由 ----------
    from routes.chart_routes import dispatch_process

    @app.route('/')
    def home():
        """首页"""
        return render_template('index.html')

    @app.route('/process', methods=['POST'])
    def process():
        """统一的数据处理入口（字典分发到各图表处理器）"""
        return dispatch_process()

    return app


# ---------- 直接运行 ----------
if __name__ == '__main__':
    app = create_app()
    app.run(debug=DEBUG, host=HOST, port=PORT)
