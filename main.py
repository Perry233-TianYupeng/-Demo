"""
main.py — 桌面应用入口

使用 pywebview 将 Flask Web 应用包装为桌面窗口。
启动时会自动开启 Flask 后端，然后在原生窗口中加载前端页面。
"""

import threading
import webview
from app import create_app
from config import HOST, PORT, WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT


def run_flask():
    """在子线程中启动 Flask 服务器"""
    flask_app = create_app()
    flask_app.run(host=HOST, port=PORT, debug=False)


if __name__ == '__main__':
    # 启动 Flask 后台线程
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

    # 创建桌面窗口
    webview.create_window(
        title=WINDOW_TITLE,
        url=f'http://{HOST}:{PORT}',
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
    )
    webview.start()
