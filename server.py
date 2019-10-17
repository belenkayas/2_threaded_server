import socket
import json
import threading



sock = socket.socket()
f = open ('logfile.txt', 'w')

port=9090
while True:
    try:
        sock.bind(('',port))
        break
    except:
        port+=1
print(port)

print ("server starts", file = f)
sock.listen(0)
print("listen",file = f)

def clientdef(conn, addr):
	with open("clientsdata.json","r+") as file:
		data=json.loads(file.read())

		for i in data["clients"]:
			if i["ip"]==addr[0]:
				conn.send(b"give your password")
				passwd=conn.recv(1024).decode()
				if passwd==i["passwd"]:
					aut = f"Hello,  {i['name']}"
				else:
					aut = "Your password is incorrect."
				conn.send(aut.encode())
				break
			else:
				conn.send(b"input your name: ")
				name = conn.recv(1024).decode()
				conn.send(b"input your password: ")
				passwd= conn.recv(1024).decode()
				newclient = {"ip": addr[0], "name": name, "passwd":passwd}
				data["clients"].append(newclient)
				file.seek(0)
				file.write(json.dumps(data))


		msg = ''
		while True:
			data = conn.recv(1024)
			print("data from client to server", file = f)
			if not data:
				break
			msg += data.decode()
			conn.send(data)
			print("data from server to client", file = f)
		print(msg)
		conn.close()

while True:
    conn,addr=sock.accept()
    t1=threading.Thread(target=clientdef,args=[conn, addr])
    t1.start()