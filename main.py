<<<<<<< HEAD
import threading
import webview 
from app import app

def run_flask():
    app.run()

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

    webview.create_window("数据可视化系统", "http://127.0.0.1:5000")
    webview.start()
=======
import threading
import webview 
from app import app

def run_flask():
    app.run()

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

    webview.create_window("数据可视化系统", "http://127.0.0.1:5000")
    webview.start()
>>>>>>> b9f8aecd2322683f65de26eab2c5e228a399aea8
