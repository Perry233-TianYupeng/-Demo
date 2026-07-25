# 📊 数据可视化系统

基于 **Python + Flask + Matplotlib + PyWebView + Chart.js** 开发的桌面数据可视化工具。无需编写代码，通过 GUI 表单即可完成专业级图表的定制与生成。

---

## ✨ 功能特性

- **6 种图表类型**：折线图、柱状图、直方图、饼图（含环形图）、箱线图、散点图 — 全部可用
- **双引擎渲染**：Python (Matplotlib) 生成静态图片 / JavaScript (Chart.js) 动态渲染
- **丰富的可调参数**：15 项通用设置 + 每种图表 6~12 项专属参数，全部通过颜色选择器、下拉框、滑块等可视化控件操作
- **统计指标自动计算**：均值、标准差、最大值、最小值一目了然
- **桌面原生窗口**：基于 PyWebView，无需浏览器，独立窗口运行
- **模块化架构**：服务层 / 路由层 / 工具层清晰分离，易于扩展和维护

---

## 🖥️ 支持的图表类型

| 图表 | 可调参数 |
|------|------|
| 📈 **折线图** | 线条颜色、宽度、线型（实线/虚线/点线/点划线）、标记样式/大小/颜色、透明度、累加线、对数轴 |
| 📊 **柱状图** | 填充颜色、柱子宽度、透明度、边框颜色/宽度、方向（垂直/水平） |
| 📋 **直方图** | 分箱数量/边界、堆叠/阶梯/填充模式、密度归一化、累积、边框颜色/宽度 |
| 🥧 **饼图 / 环形图** | 每扇区颜色、起始角度、扇区分离(explode)、阴影、标签格式、环形内径(0=饼图,>0=环形)、文字大小 |
| 📦 **箱线图** | 箱子颜色、缺口(中位数CI)、显示均值、显示异常值、颜色填充、方向 |
| 🔵 **散点图** | 点大小、颜色（单色或数值映射）、标记样式、透明度、颜色映射方案(viridis/plasma等)、颜色条 |

> 所有图表均支持：标题(含字号)、轴标签(含字号)、图例(位置/字号)、网格(线型/透明度)、背景色、图片尺寸(英寸)、分辨率(DPI)、X/Y 对数刻度。

---

## 📁 项目结构

```
learning01/
├── main.py                        # 🖥️ 桌面入口：PyWebView 启动 Flask + 窗口
├── app.py                         # 🌐 Flask 应用工厂：创建 app + 注册路由
├── config.py                      # ⚙️ 全局配置：字体、默认值、选项列表、服务器参数
├── requirements.txt               # 📦 Python 依赖清单
├── .gitignore
│
├── services/                      # 🔧 业务逻辑层（纯函数，无 Flask 依赖）
│   ├── chart_generator.py         #    6 种图表的 Matplotlib 生成函数
│   └── statistics.py              #    统计指标计算（均值/标准差/极值）
│
├── routes/                        # 🧭 路由层（HTTP 参数 → Service → JSON 响应）
│   └── chart_routes.py            #    字典分发模式 + 参数提取与校验
│
├── utils/                         # 🛠️ 工具层
│   └── helpers.py                 #    format_data, resource_path, parse_color 等
│
├── static/
│   ├── css/style.css              # 🎨 样式：Tab 栏 / 卡片 / 折叠面板 / 响应式
│   └── js/
│       ├── api.js                 # 📡 统一 fetch 封装 + 各图表参数收集
│       ├── charts.js              # 📈 Chart.js / Matplotlib 图片渲染切换
│       ├── ui.js                  # 🖱️ Tab 切换 + 面板显隐 + 统计清空
│       └── main.js                # 🎯 6 种图表 sendData_*() 入口函数
│
└── templates/
    └── index.html                 # 📄 前端页面（Tab 布局 + 完整参数表单 + 统计区）
```

### 各文件职责速查

| 文件 | 一句话职责 |
|------|-----------|
| `main.py` | 启动 Flask 后台线程 + 创建 PyWebView 桌面窗口 |
| `app.py` | 创建 Flask 实例，注册 `/` 和 `/process` 两条路由 |
| `config.py` | 集中管理所有配置常量，改一处全局生效 |
| `services/chart_generator.py` | 接收数据+参数，返回 base64 编码的 PNG 图片 |
| `services/statistics.py` | `compute_stats()` 统一计算统计指标，消除重复代码 |
| `routes/chart_routes.py` | 字典 `HANDLERS[(lang, type)]` 分发请求，提取校验参数 |
| `utils/helpers.py` | 数值格式化、PyInstaller 路径兼容、颜色解析等 |
| `static/js/api.js` | `sendRequest(chartType)` 收集表单→POST→返回 Promise |
| `static/js/charts.js` | Chart.js Canvas / Matplotlib 图片自动切换显示 |
| `static/js/ui.js` | Tab 切换、面板显隐、通用设置折叠展开 |
| `static/js/main.js` | 数据校验 + 调用 api + 渲染图表 + 显示统计 |
| `templates/index.html` | Tab 式布局，6 个图表面板 + 15 项通用设置 + 统计区 |

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Windows / macOS / Linux

