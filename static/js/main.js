let chart = null;  // 保存图表对象，防止重复叠加

function toggleOption() {
        const chartType = document.querySelector('input[name="chartType"]:checked').value;
        const LineOption = document.getElementById('LineOption');
        const barOption = document.getElementById('Bar');
        const pieOption = document.getElementById('Pie');
        const scatterOption = document.getElementById('Scatter');
        const hisOption = document.getElementById('Histogram');
        const boxOption = document.getElementById('Boxplot');
        const LanguageOption = document.getElementById('ProcessLanguage');
        const Warning = document.getElementById('Warning');
        LanguageChange(chartType,LanguageOption,Warning);
        LineOptionChange(chartType,LineOption);
        barOptionChange(chartType,barOption);
        pieOptionChange(chartType,pieOption);
        scatterOptionChange(chartType,scatterOption);
        hisOptionChange(chartType,hisOption);
        boxOptionChange(chartType,boxOption);
}
    // 页面加载时初始化累加线选项的显示状态
    window.onload = function() {
        toggleOption();
    };

function sendData_Line() {
    let xvalue = document.getElementById("xInput").value;
    let xdataArray;
    if (xvalue.trim() === '') {xdataArray = [];}
    else{xdataArray = xvalue.split(/[,，\s]+/).map(Number);}
    const chartTypeElements = document.getElementsByName('chartType');
   
    let selectedChartType = "line"; // 默认图表类型
    selectedChartType = document.querySelector('input[name="chartType"]:checked').value;
    console.log('选择的图表类型:', selectedChartType);

    let yvalue = document.getElementById("yInput").value;
    let ydataArray = yvalue.trim() === '' ? [] : yvalue.split(/[,，\s]+/).map(Number);
    if (xdataArray.some(isNaN) || xdataArray.length == 0) {
        document.getElementById("result").innerText = "错误：请输入有效的x数据格式";
        return;
    }
    if (ydataArray.length > 0 && ydataArray.some(isNaN)) {
        document.getElementById("result").innerText = "错误：请输入有效的y数据格式";
        return;
    }
    if (ydataArray.length > 0 && xdataArray.length != ydataArray.length) {
        document.getElementById("result").innerText = "错误：x和y数据长度不匹配";
        return;
    }
    let x_only = ydataArray.length === 0;
    let gridon = document.getElementById("grid").checked;
    let processlanguage = document.querySelector('input[name="ProcessLanguage"]:checked').value;
    
    let cumulative=false;letlogoption=false;
    if (selectedChartType === "line") {
        cumulative = document.getElementById("showCumulative").checked;
        logoption = document.getElementById("logScaleX").checked;
    }

    let label = document.getElementById("labelInput").value;
    let xlabel = document.getElementById("xlabelInput").value;
    let ylabel = document.getElementById("ylabelInput").value;
    let title = document.getElementById("titleInput").value;

    fetch("/process", 
    {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            x: xdataArray,
            y: ydataArray,
            chartType: selectedChartType,
            label: label,
            xlabel: xlabel,
            ylabel: ylabel,
            gridon: gridon,
            title: title,
            cumulative: cumulative,
            logoption: logoption,
            Language: processlanguage,
        })
    })
    
    .then(response => response.json())
    .then(result => {
        let x = result.x;
        let y = result.y;
        let x_data = result.x_data;
        let y_data = result.y_data;
        updateData(result,x,y,x_only);
        if (result.chartImage) {updateChartImage(result.chartImage);} 
        else if (selectedChartType === "line") {
        let cumsumData = result.cumsum;
        drawChart(x_data, y_data, cumsumData, cumulative);}
    })
    .catch(error => {
    console.error('Error:', error);
    document.getElementById("result").innerText = 
        "请求失败：" + error.message;
    });
}

