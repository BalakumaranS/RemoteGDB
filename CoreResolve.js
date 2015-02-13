var formidable = require('formidable'),
    http = require('http'),
    util = require('util'),
    PythonShell = require('python-shell');

http.createServer(function(req, res) {
  if (req.url == '/xdta_coredump' && req.method.toLowerCase() == 'post') {
    // parse a file upload
    var form = new formidable.IncomingForm();

    form.parse(req, function(err, fields, files) {
     
      fpath = files.upload.path;
      fname = files.upload.name;
      
      var options = {
      pythonPath: '/usr/bin/python',
      scriptPath: '/home/team_auto/pyexec/tests/pkdta/CoreDumpResolve/CoreDumpResolver/',
      pythonOptions: ['-u'],
      args: [fpath]
      
      };

    PythonShell.run('CoreResolver.py', options, function (err, results) {
    if (err) throw err;
    // results is an array consisting of messages collected during execution
    console.log('results: %j', results);
    res.writeHead(200,{'Content-Type':'text/plain'});
   // res.write('Received upload:\n\n');
    res.end(String(results));
        });
    });

    return;
  }

  // show a file upload form
  res.writeHead(200, {'content-type': 'text/html'});
  res.end(
    '<form action="/xdta_coredump" enctype="multipart/form-data" method="post">'+
    '<input type="file" name="upload" multiple="multiple"><br>'+
    '<input type="submit" value="Upload dump">'+
    '</form>'
  );
}).listen(9876);
