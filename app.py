<<<<<<< HEAD
from flask import Flask,render_template,request,jsonify
import numpy as np
import os
import sys
import io
import base64
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import api 

plt.rcParams['font.sans-serif'] = ['SimHei'] # 修改这里尝试不同的字体名
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)


app = Flask(
    __name__,
    template_folder=resource_path("templates"),
    static_folder=resource_path("static")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process",methods=["POST"])
def process():
    api.debug_print(request)
    language = request.json["Language"] 
    ChartType = request.json["chartType"]
    if language =='python':
        chart_image = None
        if ChartType == "line" :
            return api.Python_Line(chart_image)
        elif ChartType == "bar" :
            return api.Python_Bar(chart_image)
        elif ChartType == "histogram": 
            return api.Python_Histogram(chart_image)
        # 其他图表类型的处理逻辑可以在这里添加
    elif language =='JS':
        if ChartType == "line" :
           return api.JS_Line()


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)
=======
from flask import Flask,render_template,request,jsonify
import numpy as np
import os
import sys
import io
import base64
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import api 

plt.rcParams['font.sans-serif'] = ['SimHei'] # 修改这里尝试不同的字体名
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)


app = Flask(
    __name__,
    template_folder=resource_path("templates"),
    static_folder=resource_path("static")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process",methods=["POST"])
def process():
    api.debug_print(request)
    language = request.json["Language"] 
    ChartType = request.json["chartType"]
    if language =='python':
        chart_image = None
        if ChartType == "line" :
            return api.Python_Line(chart_image)
        elif ChartType == "bar" :
            return api.Python_Bar(chart_image)
        elif ChartType == "histogram": 
            return api.Python_Histogram(chart_image)
        # 其他图表类型的处理逻辑可以在这里添加
    elif language =='JS':
        if ChartType == "line" :
           return api.JS_Line()


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)
>>>>>>> b9f8aecd2322683f65de26eab2c5e228a399aea8