function sendData_Bar() {
    let xvalue = document.getElementById("xInputBar").value;
    let xdataArray;
    if (xvalue.trim() === '') {xdataArray = [];}
    else{xdataArray = xvalue.split(/[,，\s]+/);}

   
    let selectedChartType = "bar"; // 默认图表类型
    selectedChartType = document.querySelector('input[name="chartType"]:checked').value;
    console.log('选择的图表类型:', selectedChartType);

    let yvalue = document.getElementById("yInputBar").value;
    let ydataArray = yvalue.trim() === '' ? [] : yvalue.split(/[,，\s]+/).map(Number);
    if (xdataArray.length == 0) {
        document.getElementById("result").innerText = "错误：请输入有效的x数据格式";
        return;
    }
    if (ydataArray.length > 0 && ydataArray.some(isNaN)) {
        document.getElementById("result").innerText = "错误：请输入有效的y数据格式";
        return;
    }
    if (ydataArray.length > 0 && xdataArray.length != ydataArray.length) {
        document.getElementById("result").innerText = "错误：x和y数据长度不匹配";
        return;
    }

    let processlanguage = document.querySelector('input[name="ProcessLanguageWarning"]:checked').value;
    let gridon = document.getElementById("grid").checked;
    let width = 0.5; let alpha = 0.8;
    if (selectedChartType === "bar") {
        width = parseFloat(document.getElementById("widthInputBar").value) || 0.5;
        alpha = parseFloat(document.getElementById("alphaInputBar").value) || 0.8;
    }
    let label = document.getElementById("labelInputBar").value;
    let xlabel = document.getElementById("xlabelInputBar").value;
    let ylabel = document.getElementById("ylabelInputBar").value;
    let title = document.getElementById("titleInputBar").value;

    fetch("/process", 
    {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            x: xdataArray,
            y: ydataArray,
            chartType: selectedChartType,
            label: label,
            xlabel: xlabel,
            ylabel: ylabel,
            gridon: gridon,
            title: title,
            Language: processlanguage,
            width:width,
            alpha:alpha
        })
    })
    
    .then(response => response.json())
    .then(result => {
        let x = result.x;
        let y = result.y;
        let x_data = result.x_data;
        let y_data = result.y_data;
        updateData_bar(result,x,y);
        updateChartImage(result.chartImage);
    })
    .catch(error => {
    console.error('Error:', error);
    document.getElementById("result").innerText = 
        "请求失败：" + error.message;
    });
}


function sendData_Histogram(){
    // 1. 获取数据输入
    const xvalue = document.getElementById("xInputHis").value;
    const yvalue = document.getElementById("yInputHis").value;
    const zvalue = document.getElementById("zInputHis").value;
    const parseData = (str) => str ? str.split(/[,，\s]+/).map(Number) : [];
    const xdataArray = parseData(xvalue);
    const ydataArray = parseData(yvalue);
    const zdataArray = parseData(zvalue);
    const dataGroups = [xdataArray, ydataArray, zdataArray].filter(dataArray => dataArray.length > 0); // 过滤掉空数组
    // 2. 获取分箱模式
    const binsMode = document.querySelector('input[name="binsMode"]:checked').value;
    let bins = null;
    // 3. 根据模式获取分箱参数
    if (binsMode === 'edges') {
        const binsEdgesStr = document.getElementById("binsEdgesInputHis").value;
        if (binsEdgesStr) {
            try {
                // 简单的字符串解析，实际应用中应更严格
                bins = JSON.parse(binsEdgesStr.replace(/'/g, '[]'));
            } catch (e) {
                console.error("分箱边界格式错误", e);
                document.getElementById("result").innerText = "错误：分箱边界格式不正确，应为 [0,5,10] 格式";
                return;
            }
        }
    } else {
        const binsCountStr = document.getElementById("binsCountInputHis").value;
        bins = binsCountStr ? parseInt(binsCountStr) : 10; // 默认10
    }
     // 4. 获取其他参数
    const gridon = document.getElementById("grid").checked;
    const histtype = document.getElementById("histtypeSelectHis").value;
    const color = document.getElementById("colorInputHis").value ;
    const alpha = parseFloat(document.getElementById("alphaInputHis").value)||0.8
    const density = document.getElementById("densityCheckHis").checked;
    const orientation = document.getElementById("orientationSelectHis").value;
    const cumulative = document.getElementById("CumulativeHis").checked;
    const logScale = document.getElementById("logScaleHis").checked;
    // 5. 发送请求
    fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            chartType: "histogram",
            y: dataGroups, // 将多组数据放在 y 字段中
            bins: bins,
            histtype: histtype,
            color: color,
            alpha: alpha,
            density: density,
            orientation: orientation,
            cumulative: cumulative,
            logScale: logScale,
            gridon: gridon,
            Language: "python" // 直方图目前仅支持 Python
        })
    })
    .then(response => response.json())
    .then(result => {
        // 处理响应，例如显示图像
        if (result.chartImage) {
            updateChartImage(result.chartImage);
            document.getElementById("result").innerText = "请求成功";
        } 
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("result").innerText = "请求失败：" + error.message;
    });
}



