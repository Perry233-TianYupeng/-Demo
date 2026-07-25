/**
 * main.js — 应用入口
 *
 * 绑定各图表面板的"生成图表"按钮事件，协调 api.js 和 charts.js 完成：
 *  1. 收集表单数据 → 2. 发送请求 → 3. 渲染图表 → 4. 显示统计结果
 */

// ================================================================
// 折线图
// ================================================================
function sendData_Line() {
    const xRaw = document.getElementById('lineXInput').value;
    const yRaw = document.getElementById('lineYInput').value;
    const xData = xRaw.trim() ? xRaw.split(/[,，\s]+/).map(Number) : [];
    const yData = yRaw.trim() ? yRaw.split(/[,，\s]+/).map(Number) : [];

    // 前端数据校验
    if (xData.length === 0 || xData.some(isNaN)) {
        document.getElementById('resultMsg').innerText = '错误：请输入有效的 x 数据';
        return;
    }
    if (yData.length > 0 && yData.some(isNaN)) {
        document.getElementById('resultMsg').innerText = '错误：请输入有效的 y 数据';
        return;
    }
    if (yData.length > 0 && xData.length !== yData.length) {
        document.getElementById('resultMsg').innerText = '错误：x 和 y 数据长度不匹配';
        return;
    }

    const language = document.querySelector('input[name="lineLanguage"]:checked')?.value || 'python';

    sendRequest('line')
        .then(result => {
            updateLineStats(result);

            if (language === 'js' && result.x_data && result.y_data) {
                drawChartJs(result.x_data, result.y_data, result.cumsum, result.cumsum && result.cumsum.length > 0);
                document.getElementById('resultMsg').innerText = `JS渲染完成 — x: ${result.x?.slice(0, 3)}...`;
            } else if (result.chartImage) {
                showMatplotlibImage(result.chartImage);
                document.getElementById('resultMsg').innerText = `图表生成成功 — x: ${result.x?.slice(0, 3)}... y: ${result.y?.slice(0, 3)}...`;
            } else {
                document.getElementById('resultMsg').innerText = '图表生成成功';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('resultMsg').innerText = '请求失败：' + error.message;
        });
}

// ================================================================
// 柱状图
// ================================================================
function sendData_Bar() {
    const xRaw = document.getElementById('barXInput').value;
    const yRaw = document.getElementById('barYInput').value;
    const xData = xRaw.trim() ? xRaw.split(/[,，\s]+/) : [];
    const yData = yRaw.trim() ? yRaw.split(/[,，\s]+/).map(Number) : [];

    if (xData.length === 0) {
        document.getElementById('resultMsg').innerText = '错误：请输入有效的 x 数据';
        return;
    }
    if (yData.length === 0 || yData.some(isNaN)) {
        document.getElementById('resultMsg').innerText = '错误：请输入有效的 y 数据';
        return;
    }
    if (xData.length !== yData.length) {
        document.getElementById('resultMsg').innerText = '错误：x 和 y 数据长度不匹配';
        return;
    }

    sendRequest('bar')
        .then(result => {
            updateBarStats(result);
            if (result.chartImage) {
                showMatplotlibImage(result.chartImage);
                document.getElementById('resultMsg').innerText = `图表生成成功 — x: ${result.x?.slice(0, 3)}... y: ${result.y?.slice(0, 3)}...`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('resultMsg').innerText = '请求失败：' + error.message;
        });
}

// ================================================================
// 直方图
// ================================================================
function sendData_Histogram() {
    const xRaw = document.getElementById('hisXInput').value;
    const yRaw = document.getElementById('hisYInput').value;
    const zRaw = document.getElementById('hisZInput').value;
    const parseData = (s) => s.trim() ? s.split(/[,，\s]+/).map(Number) : [];
    const groups = [parseData(xRaw), parseData(yRaw), parseData(zRaw)].filter(a => a.length > 0);

    if (groups.length === 0) {
        document.getElementById('resultMsg').innerText = '错误：请至少输入一组数据';
        return;
    }

    sendRequest('histogram')
        .then(result => {
            if (result.chartImage) {
                showMatplotlibImage(result.chartImage);
                document.getElementById('resultMsg').innerText = '直方图生成成功';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('resultMsg').innerText = '请求失败：' + error.message;
        });
}

// ================================================================
// 饼图
// ================================================================
function sendData_Pie() {
    const labelsRaw = document.getElementById('pieLabels').value;
    const valuesRaw = document.getElementById('pieValues').value;
    const labels = labelsRaw.trim() ? labelsRaw.split(/[,，\n]+/).map(s => s.trim()).filter(Boolean) : [];
    const values = valuesRaw.trim() ? valuesRaw.split(/[,，\n\s]+/).map(Number).filter(n => !isNaN(n)) : [];

    if (labels.length === 0 || values.length === 0) {
        document.getElementById('resultMsg').innerText = '错误：请输入标签和数值';
        return;
    }
    if (labels.length !== values.length) {
        document.getElementById('resultMsg').innerText = '错误：标签和数值数量不匹配';
        return;
    }

    sendRequest('pie')
        .then(result => {
            if (result.chartImage) {
                showMatplotlibImage(result.chartImage);
                document.getElementById('resultMsg').innerText = '饼图生成成功';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('resultMsg').innerText = '请求失败：' + error.message;
        });
}

// ================================================================
// 箱线图
// ================================================================
function sendData_Boxplot() {
    const g1 = document.getElementById('boxG1').value;
    const g2 = document.getElementById('boxG2').value;
    const g3 = document.getElementById('boxG3').value;
    const parseData = (s) => s.trim() ? s.split(/[,，\s]+/).map(Number) : [];
    const groups = [parseData(g1), parseData(g2), parseData(g3)].filter(a => a.length > 0);

    if (groups.length === 0) {
        document.getElementById('resultMsg').innerText = '错误：请至少输入一组数据';
        return;
    }

    sendRequest('boxplot')
        .then(result => {
            if (result.chartImage) {
                showMatplotlibImage(result.chartImage);
                document.getElementById('resultMsg').innerText = '箱线图生成成功';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('resultMsg').innerText = '请求失败：' + error.message;
        });
}

// ================================================================
// 散点图
// ================================================================
function sendData_Scatter() {
    const xRaw = document.getElementById('scatterXInput').value;
    const yRaw = document.getElementById('scatterYInput').value;
    const xData = xRaw.trim() ? xRaw.split(/[,，\s]+/).map(Number) : [];
    const yData = yRaw.trim() ? yRaw.split(/[,，\s]+/).map(Number) : [];

    if (xData.length === 0 || xData.some(isNaN)) {
        document.getElementById('resultMsg').innerText = '错误：请输入有效的 x 数据';
        return;
    }
    if (yData.length === 0 || yData.some(isNaN)) {
        document.getElementById('resultMsg').innerText = '错误：请输入有效的 y 数据';
        return;
    }
    if (xData.length !== yData.length) {
        document.getElementById('resultMsg').innerText = '错误：x 和 y 数据长度不匹配';
        return;
    }

    sendRequest('scatter')
        .then(result => {
            updateLineStats(result);
            if (result.chartImage) {
                showMatplotlibImage(result.chartImage);
                document.getElementById('resultMsg').innerText = `散点图生成成功 — x: ${result.x?.slice(0, 3)}... y: ${result.y?.slice(0, 3)}...`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('resultMsg').innerText = '请求失败：' + error.message;
        });
}
