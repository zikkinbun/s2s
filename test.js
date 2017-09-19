var http = require('http');
var querystring = require('querystring');

var data =  querystring.stringify({
    chn_id: 'DbcMXzmk',
});

var options = {
    hostname: '127.0.0.1',
        port: 8000,
        path: '/app/list',
      method: 'POST',
     headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
};
var req = http.request(options,function(res){
    res.setEncoding('utf8');
    res.on('data',function(chunk){
        var returnData = JSON.parse(chunk);
        console.log(returnDataata);
    });
});

req.write(data);
req.end();
