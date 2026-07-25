"""
services/chart_generator.py — 图表生成服务

提供 6 种图表类型的纯 matplotlib 生成函数。
所有函数均为纯函数：接收数据和参数，返回 base64 编码的 PNG 图片字符串。
不依赖 Flask 的 request/response，可被任何调用方使用。

支持的图表类型：
  - line:      折线图
  - bar:       柱状图
  - histogram: 直方图
  - pie:       饼图 / 环形图
  - boxplot:   箱线图
  - scatter:   散点图
"""

import io
import base64
import traceback

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from config import (
    FONT_FAMILY, DEFAULT_FIGSIZE, DEFAULT_DPI, DEFAULT_COLORS,
    DEFAULT_TITLE_SIZE, DEFAULT_LABEL_SIZE, DEFAULT_LEGEND_SIZE,
    DEFAULT_LINE_WIDTH, DEFAULT_MARKER_SIZE, DEFAULT_BAR_WIDTH,
    DEFAULT_ALPHA, DEFAULT_GRID_ALPHA, DEFAULT_BG_COLOR,
    DEFAULT_EDGE_COLOR, DEFAULT_EDGE_WIDTH, DEFAULT_SCATTER_SIZE,
    DEFAULT_PIE_TEXT_SIZE,
)

# 全局字体设置
plt.rcParams['font.sans-serif'] = [FONT_FAMILY]
plt.rcParams['axes.unicode_minus'] = False


def _fig_to_base64(fig):
    """将 matplotlib Figure 对象转为 base64 PNG 字符串"""
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', dpi=DEFAULT_DPI, bbox_inches='tight')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    plt.close(fig)
    return img_str


def _setup_common(fig, ax, params):
    """
    应用通用图表设置：标题、轴标签、图例、网格、背景色、对数轴等。

    Args:
        fig:    matplotlib Figure 对象
        ax:     matplotlib Axes 对象
        params: dict，包含所有通用参数
    """
    # 标题
    title = params.get('title', '')
    if title:
        ax.set_title(title, fontsize=params.get('title_size', DEFAULT_TITLE_SIZE))

    # 轴标签
    xlabel = params.get('xlabel', '')
    ylabel = params.get('ylabel', '')
    label_size = params.get('label_size', DEFAULT_LABEL_SIZE)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=label_size)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=label_size)

    # 网格
    if params.get('grid', True):
        grid_style = params.get('grid_style', '--')
        grid_alpha_val = params.get('grid_alpha', DEFAULT_GRID_ALPHA)
        ax.grid(True, linestyle=grid_style, alpha=grid_alpha_val)

    # 对数轴
    if params.get('x_log', False):
        ax.set_xscale('log')
    if params.get('y_log', False):
        ax.set_yscale('log')

    # 背景色
    bg_color = params.get('bg_color', DEFAULT_BG_COLOR)
    if bg_color:
        try:
            fig.patch.set_facecolor(bg_color)
            ax.set_facecolor(bg_color)
        except ValueError:
            pass  # 无效颜色忽略


def _setup_legend(ax, params):
    """设置图例（如果有）"""
    legend_pos = params.get('legend_pos', 'best')
    legend_size = params.get('legend_size', DEFAULT_LEGEND_SIZE)
    if legend_pos and legend_pos != 'none':
        handles, labels = ax.get_legend_handles_labels()
        if handles:
            ax.legend(loc=legend_pos, fontsize=legend_size)


# ================================================================
# 折线图
# ================================================================
def generate_line_chart(x, y, **kwargs):
    """
    生成折线图。

    必需参数:
        x, y: numpy 数组

    可选参数（kwargs）:
        外观: color, linewidth, linestyle, marker, markersize, marker_color, alpha
        功能: cumulative (累积线), x_log, y_log
        通用: title, title_size, xlabel, ylabel, label_size,
              legend_pos, legend_size, grid, grid_style, grid_alpha,
              bg_color, figsize, dpi
    """
    try:
        figsize = kwargs.get('figsize', DEFAULT_FIGSIZE)
        dpi = kwargs.get('dpi', DEFAULT_DPI)
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

        color = kwargs.get('color', DEFAULT_COLORS[0])
        linewidth = kwargs.get('linewidth', DEFAULT_LINE_WIDTH)
        linestyle = kwargs.get('linestyle', 'solid')
        marker = kwargs.get('marker', 'none')
        markersize = kwargs.get('markersize', DEFAULT_MARKER_SIZE)
        marker_color = kwargs.get('marker_color', color)
        alpha = kwargs.get('alpha', 1.0)
        label = kwargs.get('label', '数据')

        ax.plot(x, y,
                color=color, linewidth=linewidth, linestyle=linestyle,
                marker=marker if marker != 'none' else '',
                markersize=markersize,
                markerfacecolor=marker_color,
                markeredgecolor=marker_color,
                alpha=alpha, label=label)

        # 累积和线
        if kwargs.get('cumulative', False):
            cumsum = np.cumsum(y)
            ax.plot(x, cumsum, color='#DC3912', linewidth=linewidth,
                    linestyle='--', label='累积和')

        _setup_common(fig, ax, kwargs)
        _setup_legend(ax, kwargs)

        return _fig_to_base64(fig)
    except Exception as e:
        traceback.print_exc()
        return None


