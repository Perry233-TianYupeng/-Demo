/**
 * api.js — API 通信层
 *
 * 封装所有与后端 /process 接口的通信逻辑。
 * 提供统一的 sendRequest() 函数，收集表单数据、发送 POST 请求、
 * 处理响应和错误。
 */

/**
 * 统一的数据发送函数。
 * 从当前活动面板收集所有表单数据，组装为 JSON 发送到 /process。
 *
 * @param {string} chartType - 图表类型: line | bar | histogram | pie | boxplot | scatter
 * @returns {Promise<object>} 后端返回的 JSON 结果
 */
function sendRequest(chartType) {
    // 收集通用参数
    const commonData = {
        chartType: chartType,
        title:      document.getElementById('commonTitle').value || '',
        title_size: parseInt(document.getElementById('commonTitleSize').value) || 16,
        xlabel:     document.getElementById('commonXlabel').value || '',
        ylabel:     document.getElementById('commonYlabel').value || '',
        label_size: parseInt(document.getElementById('commonLabelSize').value) || 12,
        legend_pos: document.getElementById('commonLegendPos').value || 'best',
        legend_size:parseInt(document.getElementById('commonLegendSize').value) || 10,
        fig_width:  parseFloat(document.getElementById('commonFigWidth').value) || 10,
        fig_height: parseFloat(document.getElementById('commonFigHeight').value) || 6,
        dpi:        parseInt(document.getElementById('commonDpi').value) || 100,
        grid:       document.getElementById('commonGrid').checked,
        grid_style: document.getElementById('commonGridStyle').value || '--',
        grid_alpha: parseFloat(document.getElementById('commonGridAlpha').value) || 0.5,
        bg_color:   document.getElementById('commonBgColor').value || '#FFFFFF',
        x_log:      document.getElementById('commonXLog').checked,
        y_log:      document.getElementById('commonYLog').checked,
        Language:   'python',  // 默认 Python 处理
    };

    // 收集图表专属参数
    let chartData = {};
    switch (chartType) {
        case 'line':
            chartData = _collectLineData();
            break;
        case 'bar':
            chartData = _collectBarData();
            break;
        case 'histogram':
            chartData = _collectHistogramData();
            break;
        case 'pie':
            chartData = _collectPieData();
            break;
        case 'boxplot':
            chartData = _collectBoxplotData();
            break;
        case 'scatter':
            chartData = _collectScatterData();
            break;
    }

    const payload = { ...commonData, ...chartData };

    return fetch('/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`服务器返回错误: ${response.status}`);
        }
        return response.json();
    });
}

// ================================================================
// 各图表类型的参数收集函数
// ================================================================

function _collectLineData() {
    const xRaw = document.getElementById('lineXInput').value;
    const yRaw = document.getElementById('lineYInput').value;
    const xData = xRaw.trim() ? xRaw.split(/[,，\s]+/).map(Number) : [];
    const yData = yRaw.trim() ? yRaw.split(/[,，\s]+/).map(Number) : [];

    return {
        x: xData,
        y: yData,
        color:        document.getElementById('lineColor').value || '#3366CC',
        linewidth:    parseFloat(document.getElementById('lineWidth').value) || 2.0,
        linestyle:    document.getElementById('lineStyle').value || 'solid',
        marker:       document.getElementById('lineMarker').value || 'none',
        markersize:   parseFloat(document.getElementById('lineMarkerSize').value) || 6,
        marker_color: document.getElementById('lineMarkerColor').value || document.getElementById('lineColor').value,
        alpha:        parseFloat(document.getElementById('lineAlpha').value) || 1.0,
        cumulative:   document.getElementById('lineCumulative').checked,
        label:        document.getElementById('lineLabel').value || '数据',
        Language:     document.querySelector('input[name="lineLanguage"]:checked')?.value || 'python',
    };
}

function _collectBarData() {
    const xRaw = document.getElementById('barXInput').value;
    const yRaw = document.getElementById('barYInput').value;
    const xData = xRaw.trim() ? xRaw.split(/[,，\s]+/) : [];
    const yData = yRaw.trim() ? yRaw.split(/[,，\s]+/).map(Number) : [];

    return {
        x: xData,
        y: yData,
        color:       document.getElementById('barColor').value || '#3366CC',
        width:       parseFloat(document.getElementById('barWidth').value) || 0.8,
        alpha:       parseFloat(document.getElementById('barAlpha').value) || 0.8,
        edge_color:  document.getElementById('barEdgeColor').value || '#333333',
        edge_width:  parseFloat(document.getElementById('barEdgeWidth').value) || 0.5,
        orientation: document.getElementById('barOrientation').value || 'vertical',
        label:       document.getElementById('barLabel').value || '数据',
        Language:    'python',
    };
}

