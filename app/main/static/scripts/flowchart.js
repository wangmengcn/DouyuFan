var flowdom = document.getElementById("flowmonitor");
var flowchart = echarts.init(flowdom);
var app = {};
var flowdata;
var initdata;
flowoption = null;
var base = new Date();

var oneDay = 24 * 3600 * 1000;
var date = [];
var data = [];


function addData(shift) {
    var now = new Date();
    now = [now.getMonth()+1,now.getDate(),now.getHours(), now.getMinutes()].join('-');
    $.get( "http://123.206.211.77:8000", function( data ) {
        flowdata = data;
    });
    flowdata =parseInt(flowdata)
    date.push(now);
    data.push(flowdata);
    if (shift) {
        date.shift();
        data.shift();
    }
}
//从历史数据获取🚀数量
function initChart(){
    $.get("http://123.206.211.77:7000",function(transdata){
        initdata =transdata;
        initdata = JSON.parse(initdata);
        array =[]
        for(a in initdata){
         array.push([a,initdata[a]])
        }
        array.sort(function(a,b){return a[1] - b[1]});
        convert = array;
        for (var i = 0; i < array.length; i++) {
            array[i]
            date.push(array[i][0]);
            data.push(array[i][1]);
        }
        flowchart.hideLoading();
        flowchart.setOption({
            xAxis: {
                data: date
            },
            series: [{
                name:'弹幕量',
                data: data
            }]
        });
        app.timeTicket = setInterval(function () {
            addData(false);
            flowchart.setOption({
                xAxis: {
                    data: date
                },
                series: [{
                    name:'弹幕量',
                    data: data
                    }]
                });
            }, 6000);
    });            
    
}

flowoption = {
    title: {
        text: '🚀实时数量',
        subtext: '🚀',
        left: 'center'
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: date
    },
    yAxis: {
        name: "数量(个)",
        boundaryGap: [0, '50%'],
        type: 'value'
    },
    series: [
        {
            name:'弹幕量',
            type:'line',
            smooth:true,
            symbol: 'none',
            stack: 'a',
            areaStyle: {
                normal: {}
            },
            data: data
        }
    ],
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            animation: false
        },
        formatter: function (params) {
            return params[0].name + '<br />' + params[0].value;
        }
    },
    dataZoom:   
        [
            {
                type: 'slider', 
                start: 99,      
                end: 100  
            }    
        ,
        
            {
                type: 'slider',
                yAxisIndex: 0,
                start: 99,
                end: 100
            }
        ]    
    
    
};
flowchart.showLoading();
initChart()
if (flowoption && typeof flowoption === "object") {
    var startTime = +new Date();
    flowchart.setOption(flowoption, true);
    var endTime = +new Date();
    var updateTime = endTime - startTime;
    console.log("Time used:", updateTime);
} 