# ================================================================
# 柱状图
# ================================================================
def generate_bar_chart(x, y, **kwargs):
    """
    生成柱状图。

    可选参数（kwargs）:
        外观: color, width, alpha, edge_color, edge_width, orientation
        通用参数同折线图
    """
    try:
        figsize = kwargs.get('figsize', DEFAULT_FIGSIZE)
        fig, ax = plt.subplots(figsize=figsize)

        color = kwargs.get('color', DEFAULT_COLORS[0])
        width = kwargs.get('width', DEFAULT_BAR_WIDTH)
        alpha = kwargs.get('alpha', DEFAULT_ALPHA)
        edge_color = kwargs.get('edge_color', DEFAULT_EDGE_COLOR)
        edge_width = kwargs.get('edge_width', DEFAULT_EDGE_WIDTH)
        orientation = kwargs.get('orientation', 'vertical')
        label = kwargs.get('label', '数据')

        if orientation == 'horizontal':
            ax.barh(x, y, height=width, alpha=alpha,
                    color=color, edgecolor=edge_color,
                    linewidth=edge_width, label=label)
        else:
            ax.bar(x, y, width=width, alpha=alpha,
                   color=color, edgecolor=edge_color,
                   linewidth=edge_width, label=label)

        _setup_common(fig, ax, kwargs)
        _setup_legend(ax, kwargs)

        return _fig_to_base64(fig)
    except Exception as e:
        traceback.print_exc()
        return None


# ================================================================
# 直方图
# ================================================================
def generate_histogram(data_groups, **kwargs):
    """
    生成直方图，支持多组数据。

    Args:
        data_groups: list of numpy arrays，每组一个数据集

    可选参数（kwargs）:
        bins, histtype, color, alpha, density, orientation,
        cumulative, y_log, edge_color, linewidth
    """
    try:
        figsize = kwargs.get('figsize', DEFAULT_FIGSIZE)
        fig, ax = plt.subplots(figsize=figsize)

        bins = kwargs.get('bins', 10)
        histtype = kwargs.get('histtype', 'bar')
        alpha = kwargs.get('alpha', DEFAULT_ALPHA)
        density = kwargs.get('density', False)
        orientation = kwargs.get('orientation', 'vertical')
        cumulative = kwargs.get('cumulative', False)
        log_y = kwargs.get('y_log', False)
        edge_color = kwargs.get('edge_color', DEFAULT_EDGE_COLOR)
        linewidth = kwargs.get('linewidth', 1.0)

        # 颜色处理
        colors = kwargs.get('color', DEFAULT_COLORS[:len(data_groups)])
        if isinstance(colors, str):
            colors = [colors]

        for i, data in enumerate(data_groups):
            c = colors[i % len(colors)] if colors else DEFAULT_COLORS[i % len(DEFAULT_COLORS)]
            ax.hist(
                data, bins=bins, histtype=histtype,
                density=density, orientation=orientation,
                cumulative=cumulative, color=c, alpha=alpha,
                edgecolor=edge_color, linewidth=linewidth,
                log=log_y, label=f'数据组 {i+1}'
            )

        _setup_common(fig, ax, kwargs)
        _setup_legend(ax, kwargs)

        return _fig_to_base64(fig)
    except Exception as e:
        traceback.print_exc()
        return None