function updateData(result,x,y,x_only){
// 4️⃣ 显示 Python 返回的结果
        document.getElementById("result").innerText =
            "确认Python 返回的数据：" + x + " 和 " + y;
        document.getElementById("xmean").innerText = result.xmean;
        document.getElementById("xstd").innerText = result.xstd;
        document.getElementById("xmax").innerText = result.xmax;
        document.getElementById("xmin").innerText = result.xmin; 
        if (x_only){document.getElementById("ymean").innerText = "无y数据";
        document.getElementById("ystd").innerText = "无y数据";
        document.getElementById("ymax").innerText = "无y数据";
        document.getElementById("ymin").innerText = "无y数据";}
         else {
        document.getElementById("ymean").innerText = result.ymean;
        document.getElementById("ystd").innerText = result.ystd;
        document.getElementById("ymax").innerText = result.ymax;
        document.getElementById("ymin").innerText = result.ymin;}
}
function updateData_bar(result,x,y){
// 4️⃣ 显示 Python 返回的结果
        document.getElementById("result").innerText =
            "确认Python 返回的数据：" + x + " 和 " + y;
        document.getElementById("xcategories").innerText = result.xlength;
        document.getElementById("ymeanbar").innerText = result.ymean;
        document.getElementById("ystdbar").innerText = result.ystd;
        document.getElementById("ymaxbar").innerText = result.ymax;
        document.getElementById("yminbar").innerText = result.ymin;
}

function drawChart(x,y,cumsumData,cumulative) {
   const ctx = document.getElementById("myChart");    // 如果已经有图，先销毁（非常关键）
   const matplotlibChart = document.getElementById('matplotlibChart');
   const matplotlibImage = document.getElementById('matplotlibImage');
   matplotlibChart.style.display = 'none';
   matplotlibImage.style.display = 'none';
   const myChartCanvas = document.getElementById('myChart');
   myChartCanvas.style.display = 'block';
    if (chart) {
        chart.destroy();
    }

    let datasets = [
        {
            label: "原始数据",
            data: y,
            borderColor: "rgba(54, 162, 235, 1)",
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderWidth: 2
        }
    ];
    // 只有当cumulative为true时，才添加累加线数据集
    if (cumulative) {
        datasets.push({
            label: "累积和",
            data: cumsumData,
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 2
        });
    }
    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: x,
            datasets: datasets
        },
        options: {
            responsive: true
        }
    });
}
function updateChartImage(chartImage) {
    const matplotlibChart = document.getElementById('matplotlibChart');
    const matplotlibImage = document.getElementById('matplotlibImage');
    const myChartCanvas = document.getElementById('myChart');
    matplotlibChart.style.display = 'block';
    myChartCanvas.style.display = 'none';
    if (chartImage) {
        // 显示matplotlib图表
        matplotlibImage.src = 'data:image/png;base64,' + chartImage;
        matplotlibChart.style.display = 'block';
        myChartCanvas.style.display = 'none';
        
        // 销毁现有的Chart.js图表实例
        if (chart) {
            chart.destroy();
            chart = null;
        }
    } else {
        // 显示Chart.js图表
        matplotlibChart.style.display = 'none';
        myChartCanvas.style.display = 'block';
    }
}

function LanguageChange(chartType,LanguageOption,Waring) {
    if(chartType === 'line'){LanguageOption.style.display = 'block';Waring.style.display = 'none';}
    else{LanguageOption.style.display = 'none';Waring.style.display = 'block';}}
function LineOptionChange(chartType,LineOption) {
    if(chartType === 'line'){LineOption.style.display = 'block';}
    else{LineOption.style.display = 'none';}}
function barOptionChange(chartType,barOption) {
    if(chartType === 'bar'){barOption.style.display = 'block';}
    else{barOption.style.display = 'none';}}
function pieOptionChange(chartType,pieOption) {
    if(chartType === 'pie'){pieOption.style.display = 'block';}
    else{pieOption.style.display = 'none';}
}
function scatterOptionChange(chartType,scatterOption) {
    if(chartType === 'scatter'){scatterOption.style.display = 'block';}
    else{scatterOption.style.display = 'none';}
}
function hisOptionChange(chartType,hisOption) {
    if(chartType === 'histogram'){hisOption.style.display = 'block';}
    else{hisOption.style.display = 'none';}}
function boxOptionChange(chartType,boxOption) {
    if(chartType === 'boxplot'){boxOption.style.display = 'block';}
    else{boxOption.style.display = 'none';}}