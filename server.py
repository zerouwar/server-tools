import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse as urlparse

hostName = "localhost"
serverPort = 8080
savePath = '/sftp/public/'


class MyServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        parseUrl = urlparse.urlparse(self.path)
        if (parseUrl.path == '/wget'):
            self.wget(parseUrl)
        else:
            self.return_simple_message(404, "未找到相关命令")

    def wget(self, parseUrl):
        queryParams = urlparse.parse_qs(parseUrl.query)

        downloadUrl = queryParams['url'][0]
        name = queryParams['name'][0]

        res = subprocess.call(['wget', downloadUrl, '-O', '' + savePath + name])

        if (res == 0):
            self.return_simple_message(200, "下载中，可能需要一点时间，完成后可点击此链接下载<a>http://ftp.chenhuanming.cn/" + name + "</a>")
        else:
            self.return_simple_message(400, "下载失败")

    def return_simple_message(self, code, message):
        self.send_response(code)
        self.send_header("Content-type", "text/html;charset=UTF-8")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>wget</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>" + message + "</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
