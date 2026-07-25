"""
routes/chart_routes.py — 路由处理层

提供 Flask 路由处理函数。采用字典分发模式，根据 (language, chart_type)
将请求分发到对应的处理函数，避免 if-elif 链。

职责:
  1. 从 HTTP 请求中提取和校验参数
  2. 调用 services 层的图表生成和统计计算
  3. 组装 JSON 响应返回前端
"""

import numpy as np
from flask import request, jsonify

from services.chart_generator import (
    generate_line_chart, generate_bar_chart, generate_histogram,
    generate_pie_chart, generate_boxplot, generate_scatter_chart
)
from services.statistics import compute_stats, compute_bar_stats
from utils.helpers import format_data, debug_print, parse_float_list, parse_number

# ================================================================
# 通用参数提取
# ================================================================

def extract_common_params(req_json):
    """
    从请求 JSON 中提取所有图表类型共用的通用参数。

    Returns:
        dict: 清洗后的通用参数字典
    """
    return {
        'title':        req_json.get('title', ''),
        'title_size':   parse_number(req_json.get('title_size'), 16, int),
        'xlabel':       req_json.get('xlabel', ''),
        'ylabel':       req_json.get('ylabel', ''),
        'label_size':   parse_number(req_json.get('label_size'), 12, int),
        'legend_pos':   req_json.get('legend_pos', 'best'),
        'legend_size':  parse_number(req_json.get('legend_size'), 10, int),
        'fig_width':    parse_number(req_json.get('fig_width'), 10, float),
        'fig_height':   parse_number(req_json.get('fig_height'), 6, float),
        'figsize':      (parse_number(req_json.get('fig_width'), 10, float),
                         parse_number(req_json.get('fig_height'), 6, float)),
        'dpi':          parse_number(req_json.get('dpi'), 100, int),
        'grid':         req_json.get('grid', True),
        'grid_style':   req_json.get('grid_style', '--'),
        'grid_alpha':   parse_number(req_json.get('grid_alpha'), 0.5, float),
        'bg_color':     req_json.get('bg_color', '#FFFFFF'),
        'x_log':        req_json.get('x_log', False),
        'y_log':        req_json.get('y_log', False),
    }


def _get_json(key, default=None):
    """便捷地从 request.json 获取参数"""
    return request.json.get(key, default) if request.json else default


# ================================================================
# 数据预处理
# ================================================================

def preprocess_xy(x_raw, y_raw):
    """
    预处理 x, y 原始输入数据。
    - 若只有 x（无 y），则 y=x，x=索引
    - 按 x 排序
    - 返回 numpy 数组
    """
    x_arr = np.array(x_raw)
    y_arr = np.array(y_raw) if y_raw and len(y_raw) > 0 else np.array([])

    if len(y_arr) == 0:
        y_arr = x_arr.copy()
        x_arr = np.arange(len(x_arr), dtype=float)

    sort_idx = np.argsort(x_arr)
    return x_arr[sort_idx], y_arr[sort_idx]


# ================================================================
# Python 处理 - 各图表类型
# ================================================================

def handle_python_line():
    """Python 折线图处理"""
    x_raw = _get_json('x', [])
    y_raw = _get_json('y', [])
    has_y = bool(y_raw and len(y_raw) > 0)

    x, y = preprocess_xy(x_raw, y_raw)
    params = extract_common_params(request.json)

    # 折线图专属参数
    params.update({
        'color':          _get_json('color', '#3366CC'),
        'linewidth':      parse_number(_get_json('linewidth'), 2.0, float),
        'linestyle':      _get_json('linestyle', 'solid'),
        'marker':         _get_json('marker', 'none'),
        'markersize':     parse_number(_get_json('markersize'), 6, float),
        'marker_color':   _get_json('marker_color', _get_json('color', '#3366CC')),
        'alpha':          parse_number(_get_json('alpha'), 1.0, float),
        'cumulative':     _get_json('cumulative', False),
        'label':          _get_json('label', '数据'),
    })

    chart_image = generate_line_chart(x, y, **params)
    stats = compute_stats(x, y, has_y=has_y)

    cumsum_data = np.cumsum(y).tolist() if _get_json('cumulative', False) else None

    return jsonify({
        'x':          format_data(x.tolist()),
        'y':          format_data(y.tolist()),
        'x_data':     format_data(x.tolist()),
        'y_data':     format_data(y.tolist()),
        'cumsum':     format_data(cumsum_data),
        'chartImage': chart_image,
        **stats
    })


