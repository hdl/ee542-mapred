import time
import BaseHTTPServer
import csv
import sys


HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8080 # Maybe set this to 9000.

def process_path(path):
    result = {}
    info=path.split('/')[1]
    if 'zip' in info:
        result['zip'] = info.split('=')[1]
    else:
        result['zip'] = ''
    return result

# 'Station Name', #0
# 'Station Address', #1
# 'City',#2
# 'Zip', #3
# 'Phone', #4
# 'Hours', #5
# 'Charger Network', #6
# 'Latitude', #7
# 'Longitude', #8
# 'Score', #9
# 'Businesses'] #10
def process_keyword(zip):
    result = ''
    f = open('YelpResults.csv', 'rt')
    reader = csv.reader(f)
    i = 0
    for row in reader:
        if row[3] == zip:
            tr = "<tr>"
            tr += "<td>"+row[0]+"</td>"
            tr += "<td>"+row[1]+"</td>"
            tr += "<td>"+row[9]+"</td></tr>"
            result += tr
    f.close()
    return result

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        print "do head"
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Web demo</title></head>")
        search_form = '''
        <body><p align="center">EE542 Team5 Web Demo</p>
        <form align="center" action="search">
        Zip code:
        <input size= type="text" name="zip">
        <input type="submit" value="Search">
        </form> 
        ''' 
        s.wfile.write(search_form)
        info = process_path(s.path)
        if info['zip'] != '':
            table_header = '''
              <table align="center">
              <tr>
                  <td width="60%">Station Name</td>
                  <td>Station address</td>
                  <td>Score</td> 
              </tr>'''
            s.wfile.write(table_header)
            s.wfile.write(process_keyword(info['zip']))
            s.wfile.write("</table>")
        s.wfile.write("</body></html>")


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)


        
