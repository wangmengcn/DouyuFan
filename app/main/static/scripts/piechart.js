var dom = document.getElementById("piemonitor");
var myChart = echarts.init(dom);
var jsondata;
option = null;
var key = [];
var value = [];


function addData() {
    $.get( "http://123.206.211.77:8888", function( data ) {
        jsondata = JSON.parse(data)
        for (k in jsondata){
            key.push(k);
            value.push(jsondata[k]);
            option = {
                title : {
                    text: '斗鱼土豪榜',
                    subtext: '🚀排名',
                    x:'center'
                },
                roseType: 'angle',
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                series : [
                    {
                        name: '🚀发射者',
                        type: 'pie',
                        radius : '55%',
                        center: ['50%', '60%'],
                        data:[
                            {value:value[0],name:key[0]},
                            {value:value[1],name:key[1]},
                            {value:value[2],name:key[2]},
                            {value:value[3],name:key[3]},
                            {value:value[4],name:key[4]},
                            {value:value[5],name:key[5]},
                            {value:value[6],name:key[6]},
                            {value:value[7],name:key[7]},
                            {value:value[8],name:key[8]},
                            {value:value[9],name:key[9]}
                        ],
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            };
            myChart.setOption(option, true);
        }
    });
}

        addData();