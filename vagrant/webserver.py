from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

## import for CRUD operations ##
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<a href='/restaurants/new'>Add new Restaurant<a><br>"
            restaurants = session.query(Restaurant).all()
            for restaurant in restaurants:
                output += restaurant.name
                output += "<br><a href='#'>Edit</a>"
                output += "<br><a href='#'>Delete</a>"
                output += "<br><br>"    
            output += "</body></html>"
            self.wfile.write(output)
            #print output
            return
            
        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>Add a New Restaurant</h1>"
            output += "<form method='POST' enctype='multipart/form-data' action='/restaurants'><input name='restaurantName' type='text'><input type='submit' value='Submit'></form>"
            output += "</body></html>"
            self.wfile.write(output)
            return
            
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>Hello!</h1>"
            output += "<form method='POST' enctype='multipart/form-data' action='/post'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit'' value='Submit'> </form>"
            output += "</body></html>"
            self.wfile.write(output)
            print output
            return
            
        if self.path.endswith("/halo"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>&#161 Hola !</h1>"
            output += "<form method='POST' enctype='multipart/form-data' action='/post'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit'' value='Submit'> </form>"
            output += "</body></html>"
            self.wfile.write(output)
            print output
            return
            
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)
            
    def do_POST(self):
        try:
            """
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += "<form method='POST' enctype='multipart/form-data' action='/post'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit'' value='Submit'> </form>"
            output += "</body></html>"
            self.wfile.write(output)
            print output
            """
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                restaurantName = fields.get('restaurantName')
            newRestaurant = Restaurant(name = restaurantName[0])
            session.add(newRestaurant)
            session.commit()
            output = ""
            output += "<html><body>"
            output += "<a href='/restaurants/new'>Add new Restaurant<a><br>"
            restaurants = session.query(Restaurant).all()
            for restaurant in restaurants:
                output += restaurant.name
                output += "<br><a href='#'>Edit</a>"
                output += "<br><a href='#'>Delete</a>"
                output += "<br><br>"    
            output += "</body></html>"
            self.wfile.write(output)
            
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Restaurant Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

## run the main method immediately when executing the script
if __name__ == '__main__':
    main()