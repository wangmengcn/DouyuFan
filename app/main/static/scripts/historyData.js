/**
 * historyData.js
 * @authors Wangmengcn (eclipse_sv@163.com)
 * @date    2016-07-23 09:36:03
 * @version $Id$
 */

 // 连接socket.io服务器
 var socket = io.connect('http://localhost:' + 3000);
 // 设置echarts
 var rocketbyHour = document.getElementById('historyRockets');
 var myChart = echarts.init(rocketbyHour);
 var cuurentdate;
 $(document).ready(function () {
     $("#calendar").zabuto_calendar({language: "en",
     								cell_border :true,
     								today : true,
     								show_days : false,
     								weekstartson : 0,
     								action: function () {
             							return myDateFunction(this.id, false);
         							}			
 	});
 	myChart.showLoading({text:'点击日历获取数据'});
 });
 function myDateFunction(id, fromModal) {
     var date = $("#" + id).data("date");
     cuurentdate = date
     socket.emit('historyDate',date);
 	myChart.showLoading({text:'数据加载中！'});
     return true;
 }
 socket.on('historyRockets', function(msg){
 	value = msg;
 	if(value!=null){
 		var hours = [];
 		for(var i=0;i<24;i++){
 			hours.push(i);
 		}
 		option = {
 			title: {
 				show: true,
 				text: cuurentdate+'🚀逐时发送量',
 				textAlign: 'middle',
 				x : 'center'
 			},
 			tooltip: {
 			    trigger: 'axis',
 			    axisPointer: {
 			        animation: false
 			    },
 			    formatter: function (params) {
 			        return params[0].name+ "点" + params[0].value + "个🚀";
 			    }
 			},
 		    xAxis: {
 		        type: 'category',
 		        boundaryGap: false,
 		        data: hours
 		    },
 		    yAxis: {
 		        type: 'value'
 		    },
 		    series: [
 		        {
 		            name:'🚀',
 		            type:'line',
 		            smooth:true,
 		            symbol: 'none',
 		            stack: 'a',
 		            areaStyle: {
 		                normal: {}
 		            },
 		            data: value
 		        }
 		    ]
 		};
 		myChart.hideLoading();
 		myChart.setOption(option,true);
 	}
 	else{
 		myChart.showLoading({text:'缺少本日数据！'});
 	}
 });