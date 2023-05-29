import socket        # mengimpor modul socket, yang digunakan untuk membuat dan mengendalikan socket di Python.

HOST = '127.0.0.1'   # menentukan alamat HOST (localhost) dan PORT (8080) yang akan digunakan oleh server socket.
PORT = 8080

# HTML for 404 error
not_found = """\
HTTP/1.1 404 Not Found
Content-Type: text/html; charset=utf-8

"""
not_found += open("404notfound.html").read()    # untuk membaca file html 404notfound

# HTML for index page
index_html = """\
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

"""
index_html += open("jarkom_tubes.html").read()  # # untuk membaca file html index

# Fungsi untuk menangani permintaan client
def handle_request(conn):                       # menerima objek 'conn' sebagai argumen, yang merupakan koneksi socket dengan client
    # Get the client request
    request = conn.recv(1024).decode('utf-8')   # Fungsi akan menerima permintaan client dan mengkonversinya menjadi byte
    if not request:                             # Fungsi mengembalikan nilai return bila tidak ada permintaan yang diterima dari client
        return          
    
    # Mengambil nama file yang diminta dari request yang diterima
    filename = request.split()[1]       # Permintaan file tsb dibagi menjadi potongan2 berdasarkan spasi, dan elemen ke-2 '[1]' merupakan file yg diminta
    
    # Serve index page by default if no filename provided
    if filename == '/':
        response = index_html.encode('utf-8')
    else:
        # Try to open the file
        try:
            with open('.' + filename, 'rb') as f:   # mencoba membuka file yang diminta ('.' + filename) dalam mode baca biner ('rb')
                content = f.read()                  # Jika file tersebut ditemukan, kontennya akan dibaca dan disimpan dalam variabel content.
            # Build the response                    # Baris ini membangun respons yang akan dikirimkan kembali ke klien.
            response = b'HTTP/1.1 200 OK\n'         # inisiasi
            if filename.endswith('.html'):          # tipe konten (Content-Type) yang sesuai ditambahkan ke respons berdasarkan ekstensi yang diminta. 
                response += b'Content-Type: text/html; charset=utf-8\n'
            elif filename.endswith('.css'):
                response += b'Content-Type: text/css; charset=utf-8\n'
            else:                                   # respons untuk ekstensi selain tipe konten html dan css.
                response += b'Content-Type: text/plain\n'
            response += b'\n' + content             # konten file ditambahkan ke respons menggunakan b'\n' + content.
        except FileNotFoundError:
            # File not found, return 404 error
            response = not_found.encode('utf-8')    # Jika file tidak ditemukan, maka response di enkripsi menjadi byte nenggunakan utf-8
    
    # Send the response
    conn.sendall(response)                          # mengirim response ke klien
    conn.close()                                    # Setelah terkirim, socket ditutup

# Create the socket and start listening
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    # membuat socket menggunakan socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))                                        # lalu mengaitkannya dengan alamat HOST dan PORT menggunakan s.bind((HOST, PORT)).
    s.listen()                                                  # Kemudian, socket mulai mendengarkan permintaan masuk menggunakan s.listen().
    print(f'Server listening on http://{HOST}:{PORT}')          # Pesan yang mencetak URL server saat sedang 'listening'
    # Accept incoming connections
    while True:
        conn, addr = s.accept()                                 # socket menerima koneksi masuk
        print('Connected by {addr[0]}:{addr[1]}')               # ketika koneksi diterima, informasi tentang koneksi tersebut dicetak
        handle_request(conn)                                    # fungsi ini dipanggil untuk menangani permintaan dari klien tersebut.