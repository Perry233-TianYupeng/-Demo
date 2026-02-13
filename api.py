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

plt.rcParams['font.sans-serif'] = ['SimHei'] # 修改这里尝试不同的字体名
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

def format_data(data):
    if data is None:
        return None
    if isinstance(data, list):
        return [round(float(num), 3) if isinstance(num, (int, float)) else num for num in data]
    return round(float(data), 3)

def generate_chart_image(x, y, chart_type, cumulative=False, logoption=False, xlabel=None, ylabel=None, title=None, label=None, width=0.5, alpha=0.8, gridon=True, bins=10, histtype='bar', color=None, density=False, orientation='vertical'):
    """
    使用matplotlib生成图表并返回base64编码的图片
    """
    # 创建图形
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 根据图表类型绘制不同的图表
    if chart_type == 'line':
        ax.plot(x, y, label=label if label else '原始数据')
        ax.set_xlabel(xlabel if xlabel else None)
        ax.set_ylabel(ylabel if ylabel else None)
        if cumulative:
            cumsum = np.cumsum(y)
            ax.plot(x, cumsum, label='累积和', color='red')
        if logoption:
            ax.set_xscale('log')
        ax.set_title(title if title else None)
        
    elif chart_type == 'bar':
        ax.bar(x, y, width=width, alpha=alpha, label=label if label else '原始数据')
        ax.set_xlabel(xlabel if xlabel else None)
        ax.set_ylabel(ylabel if ylabel else None)
        ax.set_title(title if title else None)
        
    elif chart_type == 'histogram':
        data_to_plot = y if isinstance(y[0], list) else [y]
        if color == "":
            color = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'purple', 'pink', 'brown']
        # 循环绘制每一组数据
        for i, data_group in enumerate(data_to_plot):
            ax.hist(
                data_group,
                bins=bins, # 使用前端传递的 bins 参数
                histtype=histtype, # 使用前端传递的 histtype
                density=density, # 使用前端传递的 density
                orientation=orientation, # 使用前端传递的 orientation
                cumulative=cumulative, # 使用前端传递的 cumulative
                color=color[i], # 使用前端传递的 color
                alpha=alpha, # 使用前端传递的 alpha
                label=f"Group {i+1}", # 为每组数据生成标签
                log=logoption # 使用前端传递的 logoption (对应 Y 轴对数)
            )
        ax.set_title(title if title else None)
        
    elif chart_type == 'boxplot':
        ax.boxplot(y)
        ax.set_title(title if title else None)
    elif chart_type == 'scatter':
        ax.scatter(x, y)
        ax.set_title(title if title else None)
    elif chart_type == 'pie':
        ax.pie(y, labels=x, autopct='%1.1f%%')
        ax.set_title(title if title else None)
        
    ax.legend()
    ax.grid(gridon)
    
    # 将图形转换为PNG格式的字节流
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
    img_buffer.seek(0)
    
    # 将字节流转换为base64编码的字符串
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    
    # 关闭图形，释放内存
    plt.close(fig)
    
    return img_str

def debug_print(request):
    print("--------Debug Info---------")
    print(request.json)

def receive_line_data():
    xdata = request.json["x"]
    ydata = request.json["y"] if "y" in request.json else None
    ChartType = request.json["chartType"] 
    print(f"Received data: x={xdata}, y={ydata},ChartType={ChartType}")
    return xdata, ydata, ChartType

def preprocess_line_data(xdata, ydata):
    xdata_np = np.array(xdata) if len(ydata) else np.arange(0,len(xdata),1)
    ydata_np = np.array(ydata) if len(ydata) else np.array(xdata)
    sort_indices = np.argsort(xdata_np)
    x_sorted = xdata_np[sort_indices]
    y_sorted = ydata_np[sort_indices]
    return x_sorted, y_sorted

def LineChartProcess(x, y, cumulative=False, logoption=False):
    if cumulative:
        cum = np.cumsum(y)
    if logoption:
        x = np.log10(x + 1e-10)
    if cumulative:
        return x, cum
    return x,y

