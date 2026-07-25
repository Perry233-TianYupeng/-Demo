"""
services/statistics.py — 统计计算服务

提供统一的统计指标计算函数。所有函数均为纯函数，接收 numpy 数组，
返回格式化后的统计指标字典，供路由层直接序列化为 JSON 响应。
"""

import numpy as np
from utils.helpers import format_data


def compute_stats(x, y, has_y=True):
    """
    统一计算 x 和 y 的统计指标。

    Args:
        x:     numpy 数组，x 轴数据
        y:     numpy 数组或 None，y 轴数据
        has_y: bool，是否有 y 数据

    Returns:
        dict: {
            'xmean', 'xstd', 'xmax', 'xmin',
            'ymean', 'ystd', 'ymax', 'ymin'  （has_y=False 时 y 字段为 None）
        }
    """
    stats = {
        'xmean': format_data(float(x.mean())),
        'xstd':  format_data(float(x.std())),
        'xmax':  format_data(float(x.max())),
        'xmin':  format_data(float(x.min())),
    }

    if has_y and y is not None and len(y) > 0:
        stats.update({
            'ymean': format_data(float(y.mean())),
            'ystd':  format_data(float(y.std())),
            'ymax':  format_data(float(y.max())),
            'ymin':  format_data(float(y.min())),
        })
    else:
        stats.update({
            'ymean': None, 'ystd': None, 'ymax': None, 'ymin': None
        })

    return stats


def compute_bar_stats(x, y):
    """
    计算柱状图的统计指标（含 x 类别数）。

    Args:
        x: x 轴类别数据
        y: numpy 数组，y 轴数值

    Returns:
        dict: { 'xlength', 'ymean', 'ystd', 'ymax', 'ymin' }
    """
    return {
        'xlength': len(set(x)),
        'ymean':   format_data(float(y.mean())),
        'ystd':    format_data(float(y.std())),
        'ymax':    format_data(float(y.max())),
        'ymin':    format_data(float(y.min())),
    }