def handle_python_bar():
    """Python 柱状图处理"""
    x_raw = _get_json('x', [])
    y_raw = _get_json('y', [])

    x = x_raw  # 柱状图 x 可能是字符串类别，不作为数值处理
    y = np.array(y_raw) if y_raw else np.array([])
    params = extract_common_params(request.json)

    params.update({
        'color':       _get_json('color', '#3366CC'),
        'width':       parse_number(_get_json('width'), 0.8, float),
        'alpha':       parse_number(_get_json('alpha'), 0.8, float),
        'edge_color':  _get_json('edge_color', '#333333'),
        'edge_width':  parse_number(_get_json('edge_width'), 0.5, float),
        'orientation': _get_json('orientation', 'vertical'),
        'label':       _get_json('label', '数据'),
    })

    chart_image = generate_bar_chart(x, y, **params)
    stats = compute_bar_stats(x, y)

    return jsonify({
        'x':          x,
        'y':          format_data(y.tolist()),
        'chartImage': chart_image,
        **stats
    })


def handle_python_histogram():
    """Python 直方图处理"""
    data_groups_raw = _get_json('y', [[]])
    bins = _get_json('bins', 10)
    params = extract_common_params(request.json)

    # 将列表数据转为 numpy 数组列表
    data_groups = [np.array(g) for g in data_groups_raw if g and len(g) > 0]

    params.update({
        'bins':        bins,
        'histtype':    _get_json('histtype', 'bar'),
        'color':       _get_json('color', ''),
        'alpha':       parse_number(_get_json('alpha'), 0.8, float),
        'density':     _get_json('density', False),
        'orientation': _get_json('orientation', 'vertical'),
        'cumulative':  _get_json('cumulative', False),
        'y_log':       _get_json('logScale', False),
        'edge_color':  _get_json('edge_color', '#333333'),
        'linewidth':   parse_number(_get_json('linewidth'), 1.0, float),
    })

    chart_image = generate_histogram(data_groups, **params)

    return jsonify({
        'chartImage': chart_image
    })


def handle_python_pie():
    """Python 饼图处理"""
    labels = _get_json('labels', [])
    values = _get_json('values', [])
    params = extract_common_params(request.json)

    # 解析 explode
    explode_raw = _get_json('explode', '')
    explode = parse_float_list(explode_raw) if explode_raw else None

    params.update({
        'color':               _get_json('color', ''),
        'explode':             explode,
        'shadow':              _get_json('shadow', False),
        'start_angle':         parse_number(_get_json('start_angle'), 0, float),
        'autopct':             _get_json('autopct', '%1.1f%%'),
        'label_distance':      parse_number(_get_json('label_distance'), 1.1, float),
        'donut':               parse_number(_get_json('donut'), 0, float),
        'text_size':           parse_number(_get_json('text_size'), 12, int),
        'wedge_edge_color':    _get_json('wedge_edge_color', 'white'),
        'wedge_edge_width':    parse_number(_get_json('wedge_edge_width'), 1, float),
    })

    chart_image = generate_pie_chart(labels, values, **params)

    return jsonify({'chartImage': chart_image})


