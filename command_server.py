from socketserver import BaseRequestHandler, ThreadingTCPServer
import traceback

import filter
import plot

def rnt(string):
    return str(string).replace('\b','').replace('\r','').replace('\t','    ').replace('\n', '\r\n')


class CommandHandler(BaseRequestHandler):

    def print(self, obj):
        self.request.send(str(obj).encode())

    def handle(self):
        #print('Got connection from ', self.client_address)
        self.request.send(rnt('Command Server\n').encode())
        buffer = ''
        while True:
            input = self.request.recv(256)
            if not input:
                break

            for ch in input.decode():
                if ch == '\n':
                    try:
                        r = exec(buffer)                
                        if r != None:
                            self.request.send(rnt(r).encode())                           

                    except Exception as e:
                        self.request.send(rnt(traceback.format_exc()).encode())                        
                    buffer = ''

                else:
                    buffer+=ch       

    

def run_command_server():
    serv = ThreadingTCPServer(('',9000),CommandHandler)
    serv.serve_forever()

def run_command_server_thread():
    import threading
    threading.Thread(target=run_command_server, name='command server').start()

if __name__=='__main__':
    run_command_server()