### 安装依赖

```bash
pip install flask numpy matplotlib pywebview
```

或使用 conda：

```bash
conda create -n viz python=3.12
conda activate viz
pip install flask numpy matplotlib pywebview
```

### 启动应用

```bash
python main.py
```

应用将自动打开桌面窗口。在窗口中：
1. 点击顶部 **Tab 标签页** 选择图表类型
2. 在 **数据输入区** 填入数据（逗号、空格、换行均可分隔）
3. 调整 **图表样式** 参数（颜色选择器、下拉框、滑块）
4. 展开 **通用设置** 配置标题、标签、图例、网格等
5. 点击 **「🚀 生成图表」** 按钮
6. 查看下方 **统计结果** 和 **图表**

---

## 🎨 图表参数速查

### 通用参数（所有图表适用）

| 参数 | 控件类型 | 默认值 |
|------|---------|--------|
| 图表标题 / X轴标签 / Y轴标签 | 文本框 | 空 |
| 标题字号 / 轴标签字号 | 数字框 | 16 / 12 |
| 图片宽度 / 高度（英寸） | 数字框 | 10 × 6 |
| 分辨率 DPI | 数字框 | 100 |
| 图例位置 | 下拉框 | 自动最佳 |
| 图例字号 | 数字框 | 10 |
| 显示网格 / 网格线型 / 网格透明度 | 复选框 + 下拉 + 滑块 | 开启 / 虚线 / 0.5 |
| 背景色 | 颜色选择器 🎨 | #FFFFFF |
| X轴对数 / Y轴对数 | 复选框 | 关闭 |

### 各图表专属参数

**折线图** — 线条颜色 🎨 · 线宽 · 线型(实线/虚线/点线/点划线) · 标记样式(○□△◇☆＋×) · 标记大小 · 标记颜色 🎨 · 透明度 · 累加线

**柱状图** — 填充颜色 🎨 · 柱子宽度 · 透明度 · 边框颜色 🎨 · 边框宽度 · 方向(垂直/水平)

**直方图** — 分箱模式(数量/边界) · 类型(普通/堆叠/阶梯/填充阶梯) · 颜色 · 透明度 · 密度归一化 · 累积 · 边框

**饼图** — 颜色列表 · 起始角度 · 扇区分离(explode) · 阴影 · 标签格式 · 环形内径(0=饼图, 0.4=环形) · 文字大小 · 边框

**箱线图** — 箱子颜色 🎨 · 缺口(中位数CI) · 显示均值 · 异常值 · 方向 · 颜色填充

**散点图** — 点大小 · 颜色(单色/数值映射) · 标记样式 · 透明度 · 边框 · 颜色映射方案(viridis/plasma/coolwarm/RdBu) · 颜色条

---

## 🔧 自定义配置

编辑 `config.py` 可修改全局默认值：

```python
FONT_FAMILY = 'SimHei'          # 中文字体（macOS 可改为 'PingFang SC'）
DEFAULT_COLORS = [...]           # 多组数据默认色板
HOST = '127.0.0.1'              # 服务器地址
PORT = 5000                     # 服务器端口
WINDOW_TITLE = '数据可视化系统'  # 窗口标题
WINDOW_WIDTH = 1200             # 窗口宽度
WINDOW_HEIGHT = 900             # 窗口高度
```

---

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| [Flask](https://flask.palletsprojects.com/) | Web 框架，处理前后端通信 |
| [Matplotlib](https://matplotlib.org/) | Python 端图表生成引擎 |
| [NumPy](https://numpy.org/) | 数值计算与数据处理 |
| [Chart.js](https://www.chartjs.org/) | JavaScript 端动态图表渲染 |
| [PyWebView](https://pywebview.flowrl.com/) | 将 Web 应用包装为跨平台桌面窗口 |

---

## 📝 许可证

本项目仅供学习交流使用。

---

## 👤 作者

**Perry233** — 非计算机科班专业，本项目作为前后端练手之作，不定期更新。
