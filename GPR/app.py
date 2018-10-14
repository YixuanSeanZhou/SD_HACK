from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Thread, Event
from time import sleep
import eventlet
eventlet.monkey_patch()

# import importlib
# lorem = importlib.import_module("lorem")

app = Flask(__name__)
socketio = SocketIO(app, threaded=True)

thread = Thread()
thread_play = Event()

class StreamData:
    def __init__(self, data, pos, rate):
        self.data = data
        self.pos = pos
        self.rate = rate
        self.eof = False

    def get_chunk(self):
        if self.eof:
            return None
        chunk = self.data[self.pos:self.pos+self.rate]
        self.pos += self.rate
        self.eof = self.pos >= len(self.data)
        return chunk

    def __str__(self):
        return "StreamData[len(data):{} pos:{} rate:{} eof:{}]".format(
                len(self.data), self.pos, self.rate, self.eof)

data = StreamData("abcdefghijklmnopqrstuvwxyz", 0 , 4)

def send_chunk(chunk):
    socketio.emit("chunk", {"chunk": chunk}, broadcast=True)

class StreamThread(Thread):
    def __init__(self, obj=None, pos=None, rate=None):
        super(StreamThread, self).__init__()

    def run(self):
        global data
        print("Start")
        while thread_play.isSet():
            chunk = data.get_chunk()
            print(data)
            if chunk:
                send_chunk(chunk)
                socketio.sleep(1)
            else:
                thread_play.clear()

def start_stream():
    global thread
    if not thread.isAlive():
        thread = StreamThread()
        thread.start()

def toggle():
    global thread, thread_play
    if not thread_play.isSet():
        print("Start")
        thread_play.set()
        start_stream()
    else:
        print("Stop")
        thread_play.clear()

def status_update():
    emit("status_update", {"playing": thread_play.isSet()}, broadcast=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@socketio.on("connect")
def client_connect():
    print("Client conneced")
    status_update()

@socketio.on("disconnect")
def client_disconnect():
    print("Client disconnected")

@socketio.on("status_request")
def status_request():
    print("Status request")
    global thread
    status_update()

@socketio.on("admin_pause")
def admin_pause():
    toggle()
    status_update()

if __name__ == "__main__":
    socketio.run(app, debug=True)
