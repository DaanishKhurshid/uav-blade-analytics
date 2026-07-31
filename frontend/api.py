import os
import sys

# Tell Vercel's system loader to look directly into your dashboard runtime
def app(environ, start_response):
    os.system("streamlit run frontend/app.py --server.port=8080 --server.address=0.0.0.0 &")
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [b"UAV Drone Platform Initializing... Refresh Page in 5 seconds."]