function _collectHistogramData() {
    const xRaw = document.getElementById('hisXInput').value;
    const yRaw = document.getElementById('hisYInput').value;
    const zRaw = document.getElementById('hisZInput').value;
    const parseData = (s) => s.trim() ? s.split(/[,，\s]+/).map(Number) : [];
    const groups = [parseData(xRaw), parseData(yRaw), parseData(zRaw)].filter(a => a.length > 0);

    const binsMode = document.querySelector('input[name="binsMode"]:checked')?.value || 'count';
    let bins = 10;
    if (binsMode === 'edges') {
        const edgesStr = document.getElementById('hisBinsEdges').value;
        if (edgesStr) {
            try { bins = JSON.parse(edgesStr.replace(/'/g, '"')); }
            catch (e) { bins = 10; }
        }
    } else {
        bins = parseInt(document.getElementById('hisBinsCount').value) || 10;
    }

    return {
        y: groups,
        bins:         bins,
        histtype:     document.getElementById('hisHisttype').value || 'bar',
        color:        document.getElementById('hisColor').value || '',
        alpha:        parseFloat(document.getElementById('hisAlpha').value) || 0.8,
        density:      document.getElementById('hisDensity').checked,
        orientation:  document.getElementById('hisOrientation').value || 'vertical',
        cumulative:   document.getElementById('hisCumulative').checked,
        logScale:     document.getElementById('hisLogScale').checked,
        edge_color:   document.getElementById('hisEdgeColor').value || '#333333',
        linewidth:    parseFloat(document.getElementById('hisLinewidth').value) || 1.0,
        Language:     'python',
    };
}

function _collectPieData() {
    const labelsRaw = document.getElementById('pieLabels').value;
    const valuesRaw = document.getElementById('pieValues').value;
    const labels = labelsRaw.trim() ? labelsRaw.split(/[,，\n]+/).map(s => s.trim()).filter(Boolean) : [];
    const values = valuesRaw.trim() ? valuesRaw.split(/[,，\n\s]+/).map(Number).filter(n => !isNaN(n)) : [];

    return {
        labels: labels,
        values: values,
        color:            document.getElementById('pieColors').value || '',
        explode:          document.getElementById('pieExplode').value || '',
        shadow:           document.getElementById('pieShadow').checked,
        start_angle:      parseFloat(document.getElementById('pieStartAngle').value) || 0,
        autopct:          document.getElementById('pieAutopct').value || '%1.1f%%',
        label_distance:   parseFloat(document.getElementById('pieLabelDist').value) || 1.1,
        donut:            parseFloat(document.getElementById('pieDonut').value) || 0,
        text_size:        parseInt(document.getElementById('pieTextSize').value) || 12,
        wedge_edge_color: document.getElementById('pieEdgeColor').value || 'white',
        wedge_edge_width: parseFloat(document.getElementById('pieEdgeWidth').value) || 1,
        Language:         'python',
    };
}

function _collectBoxplotData() {
    const g1 = document.getElementById('boxG1').value;
    const g2 = document.getElementById('boxG2').value;
    const g3 = document.getElementById('boxG3').value;
    const parseData = (s) => s.trim() ? s.split(/[,，\s]+/).map(Number) : [];
    const groups = [parseData(g1), parseData(g2), parseData(g3)].filter(a => a.length > 0);

    const labelsRaw = document.getElementById('boxLabels').value;
    const labels = labelsRaw.trim() ? labelsRaw.split(/[,，]+/).map(s => s.trim()) : null;

    return {
        data_groups: groups,
        labels:       labels,
        notch:        document.getElementById('boxNotch').checked,
        show_means:   document.getElementById('boxShowMeans').checked,
        show_outliers:document.getElementById('boxShowOutliers').checked,
        orientation:  document.getElementById('boxOrientation').value || 'vertical',
        color:        document.getElementById('boxColor').value || '#3366CC',
        widths:       parseFloat(document.getElementById('boxWidths').value) || 0.5,
        patch_artist: document.getElementById('boxPatchArtist').checked,
        alpha:        parseFloat(document.getElementById('boxAlpha').value) || 0.6,
        edge_color:   document.getElementById('boxEdgeColor').value || '#333333',
        Language:     'python',
    };
}

function _collectScatterData() {
    const xRaw = document.getElementById('scatterXInput').value;
    const yRaw = document.getElementById('scatterYInput').value;
    const xData = xRaw.trim() ? xRaw.split(/[,，\s]+/).map(Number) : [];
    const yData = yRaw.trim() ? yRaw.split(/[,，\s]+/).map(Number) : [];

    const cRaw = document.getElementById('scatterC').value;
    let cValue = cRaw || '#3366CC';
    // 尝试解析为数值数组
    if (cRaw && cRaw.includes(',')) {
        cValue = cRaw.split(/[,，\s]+/).map(Number).filter(n => !isNaN(n));
        if (cValue.length === 0) cValue = '#3366CC';
    }

    return {
        x: xData,
        y: yData,
        s:        parseInt(document.getElementById('scatterS').value) || 20,
        c:        cValue,
        marker:   document.getElementById('scatterMarker').value || 'o',
        alpha:    parseFloat(document.getElementById('scatterAlpha').value) || 0.8,
        edge_color: document.getElementById('scatterEdgeColor').value || null,
        linewidth: parseFloat(document.getElementById('scatterLinewidth').value) || 0,
        cmap:     document.getElementById('scatterCmap').value || null,
        colorbar: document.getElementById('scatterColorbar').checked,
        Language: 'python',
    };
}
