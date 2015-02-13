var exec = require('child_process').exec,path = require('path'),spawn = require('child_process').spawn,python;

function pyshell(pythonPath,filePath,httpRes,mimeType){
	var output = "";
	//console.log(process.env)
	//python = exec(filePath,{cwd:pythonPath,env:process.env});

    var err = "";
    console.log('running..');
	python = exec('/home/team_auto/XidToolChains/XiD_BCM_URSR/toolchains/stbgcc-4.5.4-2.7/bin/arm-linux-gdb core',function(error,stdout,stderr){
	//python = exec('ls /home/team_auto',function(error,stdout,stderr){
          				console.log('stdout:'+stdout);
					output = stdout.substring(stdout.indexOf("Comments:"),stdout.indexOf("Comments:")+101);
					console.log("output >>>>>>>>>>>>>>"+output);
					console.log("#######################################");
					/*if(stderr.length > 0){
					   err = stderr;
					   console.log('stderr:'+stderr);
			                   var errorMessage = '<div class="alert alert-danger alert-dismissable">'+err+'</div>';
                                           console.log('error>>'+err);
                        		   httpRes.writeHead(200,{'Content-Type':mimeType,'Content-Length':err.length});
                                           httpRes.end(err);
                                           return;	
					}*/
                                      /*  if (error!==null){
					   console.log('exec error:'+error);
 					}*/
		     
					var successMessage = '<div class="alert alert-success">'+output+'</div>';
                                        console.log(successMessage);
                                        httpRes.writeHead(200,{'Content-Type':mimeType,'Content-Length':successMessage.length});
                                        httpRes.end(successMessage);
					return;
			//		console.log('stderr:'+stderr.length);

			});
        
 
	console.log('in pyshell'+output);
	//python.stdout.on('data',function(d){output += d});
/*	python.on('exit',function(code){
	        console.log('output >>'+output);
		if(code!==0){
			var errorMessage = '<div class="alert alert-danger alert-dismissable">'+code+'</div>';
			console.log('error>>'+err);
			httpRes.writeHead(200,{'Content-Type':mimeType,'Content-Length':err.length});
			httpRes.end(err);
			return;
		}
		//var tmo=output.match(/\[Output:(.*)\]/g);
		var tmo=output;
		console.log('tmo:'+tmo);
		var successMessage = '<div class="alert alert-success">'+tmo+'</div>';
		console.log(successMessage);
		httpRes.writeHead(200,{'Content-Type':mimeType,'Content-Length':successMessage.length});
		httpRes.end(successMessage);
	});*/
}
exports.pyshell = pyshell;
