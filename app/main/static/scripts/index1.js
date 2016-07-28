/**
* index.js
* @authors Wangmengcn (eclipse_sv@163.com)
* @date    2016-07-15 18:05:51
* @version $Id$
*/

// 连接socket.io服务器
var socket = io.connect('http://localhost:' + 3000);
// 绘制逐时🚀数据
var dom = document.getElementById("piemonitor");
var senderdom = document.getElementById("senderPie");
var recverdom = document.getElementById("recverPie");
var myChart = echarts.init(dom);
var senderChart = echarts.init(senderdom);
var recverChart = echarts.init(recverdom);
var option = null;
var hours = [];
var value = [];
var senders ;
var recvers ;

 /*
     此方法是客户端与服务器连接之后，向服务器发送空消息，从而触发服务器向客户端发送消息
 */
 socket.on('connect', function() {
 	socket.emit('index','');
 });
 /*
     此方法主要用以接收服务器的聊天信息
 */
 socket.on('rocket by day', function(msg){
     value = msg;
     for(var i=0;i<24;i++){
          hours.push(i);
     }
     option = {
          title: {
               show: true,
               text: '🚀逐时发送量',
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
     myChart.setOption(option);
   });

 socket.on('sender rank',function(msg){
     senders = msg;
     if(senders.length!=null){
          $('#senderRank').append("<ul class='list-group' id='senders'></ul>");
          piedata = new Array();
          for(item in senders){
               // $('#senders').append("<li class='list-group-item'><span class='badge'>"+senders[item][1]+"</span>"+senders[item][0]+"</li>")
               singledata = {'value':senders[item][1],'name':senders[item][0]};
               piedata.push(singledata);
               if(item==9){
                    break;
               }
          }
          pieoption = {
               title: {
                    show: true,
                    text: '土豪排行',
                    textAlign: 'middle',
                    x : 'center'
               },
               tooltip: {
               },
               series: [{
                       name: 'pie',
                       type: 'pie',
                       selectedMode: 'single',
                       selectedOffset: 30,
                       clockwise: true,
                       label: {
                           normal: {
                               textStyle: {
                                   fontSize: 18,
                                   color: '#235894'
                               }
                           }
                       },
                       labelLine: {
                           normal: {
                               lineStyle: {
                                   color: '#235894'
                               }
                           }
                       },
                       data:piedata
                   }]
          };
          senderChart.setOption(pieoption);
     }
 });
 socket.on('recver rank',function(msg){
     recvers = msg;
     if(recvers.length!=null){
          // $('#recverRank').append("<ul class='list-group' id='recvers'></ul>");
          piedata = new Array();
          for(item in recvers){
               $('#recvers').append("<li class='list-group-item'><span class='badge'>"+recvers[item][1]+"</span>"+recvers[item][0]+"</li>");
               singledata = {'value':recvers[item][1],'name':recvers[item][0]};
               piedata.push(singledata);
               if(item==9){
                    break;
               }
          }
          pieoption = {
               title: {
                    show: true,
                    text: '主播排行',
                    textAlign: 'middle',
                    x : 'center'
               },
               tooltip: {
               },
               series: [{
                       name: 'pie',
                       type: 'pie',
                       selectedMode: 'single',
                       selectedOffset: 30,
                       clockwise: true,
                       label: {
                           normal: {
                               textStyle: {
                                   fontSize: 18,
                                   color: '#235894'
                               }
                           }
                       },
                       labelLine: {
                           normal: {
                               lineStyle: {
                                   color: '#235894'
                               }
                           }
                       },
                       data:piedata
                   }]
          };
          recverChart.setOption(pieoption);
     }
});