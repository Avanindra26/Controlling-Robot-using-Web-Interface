var http = require('http').createServer(handler);
var fs = require('fs');
var io = require('socket.io')(http);
var { exec, spawn } = require('child_process');

http.listen(8080);

let continuousMovement = false;
let script3Process;

function handler(req, res) {
  fs.readFile(__dirname + '/public/index.html', function(err, data) {
    if (err) {
      res.writeHead(404, {'Content-Type': 'text/html'});
      return res.end("404 Not Found");
    }
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write(data);
    return res.end();
  });
}

io.sockets.on('connection', function(socket) {
  socket.on('move_robot', function(data) {
    if (data) {
      exec('python3 ./python/script_1.py', (error, stdout, stderr) => {
        if (error) {
          console.error(`Error executing script: ${error}`);
          return;
        }
        let robotData;
        try {
          robotData = JSON.parse(stdout);
        } catch (e) {
          console.error('Error parsing JSON:', e);
          return;
        }
        socket.emit('robot_data', robotData);
      });
    }
  });

  socket.on('move_robot_random', function(data) {
    if (data) {
      exec('python3 ./python/script_2.py', (error, stdout, stderr) => {
        if (error) {
          console.error(`Error executing script: ${error}`);
          return;
        }
        let robotData;
        try {
          robotData = JSON.parse(stdout);
        } catch (e) {
          console.error('Error parsing JSON:', e);
          return;
        }
        socket.emit('robot_data', robotData);
      });
    }
  });

  socket.on('continuous_movement', function(data) {
    continuousMovement = data;
    if (continuousMovement) {
      if (!script3Process || script3Process.killed) {
        script3Process = spawn('python3', ['./python/script_3.py'], { stdio: ['pipe', 'pipe', 'pipe'] });

        script3Process.stdout.on('data', (data) => {
          let robotData;
          try {
            robotData = JSON.parse(data.toString());
            socket.emit('robot_data', robotData);
          } catch (e) {
            console.error('Error parsing JSON:', e);
          }
        });

        script3Process.stderr.on('data', (data) => {
          console.error(`stderr from script_3.py: ${data}`);
        });

        script3Process.on('exit', (code, signal) => {
          console.log(`script_3.py process exited with code ${code} and signal ${signal}`);
        });
      }
    } else {
      if (script3Process && !script3Process.killed) {
        script3Process.on('exit', (code, signal) => {
          console.log(`script_3.py process exited with code ${code} and signal ${signal}`);
          exec('python3 ./python/script_4.py', (error, stdout, stderr) => {
            if (error) {
              console.error(`Error executing script_4.py: ${error}`);
              return;
            }
            let robotData;
            try {
              robotData = JSON.parse(stdout);
              socket.emit('robot_data', robotData);
            } catch (e) {
              console.error('Error parsing JSON:', e);
            }
            console.log(`stdout from script_4.py: ${stdout}`);
            console.error(`stderr from script_4.py: ${stderr}`);
          });
        });
        script3Process.kill();
      }
    }
  });
});

process.on('SIGINT', function() {
  if (script3Process && !script3Process.killed) {
    script3Process.kill();
  }
  process.exit();
});