def handle_python_boxplot():
    """Python 箱线图处理"""
    data_groups_raw = _get_json('data_groups', [[]])
    params = extract_common_params(request.json)

    data_groups = [np.array(g) for g in data_groups_raw if g and len(g) > 0]
    labels = _get_json('labels', None)

    params.update({
        'labels':         labels,
        'notch':          _get_json('notch', False),
        'show_means':     _get_json('show_means', False),
        'show_outliers':  _get_json('show_outliers', True),
        'orientation':    _get_json('orientation', 'vertical'),
        'color':          _get_json('color', '#3366CC'),
        'widths':         parse_number(_get_json('widths'), 0.5, float),
        'patch_artist':   _get_json('patch_artist', False),
        'alpha':          parse_number(_get_json('alpha'), 0.6, float),
        'edge_color':     _get_json('edge_color', '#333333'),
    })

    chart_image = generate_boxplot(data_groups, **params)

    return jsonify({'chartImage': chart_image})


def handle_python_scatter():
    """Python 散点图处理"""
    x_raw = _get_json('x', [])
    y_raw = _get_json('y', [])
    x, y = preprocess_xy(x_raw, y_raw)
    has_y = bool(y_raw and len(y_raw) > 0)

    params = extract_common_params(request.json)

    # 颜色：如果是数值列表则用于颜色映射
    c_raw = _get_json('c', '#3366CC')

    params.update({
        's':           parse_number(_get_json('s'), 20, float),
        'c':           c_raw,
        'marker':      _get_json('marker', 'o'),
        'alpha':       parse_number(_get_json('alpha'), 0.8, float),
        'edge_color':  _get_json('edge_color', None),
        'linewidth':   parse_number(_get_json('linewidth'), 0, float),
        'cmap':        _get_json('cmap', None),
        'colorbar':    _get_json('colorbar', False),
    })

    chart_image = generate_scatter_chart(x, y, **params)
    stats = compute_stats(x, y, has_y=has_y)

    return jsonify({
        'x':          format_data(x.tolist()),
        'y':          format_data(y.tolist()),
        'chartImage': chart_image,
        **stats
    })


# ================================================================
# JS 处理 - 折线图（Chart.js 前端渲染，后端只做统计+预处理）
# ================================================================

def handle_js_line():
    """
    JS 折线图处理。后端负责数据预处理和统计计算，返回数据供
    Chart.js 在前端渲染。
    """
    x_raw = _get_json('x', [])
    y_raw = _get_json('y', [])
    has_y = bool(y_raw and len(y_raw) > 0)

    x, y = preprocess_xy(x_raw, y_raw)

    # 累积和
    cumsum_data = None
    x_data, y_data = x.copy(), y.copy()
    if _get_json('cumulative', False):
        cumsum_data = np.cumsum(y)

    # 对数变换
    if _get_json('x_log', False):
        x_data = np.log10(x_data + 1e-10)

    stats = compute_stats(x, y, has_y=has_y)

    return jsonify({
        'x':          format_data(x.tolist()),
        'y':          format_data(y.tolist()),
        'x_data':     format_data(x_data.tolist()),
        'y_data':     format_data(y_data.tolist()),
        'cumsum':     format_data(cumsum_data.tolist()) if cumsum_data is not None else None,
        'chartImage': None,
        **stats
    })


# ================================================================
# 路由注册
# ================================================================

# 字典分发：key = (language, chart_type) → handler
HANDLERS = {
    ('python', 'line'):      handle_python_line,
    ('python', 'bar'):       handle_python_bar,
    ('python', 'histogram'): handle_python_histogram,
    ('python', 'pie'):       handle_python_pie,
    ('python', 'boxplot'):   handle_python_boxplot,
    ('python', 'scatter'):   handle_python_scatter,
    ('js', 'line'):          handle_js_line,
}


def dispatch_process():
    """
    统一的 /process 路由处理入口。
    根据请求中的 Language 和 chartType 字典分发到对应的处理函数。
    """
    try:
        debug_print(request.json)

        language  = _get_json('Language', 'python').lower()
        chart_type = _get_json('chartType', 'line').lower()

        handler = HANDLERS.get((language, chart_type))
        if handler is None:
            return jsonify({
                'error': f'不支持的图表类型: Language={language}, chartType={chart_type}'
            }), 400

        return handler()

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'服务器处理错误: {str(e)}'}), 500
