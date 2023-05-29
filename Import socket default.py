import socket

HOST = '127.0.0.1'  # Localhost
PORT = 8080  # Port to listen on

# HTML for 404 error
not_found = """\
HTTP/1.1 404 Not Found
Content-Type: text/html; charset=utf-8

"""
not_found += open("404notfound.html").read()

# HTML for index page
index_html = """\
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html>
<head>
    <title>Index</title>
</head>
<body>
    <h1>Tubes Jarkom</h1>
    <h2>Kelompok 11</h2>
    <p>M. Rafi Athallah - 1301210210</p>
    <p>Syehan Fariz Gustomo - 1301210530</p>
    <p>Nandika Abiyoga Santosa - 1301213421</p>
</body>
</html>
"""

# Define the function to handle requests
def handle_request(conn):
    # Get the client request
    request = conn.recv(1024).decode('utf-8')
    if not request:
        return
    
    # Get the requested filename from the request
    filename = request.split()[1]
    
    # Serve index page by default if no filename provided
    if filename == '/':
        response = index_html.encode('utf-8')
    else:
        # Try to open the file
        try:
            with open('.' + filename, 'rb') as f:
                content = f.read()
            # Build the response
            response = b'HTTP/1.1 200 OK\n'
            if filename.endswith('.html'):
                response += b'Content-Type: text/html; charset=utf-8\n'
            elif filename.endswith('.css'):
                response += b'Content-Type: text/css; charset=utf-8\n'
            else:
                response += b'Content-Type: text/plain\n'
            response += b'\n' + content
        except FileNotFoundError:
            # File not found, return 404 error
            response = not_found.encode('utf-8')
    
    # Send the response
    conn.sendall(response)
    conn.close()

# Create the socket and start listening
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server listening on http://{HOST}:{PORT}')

    # Accept incoming connections
    while True:
        conn, addr = s.accept()
        print('Connected by {addr[0]}:{addr[1]}')
        handle_request(conn)