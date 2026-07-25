/**
 * ui.js — UI 交互层
 *
 * 负责页面 UI 交互逻辑：
 *   - 图表类型 Tab 切换
 *   - 面板显隐控制
 *   - 通用设置区折叠/展开
 */

/**
 * 切换到指定的图表类型面板。
 * 隐藏所有面板，仅显示目标面板，更新 Tab 高亮。
 *
 * @param {string} chartType - 图表类型标识
 */
function switchChartTab(chartType) {
    // 隐藏所有面板
    const panels = document.querySelectorAll('.chart-panel');
    panels.forEach(p => p.style.display = 'none');

    // 显示目标面板
    const targetPanel = document.getElementById('panel-' + chartType);
    if (targetPanel) {
        targetPanel.style.display = 'block';
    }

    // 更新 Tab 高亮
    const tabs = document.querySelectorAll('.chart-tab');
    tabs.forEach(t => t.classList.remove('active'));
    const activeTab = document.getElementById('tab-' + chartType);
    if (activeTab) {
        activeTab.classList.add('active');
    }

    // 清除旧图表
    if (typeof clearChart === 'function') {
        clearChart();
    }
    // 清空统计结果
    clearStats();
}

/**
 * 切换通用设置区的折叠/展开状态。
 */
function toggleCommonSettings() {
    const body = document.getElementById('commonSettingsBody');
    const icon = document.getElementById('commonSettingsIcon');
    if (body.style.display === 'none') {
        body.style.display = 'block';
        if (icon) icon.textContent = '▲';
    } else {
        body.style.display = 'none';
        if (icon) icon.textContent = '▼';
    }
}

/**
 * 清空统计结果显示。
 */
function clearStats() {
    const statSpans = document.querySelectorAll('.stat-value');
    statSpans.forEach(s => s.innerText = '-');
    const resultEl = document.getElementById('resultMsg');
    if (resultEl) resultEl.innerText = '';
}

/**
 * 更新折线图/散点图统计结果。
 * @param {object} result - 后端返回的统计指标
 */
function updateLineStats(result) {
    document.getElementById('stat-xmean').innerText = result.xmean ?? '-';
    document.getElementById('stat-xstd').innerText = result.xstd ?? '-';
    document.getElementById('stat-xmax').innerText = result.xmax ?? '-';
    document.getElementById('stat-xmin').innerText = result.xmin ?? '-';
    document.getElementById('stat-ymean').innerText = result.ymean ?? '-';
    document.getElementById('stat-ystd').innerText = result.ystd ?? '-';
    document.getElementById('stat-ymax').innerText = result.ymax ?? '-';
    document.getElementById('stat-ymin').innerText = result.ymin ?? '-';
}

/**
 * 更新柱状图统计结果。
 * @param {object} result - 后端返回的统计指标
 */
function updateBarStats(result) {
    document.getElementById('stat-xlength').innerText = result.xlength ?? '-';
    document.getElementById('stat-ymean-bar').innerText = result.ymean ?? '-';
    document.getElementById('stat-ystd-bar').innerText = result.ystd ?? '-';
    document.getElementById('stat-ymax-bar').innerText = result.ymax ?? '-';
    document.getElementById('stat-ymin-bar').innerText = result.ymin ?? '-';
}

// 页面加载完成后默认选中折线图
document.addEventListener('DOMContentLoaded', function () {
    switchChartTab('line');
});
