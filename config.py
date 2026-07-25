"""
config.py — 数据可视化系统配置中心

集中管理所有配置常量：字体、图表默认值、下拉选项列表、服务器配置等。
修改此文件即可全局调整默认行为。
"""

# ============================================================
# 字体设置
# ============================================================
FONT_FAMILY = 'SimHei'            # 中文字体（Windows 系统自带）
FONT_SIZE_TITLE = 16              # 标题字号
FONT_SIZE_LABEL = 12              # 轴标签字号
FONT_SIZE_LEGEND = 10             # 图例字号
FONT_SIZE_TICK = 10               # 刻度字号

# ============================================================
# 图表默认参数
# ============================================================
DEFAULT_FIGSIZE = (10, 6)         # 图片尺寸（英寸）
DEFAULT_DPI = 100                 # 分辨率
DEFAULT_TITLE_SIZE = 16           # 标题字号
DEFAULT_LABEL_SIZE = 12           # 轴标签字号
DEFAULT_LEGEND_SIZE = 10          # 图例字号
DEFAULT_LINE_WIDTH = 2.0          # 线条宽度
DEFAULT_MARKER_SIZE = 6           # 标记大小
DEFAULT_BAR_WIDTH = 0.8           # 柱子宽度
DEFAULT_ALPHA = 0.8               # 默认透明度
DEFAULT_GRID_ALPHA = 0.5          # 网格透明度
DEFAULT_GRID_STYLE = '--'         # 网格线型 (matplotlib格式)
DEFAULT_BG_COLOR = '#FFFFFF'      # 背景色
DEFAULT_EDGE_COLOR = '#333333'    # 边框颜色
DEFAULT_EDGE_WIDTH = 0.5          # 边框宽度
DEFAULT_SCATTER_SIZE = 20         # 散点大小
DEFAULT_PIE_TEXT_SIZE = 12        # 饼图文字大小

# 多组数据默认颜色（10色调色板）
DEFAULT_COLORS = [
    '#3366CC', '#DC3912', '#FF9900', '#109618', '#990099',
    '#0099C6', '#DD4477', '#66AA00', '#B82E2E', '#316395'
]

# ============================================================
# UI 下拉框选项（供前端渲染和后端校验共用）
# ============================================================
LINE_STYLES = ['solid', 'dashed', 'dotted', 'dashdot']
MARKERS = ['o', 's', '^', 'v', 'D', 'p', '*', '+', 'x', 'none']
LEGEND_POSITIONS = ['best', 'upper right', 'upper left',
                    'lower left', 'lower right', 'center']
GRID_STYLES = ['solid', 'dashed', 'dotted', 'dashdot']
HISTTYPES = ['bar', 'barstacked', 'step', 'stepfilled']
ORIENTATIONS = ['vertical', 'horizontal']
PIE_LABEL_FORMATS = ['%1.1f%%', '%.0f', '%.1f%%', 'value']
CMAPS = ['viridis', 'plasma', 'inferno', 'magma',
         'coolwarm', 'RdBu', 'Set1', 'Set2', 'Set3']

# ============================================================
# 服务器配置
# ============================================================
HOST = '127.0.0.1'
PORT = 5000
DEBUG = True

# ============================================================
# 桌面窗口配置
# ============================================================
WINDOW_TITLE = '数据可视化系统'
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