def Python_Line(chart_image=None):
    xdata, ydata,ChartType = receive_line_data()
    x,y=preprocess_line_data(xdata, ydata)
    chart_image = generate_chart_image(x=x, y=y, chart_type=ChartType, cumulative=request.json["cumulative"], logoption=request.json["logoption"],xlabel=request.json["xlabel"],ylabel=request.json["ylabel"],title=request.json["title"],label=request.json["label"],gridon=request.json["gridon"])
    return jsonify({
            "x":format_data(x.tolist()),
            "y":format_data(y.tolist()),
            "xmean":format_data(float(x.mean()) if len(ydata) else float(y.mean())),
            "xstd":format_data(float(x.std()) if len(ydata) else float(y.std())),
            "xmax":format_data(float(x.max()) if len(ydata) else float(y.max())),
            "xmin":format_data(float(x.min()) if len(ydata) else float(y.min())),
            "ymean":format_data(float(y.mean()) if len(ydata) else None),
            "ystd":format_data(float(y.std()) if len(ydata) else None),
            "ymax":format_data(float(y.max()) if len(ydata) else None),
            "ymin":format_data(float(y.min()) if len(ydata) else None),
            "chartImage": chart_image
        })   

def JS_Line():
    xdata, ydata,ChartType = receive_line_data()
    x,y=preprocess_line_data(xdata, ydata)
    cumsum = None
    x_data,y_data=x.copy(),y.copy()
    x_data,tmp = LineChartProcess(x,y,request.json["cumulative"],request.json["logoption"])
    if request.json["cumulative"]:
        cumsum = tmp   
    return jsonify({
                "x":format_data(x.tolist()),
                "y":format_data(y.tolist()),
                "xmean":format_data(float(x.mean()) if len(ydata) else float(y.mean())),
                "xstd":format_data(float(x.std()) if len(ydata) else float(y.std())),
                "xmax":format_data(float(x.max()) if len(ydata) else float(y.max())),
                "xmin":format_data(float(x.min()) if len(ydata) else float(y.min())),
                "ymean":format_data(float(y.mean()) if len(ydata) else None),
                "ystd":format_data(float(y.std()) if len(ydata) else None),
                "ymax":format_data(float(y.max()) if len(ydata) else None),
                "ymin":format_data(float(y.min()) if len(ydata) else None),
                "x_data":format_data(x_data.tolist()),
                "y_data":format_data(y_data.tolist()),
                "cumsum":format_data(cumsum.tolist()) if cumsum is not None else None,
                "chartImage": None
            })

def Python_Bar(chart_image=None):
    debug_print(request)
    x,y,ChartType=request.json["x"], request.json["y"], request.json["chartType"]
    y=np.array(y) 
    xlength=len(set(x))
    chart_image = generate_chart_image(x=x, y=y, chart_type=ChartType, xlabel=request.json["xlabel"],ylabel=request.json["ylabel"],title=request.json["title"],label=request.json["label"],width=request.json["width"],alpha=request.json["alpha"],gridon=request.json["gridon"])
    return jsonify({
            "x":x,
            "y":format_data(y.tolist()),
            "xlength":xlength,
            "ymean":format_data(float(y.mean())) ,
            "ystd":format_data(float(y.std())),
            "ymax":format_data(float(y.max())),
            "ymin":format_data(float(y.min())),
            "chartImage": chart_image
        })   

