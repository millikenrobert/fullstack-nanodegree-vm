import cgi
import os
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:

            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                items = session.query(Restaurant).all()

                output = ""
                output += "<html><body>Hello!<p>"

                for item in items:
                    output += "<p> %s <br/>" % item.name
                    output += "<a href='/restaurants/%s/edit'> Edit </a><br/>" % item.id
                    output += "<a href='/restaurants/%s/delete'> Delete </a><br/>" % item.id

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith('/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                items = session.query(Restaurant).all()

                output = ""
                output += "<html><body><h1>Make a new Restaurant</h1><p>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants'><h2>Add:</h2><input name='newName' type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith('/edit'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurantID = self.path.split('/')[2]

                items = session.query(Restaurant).all()

                output = ""
                output += "<html><body><h1>Edit Restaurant</h1> <p>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><h2>Edit:</h2><input name='newName' type='text'><input type='submit' value='Submit'></form>" % restaurantID
                output += "</body></html>"

                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith('/delete'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurantID = self.path.split('/')[2]

                items = session.query(Restaurant).all()

                output = ""
                output += "<html><body><h1>Delete Restaurant?</h1> <p>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'><input type='submit' value='Delete'></form>" % restaurantID
                output += "</body></html>"

                self.wfile.write(output)
                print(output)
                return
        except IOError:
            self.send_error(404, "File not found")

    def do_POST(self):

        try:
            self.send_response(301)
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newName')

                if self.path.endswith('/new'):

                    try:
                        newEntry = Restaurant(name="%s" % messagecontent[0])
                        session.add(newEntry)
                        session.commit()
                        print('bbbbbooooooooooooooooobbbbbbb')

                    except Exception as e:
                        print("Error %s" % e)
                        print('bbbbbooooooooooooossssoooobbbbbbb')
                        raise e

                    output = ""
                    output += "<html><body>"
                    output += "<h2>New Restaurant Added: </h2>"
                    output += "<h1> %s </h1>" % messagecontent[0]
                    output += "<a href='/restaurants'> Go back to list </a>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print(output)

                if self.path.endswith('/delete'):
                    restaurantID = self.path.split('/')[2]

                    try:

                        deleteEntry = session.query(Restaurant).filter_by(id=restaurantID).one()

                        session.delete(deleteEntry)
                        session.commit()
                        print('Deleted')

                    except Exception as e:
                        print("Error %s" % e)
                        print('bbbbbooooooooooooossssoooobbbbbbb')
                        raise e

                    output = ""
                    output += "<html><body>"
                    output += "<h2>Restaurant Deleted: </h2>"

                    output += "<a href='/restaurants'> Go back to list </a>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print(output)

                if self.path.endswith('/edit'):
                    restaurantID = self.path.split('/')[2]

                    try:

                        newEntry = session.query(Restaurant).filter_by(id=restaurantID).one()
                        newEntry.name = messagecontent[0]
                        session.add(newEntry)
                        session.commit()
                        print('Modified')

                    except Exception as e:
                        print("Error %s" % e)
                        print('bbbbbooooooooooooossssoooobbbbbbb')
                        raise e

                    output = ""
                    output += "<html><body>"
                    output += "<h2>Restaurant Modified: </h2>"
                    output += "<h1> %s </h1>" % messagecontent[0]
                    output += "<a href='/restaurants'> Go back to list </a>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print(output)

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Server is running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("Server interrupted")
        server.socket.close()


if __name__ == '__main__':
    main()
