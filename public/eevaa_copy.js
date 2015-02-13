var eevaa = (function(){
var version = 1.0,port=9876;

return {
init:function(){$("#pyvideo,#pydta,#pyhertz,#pydta270").on('click',this.showSettings);$("#menu_pyvideo_form,#menu_pydta_form,#menu_pyhertz_form,#menu_pydta270_form").on('submit',this.callPyBlock);$("#up,#down,#channel").on('click',eevaa.callPyRemote);$("#pause").on('click',function(){eevaa.pytvtimer?clearInterval(eevaa.pytvtimer):""});$("#trash").on('click',eevaa.trash)},
notifyMessage:function(message){$("#holder_notifications").html(message).show(100,function(){var me=this;setTimeout(function(){$(me).hide().html("");},5000);})},
getVersion:function(){return version;},
getDeviceInfo:function(){$.getJSON('/devices/devices.json',function(data){var device_list=$("#menu-devices").html();$.each(data,function(k,v){device_list=device_list+'<option value="'+v+'">'+k+'</option>';});$("#menu-devices").html(device_list)})},
showSettings:function(evt){evt.preventDefault();var tid=evt.target.id;$("div[id^=menu_py][id!=menu_"+tid+"]").hide();$("#menu_"+tid).slideToggle();},
callPyBlock:function(evt){evt.preventDefault();var device=$("#menu_devices option:selected").val();
if(device==-1){alert("Please select the target cloud"); return;}
var $this=$(this),tid=$this.attr('id'),urli=tid.split("_")[1],url=(urli=="pydta270a")?"pyvideo":urli,urlmain="http://"+device+":"+port,urlpics=urlmain+"/images/captures/",urlaudio=urlmain+"/Recordings/",urltools="http://"+device+":"+port+"/tools/",urlpath=urltools+url,valid={};
$this.find("input[id^="+tid+"]").each(function(){var k=$(this).attr('id').split("_")[3],v=$.trim($(this).val());valid[k]=v});$this.find("select[id^="+tid+"]").each(function(){var k=$(this).attr('id').split("_")[3],v=$(this).find("option:selected").val();valid[k]=v});
var returnv=false;
$.each(valid,function(k,v){if(v==="" | v ==-1){alert("Please fill all the fields in the settings section");returnv=true;return false;}});
if(returnv){return;}
console.log(urlpath);
//console.log("###################"+$('#testinprogress').html());
$('#testinprogress').show();
console.log("Test in Progress..............");
$.post(urlpath+".py",valid).done(hookPOut).fail(function(er){var m='<div class="alert alert-warning alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><strong>Error:</strong>'+er+'</div>';$("#testoutput").html(m);});
function hookPOut(c){switch(urli){
case "pydta":
case "pyvideo":
case "pydta270":
var ims='<div class="row"><div class="col-md-6 col-sm-6 col-lg-6"><img src="'+urlpics+valid.testname+'1.jpeg" class="img-rounded" alt="Image before" /></div><div class="col-md-6 col-sm-6 col-lg-6"><img src="'+urlpics+valid.testname+'2.jpeg" class="img-rounded" alt="Image after" /></div></div>',
c=c;$('#testinprogress').hide();$("#testoutput").html(c);$("#trash").attr('data-file','').attr('data-file','images/captures/'+valid.testname+'1.jpeg images/captures/'+valid.testname+'2.jpeg');break;
case "pyhertz":
default:
var ams='<div class="row"><div class="col-md-12 col-sm-12 col-lg-12"><audio autoplay="autoplay" controls><source src="'+urlaudio+valid.testname+'.mp3" type="audio/mpeg">Your browser does not support the audio element.</audio></div></div>',
c=ams+c;$("#testoutput").html(c);$("#trash").attr('data-file','').attr('data-file','Recordings/'+valid.testname+'.mp3');
}}},
callPyRemote:function(){var device=$("#menu_devices option:selected").val();if(device==-1){alert("Please select the target cloud");return;};var command=$(this).attr('id'),testname=$.trim($('#channelnumber').val())||0;$.post("http://"+device+":"+port+"/tools/pydtaremote_diag.py",{modulename:"testCode",channelnumber:command,testname:testname})},
trash:function(){var fwcards=$(this).attr('data-file').split(" ");var device=$("#menu_devices option:selected").val();if(device==-1){alert("Please select the target cloud");return;};for(var i=0;i<fwcards.length;++i){$.post("http://"+device+":"+port+"/delete",{file:fwcards[i]});}},
registerDevice:function(){var devicename=$("#txt_devicename").val();
if(devicename===""){ivaa.notifyMessage('<p class="fail">Device name is required!</p>');}else{$.ajax({url:'/register',type:'POST',contentType:'application/json',data:JSON.stringify({devicename:devicename}),success:function(data){ivaa.notifyMessage(data);}});}
return false;
}
};

})();


$(document).ready(function(){
window['eevaa'] = eevaa;
eevaa.init();
})
