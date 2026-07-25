/**
 * charts.js — 图表渲染层
 *
 * 负责图表的显示与切换：
 *   - Chart.js 折线图渲染（JS 模式）
 *   - matplotlib 图片显示（Python 模式）
 *   - 图表实例管理
 */

let chartInstance = null;  // Chart.js 实例引用

/**
 * 使用 Chart.js 绘制折线图。
 *
 * @param {number[]} x         - X 轴标签
 * @param {number[]} y         - Y 轴数据
 * @param {number[]} cumsumData - 累积和数组（可选）
 * @param {boolean} cumulative  - 是否显示累积线
 */
function drawChartJs(x, y, cumsumData, cumulative) {
    const ctx = document.getElementById('myChart');
    showCanvas();

    if (chartInstance) {
        chartInstance.destroy();
        chartInstance = null;
    }

    const datasets = [{
        label: '原始数据',
        data: y,
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderWidth: 2,
        tension: 0.1,
    }];

    if (cumulative && cumsumData) {
        datasets.push({
            label: '累积和',
            data: cumsumData,
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2,
            tension: 0.1,
        });
    }

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: { labels: x, datasets: datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    });
}

/**
 * 显示 matplotlib 生成的 base64 图片。
 *
 * @param {string} chartImage - base64 编码的 PNG 图片数据
 */
function showMatplotlibImage(chartImage) {
    const matplotlibDiv = document.getElementById('matplotlibChart');
    const matplotlibImg = document.getElementById('matplotlibImage');

    matplotlibImg.src = 'data:image/png;base64,' + chartImage;
    matplotlibDiv.style.display = 'flex';
    document.getElementById('myChart').style.display = 'none';

    if (chartInstance) {
        chartInstance.destroy();
        chartInstance = null;
    }
}

/**
 * 显示 Chart.js Canvas，隐藏 matplotlib 图片区。
 */
function showCanvas() {
    document.getElementById('matplotlibChart').style.display = 'none';
    document.getElementById('myChart').style.display = 'block';
}

/**
 * 清除所有图表（Chart.js 实例 + matplotlib 图片）。
 */
function clearChart() {
    if (chartInstance) {
        chartInstance.destroy();
        chartInstance = null;
    }
    document.getElementById('matplotlibImage').src = '';
    document.getElementById('matplotlibChart').style.display = 'none';
    document.getElementById('myChart').style.display = 'block';
}

/**
 * 根据后端返回结果自动选择渲染方式。
 *
 * @param {object} result - 后端 JSON 响应
 */
function renderChart(result) {
    if (result.error) {
        document.getElementById('resultMsg').innerText = '错误: ' + result.error;
        return;
    }

    if (result.chartImage) {
        // matplotlib 图片
        showMatplotlibImage(result.chartImage);
    } else if (result.x_data && result.y_data) {
        // Chart.js 折线图
        drawChartJs(result.x_data, result.y_data, result.cumsum, result.cumsum && result.cumsum.length > 0);
    }
}
