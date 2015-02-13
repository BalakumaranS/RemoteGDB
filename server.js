var express=require('express'), fs=require('fs'),path=require('path'),pyshell=require('./exports/pyshell.js');

//App variables
var app=express(),port=9876,localPath=__dirname,viewPath=path.join(localPath,'public'),pythonPath=path.join(localPath,'python'),devicePath=path.join(localPath,'devices'),indexPath=path.join(viewPath,'index.html'),
mimeType={".html":"text/html",".js":"application/javascript",".css":"text/css",".txt":"text/plain",".jpg":"image/jpeg",".gif":"image/gif",".png":"image/png",".py":"text/html",".json":"application/json"};

//Functions for app
function isValidFile(filePath,fileArgs,res,mimeType){
path.exists(path.join(pythonPath),function(exists){
if(exists){pyshell.pyshell(pythonPath,filePath+fileArgs,res,mimeType);}else{errMessage='<p class="fail">File not found</p>';res.writeHead(404,{'Content-Type':'text/html','Content-Length':errMessage.length});res.end(errMessage);}
});
}


function getFile(path,res,mimeType){
fs.readFile(path,function(err,contents){
if(!err){res.writeHead(200,{'Content-Type':mimeType,'Content-Length':contents.length});res.end(contents);}else{errMessage='<p class="fail">Internal Server Error</p><p>Contact the <i>Webmaster</i></p>';res.writeHead(500,{'Content-Type':'text/html','Content-Length':errMessage.length});res.end(errMessage);}
});
}

//Configuring app server
app.use(express.static(viewPath));app.use(express.bodyParser());app.use(express.json());app.use(express.logger('dev'));
app.all('*', function(req, res, next){
  if (!req.get('Origin')) return next();
  // use "*" here to accept any origin
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, POST');
  res.set('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type');
  // res.set('Access-Control-Allow-Max-Age', 3600);
  if ('OPTIONS' == req.method) return res.send(200);
  next();
});

//Defining routes for app
app.get('/',function(req,res){getFile(indexPath,res,mimeType[".html"])});

app.get('/automate',function(req,res){getFile(path.join(viewPath,'automate.html'),res,mimeType[".html"])});

app.get('/devices/:filename',function(req,res){getFile(path.join(devicePath,req.params.filename),res,mimeType[".json"])});
app.post('/delete',function(req,res){var filepath = path.join(viewPath,req.body.file);console.log(filepath);require('fs').unlink(filepath);res.writeHead(200,{'Content-Type':'text/html','Content-Length':'yes'.length});res.end('yes')})

app.post('/tools/:name',function(req,res){
var fileName=req.params.name,extName=path.extname(fileName),filePath="/home/team_auto/pyexec/exec.py -r /home/team_auto/pyexec/tests/Test.rsc tests.testCard.TADxTest",contents=req.body,testname=contents.testname||"",modulename=contents.modulename||"",channelnumber=contents.channelnumber||contents.recordingtime||contents.command||"",dtachannelnumber = contents.dtachannelnumber||"",fileArgs="";
if (testname!="")
 fileArgs+=" -t " + testname;
if(modulename!="")
 fileArgs+=" -m "+ modulename;
if(channelnumber!="")
 fileArgs+=" -c " +channelnumber;
if(dtachannelnumber!="")
 fileArgs+=" -d " +dtachannelnumber;

fileArgs="";

console.log('Request received:'+filePath+fileArgs);isValidFile(filePath,fileArgs,res,mimeType[extName]);
});

app.post('/register',function(req,res){
var devicename=req.body.devicename,deviceip=req.headers['x-forwarded-for']||req.connection.remoteAddress,filePath=path.join(devicePath,'devices.json');
path.exists(filePath,function(exists){
if(exists){fs.readFile(filePath,'utf8',function(err,data){
if(err){console.log('Error: '+err);errMessage='<p class="fail">Error while reading the devices.json. Try again</p>';res.writeHead(200,{'Content-Type':'text/html','Content-Length':errMessage.length});res.end(errMessage);}
else{data=JSON.parse(data);data[devicename]=deviceip;fs.writeFile(filePath,JSON.stringify(data),function(err){
if(err){console.log('Error: '+err);errMessage='<p class="fail">Error while registering the device. Try again</p>';res.writeHead(200,{'Content-Type':'text/html','Content-Length':errMessage.length});res.end(errMessage);}
else{console.log('Successfully registered: '+devicename+'&'+deviceip);successMessage='<p class="pass">Successfully registered the device.</p>';res.writeHead(200,{'Content-Type':'text/html','Content-Length':successMessage.length});res.end(successMessage);}
});}
});
}
else{var tmpObj={};tmpObj[devicename]=deviceip;fs.writeFile(filePath,JSON.stringify(tmpObj),function(err){
if(err){console.log('Error: '+err);errMessage='<p class="fail">Error while registering the device. Try again</p>';res.writeHead(200,{'Content-Type':'text/html','Content-Length':errMessage.length});res.end(errMessage);}
else{console.log('Successfully registered: '+devicename+'&'+deviceip);successMessage='<p class="pass">Successfully registered the device.</p>';res.writeHead(200,{'Content-Type':'text/html','Content-Length':successMessage.length});res.end(successMessage);}
});}
});
});

//Starting the app server
app.listen(port);
console.log('Listening on port '+port);
