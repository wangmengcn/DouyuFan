/**
 * gitf.js
 * @authors Wangmengcn (eclipse_sv@163.com)
 * @date    2016-07-16 09:18:54
 * @version $Id$
 */
 var socket = io.connect('http://localhost:' + 3000);
 var counter = 1;
 var rcounter = 0;
 var rocketrow = 0;
 /*
     此方法是客户端与服务器连接之后，向服务器发送空消息，从而触发服务器向客户端发送消息
 */
 socket.on('connect', function() {
 	    var timer = setInterval(function(){
	    	socket.emit('chat msg','');
	    },1000);
 });
 /*
     此方法主要用以接收服务器的聊天信息
 */
 // socket.on('broad cast', function(msg){
 //     if (counter%10==0){
 //         $('#messages').empty();
 //     }
 //     $('#messages').append('<li class="list-group-item">'+msg+'</li>');
 //     counter+=1;
 //   });
 /*
     此处主要用以接受来自socketio服务器发送的可以抢鱼丸的房间，并通过jQury动态添加相应的元素到页面
 */
 socket.on('rocket cast', function(msg){
     if(msg!=null){
         if(rcounter==0){
             $('#rockets').append("<h2>鱼丸礼物</h2><br>");
         }
         var rowid = "rocketrow" +parseInt(rcounter/3);
         var colid = "room" + rcounter;
         if(rcounter%3==0){
             $('#rockets').append("<div class='row' id="+ rowid +"/>")
         }
         $('#'+rowid).append("<div class='col-sm-6 col-md-4' id="+colid+ "><div class='thumbnail'><img src='"+ msg['img'] +"'"+ "alt='http://eclipsesv.com:4321/tv/"+ msg['roomid'] +"'"+">"+
             "<div class='caption'><h4>"+msg['roomtitle']+"</h4><p><a target='_blank' href='http://eclipsesv.com:4321/tv/"+msg['roomid']+"'>"+msg['anchor']+"@"+msg['tag']+"</a></p></div>"
          + "</div></div>");
         var timer = setTimeout(function(){
             $('#'+colid).remove();
         },30000)
         rcounter+=1;
     }
   });
