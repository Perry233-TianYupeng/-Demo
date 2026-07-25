"""
utils/helpers.py — 通用工具函数

提供数值格式化、路径处理、颜色解析、字符串/列表转换等基础函数。
所有函数均为纯函数，不依赖全局状态，可在任何模块中安全调用。
"""

import os
import sys


def format_data(data):
    """
    格式化数值数据，保留小数点后3位。

    Args:
        data: 单个数值、数值列表 或 None

    Returns:
        格式化后的数据（类型与输入一致），None 则返回 None

    Examples:
        >>> format_data([1.23456, 2.0])
        [1.235, 2.0]
        >>> format_data(3.1415926)
        3.142
        >>> format_data(None)
        None
    """
    if data is None:
        return None
    if isinstance(data, list):
        return [round(float(num), 3) if isinstance(num, (int, float)) else num
                for num in data]
    return round(float(data), 3)


def resource_path(relative_path):
    """
    获取资源文件的绝对路径，兼容 PyInstaller 打包和开发环境。

    PyInstaller 打包后，资源文件会被解压到 sys._MEIPASS 临时目录；
    开发环境下则相对于当前文件所在目录查找。

    Args:
        relative_path: 相对路径字符串

    Returns:
        资源的绝对路径
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def parse_color(color_str, default='#3366CC'):
    """
    解析颜色字符串，处理空值和非法输入。

    Args:
        color_str: 颜色字符串（如 '#FF0000', 'blue', '', None）
        default:  颜色无效时返回的默认颜色

    Returns:
        有效的颜色字符串
    """
    if not color_str or not isinstance(color_str, str):
        return default
    color_str = color_str.strip()
    if not color_str:
        return default
    return color_str


def parse_float_list(s, sep=','):
    """
    将分隔符分隔的字符串解析为浮点数列表。

    Args:
        s:   输入字符串，如 "1, 2, 3" 或 "0.1 0.2 0.3"
        sep: 分隔符，默认逗号（同时支持空格）

    Returns:
        float 列表；解析失败返回空列表

    Examples:
        >>> parse_float_list("1, 2.5, 3")
        [1.0, 2.5, 3.0]
        >>> parse_float_list("")
        []
        >>> parse_float_list("abc")
        []
    """
    if not s or not isinstance(s, str):
        return []
    s = s.strip()
    if not s:
        return []
    # 同时支持逗号、中文逗号、空格分隔
    import re
    parts = re.split(r'[,，\s]+', s)
    result = []
    for p in parts:
        p = p.strip()
        if p:
            try:
                result.append(float(p))
            except ValueError:
                continue
    return result


def parse_number(value, default=0.0, value_type=float):
    """
    安全地将字符串解析为数值，失败返回默认值。

    Args:
        value:      输入值
        default:    解析失败时的默认值
        value_type: 期望的数值类型 (float 或 int)

    Returns:
        解析后的数值
    """
    if value is None:
        return default
    try:
        return value_type(value)
    except (ValueError, TypeError):
        return default


def debug_print(data):
    """
    调试日志输出（后续可升级为 logging 模块）。

    Args:
        data: 要打印的调试信息
    """
    print("--------Debug Info---------")
    print(data)
