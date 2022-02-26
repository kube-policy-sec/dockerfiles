from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess

class handler(BaseHTTPRequestHandler):
    def _set_response(self, code, output):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(output).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        data = json.loads(post_data.decode('utf-8'))
        # The following is _VERY_ insecure and should not be used. It is however used as a PoC.
        # Since the subprocess takes in a user argument it is vulnerable for arbitrary code execution.
        # Sanitizing the data['image'] is one way to secure it somewhat.
        output = subprocess.run(['trivy', '-q', 'i', '--format=json', data["image"]], stdout=subprocess.PIPE)
        try: 
            res = json.loads(output.stdout)
            self._set_response(200, res)
        except:
            res = "internal error"
            self._set_response(500, res)

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8123)
    httpd = server_class(server_address, handler)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