def Python_Histogram(chart_image=None):
    # 获取参数
    y = request.json["y"] # 这是一个二维列表
    bins = request.json.get("bins", 10)
    histtype = request.json.get("histtype")
    color = request.json.get("color")
    alpha = request.json.get("alpha", 0.8)
    density = request.json.get("density", False)
    orientation = request.json.get("orientation", "vertical")
    cumulative = request.json.get("cumulative", False)
    logoption = request.json.get("logScale", False)
    title = request.json.get("title")
    gridon = request.json.get("gridon", True)
    
    # 生成图表
    chart_image = generate_chart_image(
        x=None, # 直方图不需要 x
        y=y,
        chart_type="histogram",
        cumulative=cumulative,
        logoption=logoption,
        title=title,
        gridon=gridon,
        bins=bins,
        histtype=histtype,
        color=color,
        alpha=alpha,
        density=density,
        orientation=orientation
    )
    
    # 返回响应
    return jsonify({
        "chartImage": chart_image
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

plt.rcParams['font.sans-serif'] = ['SimHei'] # 修改这里尝试不同的字体名
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

def format_data(data):
    if data is None:
        return None
    if isinstance(data, list):
        return [round(float(num), 3) if isinstance(num, (int, float)) else num for num in data]
    return round(float(data), 3)

def generate_chart_image(x, y, chart_type, cumulative=False, logoption=False, xlabel=None, ylabel=None, title=None, label=None, width=0.5, alpha=0.8, gridon=True, bins=10, histtype='bar', color=None, density=False, orientation='vertical'):
    """
    使用matplotlib生成图表并返回base64编码的图片
    """
    # 创建图形
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 根据图表类型绘制不同的图表
    if chart_type == 'line':
        ax.plot(x, y, label=label if label else '原始数据')
        ax.set_xlabel(xlabel if xlabel else None)
        ax.set_ylabel(ylabel if ylabel else None)
        if cumulative:
            cumsum = np.cumsum(y)
            ax.plot(x, cumsum, label='累积和', color='red')
        if logoption:
            ax.set_xscale('log')
        ax.set_title(title if title else None)
        
    elif chart_type == 'bar':
        ax.bar(x, y, width=width, alpha=alpha, label=label if label else '原始数据')
        ax.set_xlabel(xlabel if xlabel else None)
        ax.set_ylabel(ylabel if ylabel else None)
        ax.set_title(title if title else None)
        
    elif chart_type == 'histogram':
        data_to_plot = y if isinstance(y[0], list) else [y]
        if color == "":
            color = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'purple', 'pink', 'brown']
        # 循环绘制每一组数据
        for i, data_group in enumerate(data_to_plot):
            ax.hist(
                data_group,
                bins=bins, # 使用前端传递的 bins 参数
                histtype=histtype, # 使用前端传递的 histtype
                density=density, # 使用前端传递的 density
                orientation=orientation, # 使用前端传递的 orientation
                cumulative=cumulative, # 使用前端传递的 cumulative
                color=color[i], # 使用前端传递的 color
                alpha=alpha, # 使用前端传递的 alpha
                label=f"Group {i+1}", # 为每组数据生成标签
                log=logoption # 使用前端传递的 logoption (对应 Y 轴对数)
            )
        ax.set_title(title if title else None)
        
    elif chart_type == 'boxplot':
        ax.boxplot(y)
        ax.set_title(title if title else None)
    elif chart_type == 'scatter':
        ax.scatter(x, y)
        ax.set_title(title if title else None)
    elif chart_type == 'pie':
        ax.pie(y, labels=x, autopct='%1.1f%%')
        ax.set_title(title if title else None)
        
    ax.legend()
    ax.grid(gridon)
    
    # 将图形转换为PNG格式的字节流
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
    img_buffer.seek(0)
    
    # 将字节流转换为base64编码的字符串
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    
    # 关闭图形，释放内存
    plt.close(fig)
    
    return img_str

def debug_print(request):
    print("--------Debug Info---------")
    print(request.json)

def receive_line_data():
    xdata = request.json["x"]
    ydata = request.json["y"] if "y" in request.json else None
    ChartType = request.json["chartType"] 
    print(f"Received data: x={xdata}, y={ydata},ChartType={ChartType}")
    return xdata, ydata, ChartType

def preprocess_line_data(xdata, ydata):
    xdata_np = np.array(xdata) if len(ydata) else np.arange(0,len(xdata),1)
    ydata_np = np.array(ydata) if len(ydata) else np.array(xdata)
    sort_indices = np.argsort(xdata_np)
    x_sorted = xdata_np[sort_indices]
    y_sorted = ydata_np[sort_indices]
    return x_sorted, y_sorted

def LineChartProcess(x, y, cumulative=False, logoption=False):
    if cumulative:
        cum = np.cumsum(y)
    if logoption:
        x = np.log10(x + 1e-10)
    if cumulative:
        return x, cum
    return x,y

def Python_Line(chart_image=None):
    xdata, ydata,ChartType = receive_line_data()
    x,y=preprocess_line_data(xdata, ydata)
    chart_image = generate_chart_image(x=x, y=y, chart_type=ChartType, cumulative=request.json["cumulative"], logoption=request.json["logoption"],xlabel=request.json["xlabel"],ylabel=request.json["ylabel"],title=request.json["title"],label=request.json["label"],gridon=request.json["gridon"])
    return jsonify({
            "x":format_data(x.tolist()),
            "y":format_data(y.tolist()),
            "xmean":format_data(float(x.mean()) if len(ydata) else float(y.mean())),
            "xstd":format_data(float(x.std()) if len(ydata) else float(y.std())),
            "xmax":format_data(float(x.max()) if len(ydata) else float(y.max())),
            "xmin":format_data(float(x.min()) if len(ydata) else float(y.min())),
            "ymean":format_data(float(y.mean()) if len(ydata) else None),
            "ystd":format_data(float(y.std()) if len(ydata) else None),
            "ymax":format_data(float(y.max()) if len(ydata) else None),
            "ymin":format_data(float(y.min()) if len(ydata) else None),
            "chartImage": chart_image
        })   

def JS_Line():
    xdata, ydata,ChartType = receive_line_data()
    x,y=preprocess_line_data(xdata, ydata)
    cumsum = None
    x_data,y_data=x.copy(),y.copy()
    x_data,tmp = LineChartProcess(x,y,request.json["cumulative"],request.json["logoption"])
    if request.json["cumulative"]:
        cumsum = tmp   
    return jsonify({
                "x":format_data(x.tolist()),
                "y":format_data(y.tolist()),
                "xmean":format_data(float(x.mean()) if len(ydata) else float(y.mean())),
                "xstd":format_data(float(x.std()) if len(ydata) else float(y.std())),
                "xmax":format_data(float(x.max()) if len(ydata) else float(y.max())),
                "xmin":format_data(float(x.min()) if len(ydata) else float(y.min())),
                "ymean":format_data(float(y.mean()) if len(ydata) else None),
                "ystd":format_data(float(y.std()) if len(ydata) else None),
                "ymax":format_data(float(y.max()) if len(ydata) else None),
                "ymin":format_data(float(y.min()) if len(ydata) else None),
                "x_data":format_data(x_data.tolist()),
                "y_data":format_data(y_data.tolist()),
                "cumsum":format_data(cumsum.tolist()) if cumsum is not None else None,
                "chartImage": None
            })

def Python_Bar(chart_image=None):
    debug_print(request)
    x,y,ChartType=request.json["x"], request.json["y"], request.json["chartType"]
    y=np.array(y) 
    xlength=len(set(x))
    chart_image = generate_chart_image(x=x, y=y, chart_type=ChartType, xlabel=request.json["xlabel"],ylabel=request.json["ylabel"],title=request.json["title"],label=request.json["label"],width=request.json["width"],alpha=request.json["alpha"],gridon=request.json["gridon"])
    return jsonify({
            "x":x,
            "y":format_data(y.tolist()),
            "xlength":xlength,
            "ymean":format_data(float(y.mean())) ,
            "ystd":format_data(float(y.std())),
            "ymax":format_data(float(y.max())),
            "ymin":format_data(float(y.min())),
            "chartImage": chart_image
        })   

def Python_Histogram(chart_image=None):
    # 获取参数
    y = request.json["y"] # 这是一个二维列表
    bins = request.json.get("bins", 10)
    histtype = request.json.get("histtype")
    color = request.json.get("color")
    alpha = request.json.get("alpha", 0.8)
    density = request.json.get("density", False)
    orientation = request.json.get("orientation", "vertical")
    cumulative = request.json.get("cumulative", False)
    logoption = request.json.get("logScale", False)
    title = request.json.get("title")
    gridon = request.json.get("gridon", True)
    
    # 生成图表
    chart_image = generate_chart_image(
        x=None, # 直方图不需要 x
        y=y,
        chart_type="histogram",
        cumulative=cumulative,
        logoption=logoption,
        title=title,
        gridon=gridon,
        bins=bins,
        histtype=histtype,
        color=color,
        alpha=alpha,
        density=density,
        orientation=orientation
    )
    
    # 返回响应
    return jsonify({
        "chartImage": chart_image
>>>>>>> b9f8aecd2322683f65de26eab2c5e228a399aea8
    })