import http.server as BaseHTTPServer
import json
import os
import sys
import urllib.parse as urlparse
import webbrowser

import stravalib


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    # Handle the web data sent from the strava API
    def do_HEAD(self):
        return self.do_GET()

    def do_GET(self):
        # Get the API code for Strava
        # self.wfile.write(b'<script>window.close();</script>')
        code = urlparse.parse_qs(urlparse.urlparse(self.path).query)['code'][0]
        # Login to the API
        token = useCode(code)
        # Create page
        self.send_response(200)
        self.send_header(b"Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>Token received</title></head>")
        self.wfile.write(
            bytes("<body><p>Received and saved access token %s </p>" % str(token['access_token']), "utf-8"))
        self.wfile.write(b"</body></html>")
        return self.save_token(token)

    def save_token(self, token):
        with open(os.path.join('tokens', 'user_access.token'), 'w') as file:
            file.write(json.dumps(token))


def getclientinfo():
    # Put your data in file 'tokens/client.token' and separate the fields with a comma: clientid,clientsecrettoken
    with open(os.path.join('tokens', 'client.token'), 'r') as file:
        client_secret = file.read().split(',')
    client_id, secret = client_secret[0], client_secret[1]
    return client_id, secret


def useCode(code):
    client_id, secret = getclientinfo()
    client = stravalib.client.Client()
    # Retrieve the login code from the Strava server
    access_token = client.exchange_code_for_token(client_id=client_id,
                                                  client_secret=secret, code=code)
    return access_token


def authorize():
    port = 8008
    url = 'http://localhost:%d/authorization' % port
    client_id, __ = getclientinfo()
    # Create the strava client, and open the web browser for authentication
    client = stravalib.client.Client()
    authorize_url = client.authorization_url(client_id=client_id,
                                             redirect_uri=url,
                                             approval_prompt='auto',
                                             scope='activity:read_all')
    print('Opening: %s' % authorize_url)
    webbrowser.open(authorize_url)
    try:
        httpd = BaseHTTPServer.HTTPServer(('localhost', port), MyHandler)
        httpd.handle_request()
    except KeyboardInterrupt:
        # Allow ^C to interrupt from any thread.
        sys.stdout.write('\033[0m')
        sys.stdout.write('User Interupt\n')


def save_token(token):
    with open(os.path.join('tokens', 'user_access.token'), 'w') as file:
        file.write(json.dumps(token))


def refresh(refresh_token):
    client = stravalib.client.Client()
    with open(os.path.join('tokens', 'client.token'), 'r') as file:
        client_secret = file.read().split(',')
    client_id, secret = client_secret[0], client_secret[1]
    token = client.refresh_access_token(client_id, secret, refresh_token)
    save_token(token)
    return token