# ================================================================
# 饼图 / 环形图
# ================================================================
def generate_pie_chart(labels, values, **kwargs):
    """
    生成饼图或环形图。

    Args:
        labels: 扇区标签列表
        values: 扇区数值列表

    可选参数（kwargs）:
        colors, explode, shadow, start_angle, autopct,
        label_distance, donut (内径0-1), text_size,
        wedge_edge_color, wedge_edge_width
    """
    try:
        figsize = kwargs.get('figsize', DEFAULT_FIGSIZE)
        fig, ax = plt.subplots(figsize=figsize)

        colors = kwargs.get('color', DEFAULT_COLORS[:len(values)])
        if isinstance(colors, str):
            colors = DEFAULT_COLORS[:len(values)]

        explode = kwargs.get('explode', None)
        shadow = kwargs.get('shadow', False)
        start_angle = kwargs.get('start_angle', 0)
        autopct = kwargs.get('autopct', '%1.1f%%')
        label_distance = kwargs.get('label_distance', 1.1)
        text_size = kwargs.get('text_size', DEFAULT_PIE_TEXT_SIZE)

        # 环形图内径
        donut = kwargs.get('donut', 0)
        wedgeprops = {'width': 1 - donut, 'edgecolor': 'white', 'linewidth': 1}
        if donut > 0:
            wedgeprops['width'] = 1 - donut

        # 边框
        edge_color = kwargs.get('wedge_edge_color', 'white')
        edge_width = kwargs.get('wedge_edge_width', 1)
        wedgeprops['edgecolor'] = edge_color
        wedgeprops['linewidth'] = edge_width

        wedges, texts, autotexts = ax.pie(
            values, labels=labels, colors=colors,
            explode=explode, shadow=shadow,
            startangle=start_angle, autopct=autopct,
            pctdistance=0.6, labeldistance=label_distance,
            wedgeprops=wedgeprops,
            textprops={'fontsize': text_size}
        )

        # 标题
        title = kwargs.get('title', '')
        if title:
            ax.set_title(title, fontsize=kwargs.get('title_size', DEFAULT_TITLE_SIZE))

        # 背景色
        bg_color = kwargs.get('bg_color', DEFAULT_BG_COLOR)
        if bg_color:
            try:
                fig.patch.set_facecolor(bg_color)
            except ValueError:
                pass

        return _fig_to_base64(fig)
    except Exception as e:
        traceback.print_exc()
        return None


# ================================================================
# 箱线图
# ================================================================
def generate_boxplot(data_groups, **kwargs):
    """
    生成箱线图。

    Args:
        data_groups: list of arrays，每组一个数据集

    可选参数（kwargs）:
        labels, notch, show_means, show_outliers,
        orientation, color, widths, patch_artist
    """
    try:
        figsize = kwargs.get('figsize', DEFAULT_FIGSIZE)
        fig, ax = plt.subplots(figsize=figsize)

        labels = kwargs.get('labels', None)
        notch = kwargs.get('notch', False)
        show_means = kwargs.get('show_means', False)
        show_outliers = kwargs.get('show_outliers', True)
        orientation = kwargs.get('orientation', 'vertical')
        color = kwargs.get('color', DEFAULT_COLORS[0])
        widths = kwargs.get('widths', 0.5)
        patch_artist = kwargs.get('patch_artist', False)

        vert = orientation != 'horizontal'

        bp = ax.boxplot(
            data_groups, labels=labels, notch=notch,
            showmeans=show_means, showfliers=show_outliers,
            vert=vert, widths=widths,
            patch_artist=patch_artist
        )

        # 颜色填充
        if patch_artist:
            for patch in bp['boxes']:
                patch.set_facecolor(color)
                patch.set_alpha(kwargs.get('alpha', 0.6))

        # 中位线颜色
        median_color = kwargs.get('edge_color', DEFAULT_EDGE_COLOR)
        for median in bp['medians']:
            median.set_color(median_color)

        _setup_common(fig, ax, kwargs)
        # 箱线图通常有自己的标签，不再重复设置图例

        return _fig_to_base64(fig)
    except Exception as e:
        traceback.print_exc()
        return None


# ================================================================
# 散点图
# ================================================================
def generate_scatter_chart(x, y, **kwargs):
    """
    生成散点图。

    可选参数（kwargs）:
        s (点大小), c (颜色), marker, alpha,
        edge_color, linewidth, cmap, colorbar
    """
    try:
        figsize = kwargs.get('figsize', DEFAULT_FIGSIZE)
        fig, ax = plt.subplots(figsize=figsize)

        s = kwargs.get('s', DEFAULT_SCATTER_SIZE)
        c = kwargs.get('c', DEFAULT_COLORS[0])
        marker = kwargs.get('marker', 'o')
        alpha = kwargs.get('alpha', DEFAULT_ALPHA)
        edge_color = kwargs.get('edge_color', None)
        linewidth = kwargs.get('linewidth', 0)
        cmap = kwargs.get('cmap', None)
        show_colorbar = kwargs.get('colorbar', False)

        scatter = ax.scatter(
            x, y, s=s, c=c, marker=marker, alpha=alpha,
            edgecolors=edge_color, linewidths=linewidth,
            cmap=cmap if c is not None and not isinstance(c, str) else None
        )

        # 颜色条
        if show_colorbar and c is not None and not isinstance(c, str):
            fig.colorbar(scatter, ax=ax)

        _setup_common(fig, ax, kwargs)
        _setup_legend(ax, kwargs)

        return _fig_to_base64(fig)
    except Exception as e:
        traceback.print_exc()
        return None
