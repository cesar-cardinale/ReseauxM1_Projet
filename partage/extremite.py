# coding: utf-8
import socket

ADRESSE = ''
PORT = 123


class Extremite:
    def ext_out(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ADRESSE, PORT))

        while True:
            server.listen(5)
            client, address = server.accept()
            print("{} connected".format(address))

            response = client.recv(255)
            if response != "":
                print(response)
            else:
                client.close()

        server.close()

    def ext_in(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((ADRESSE, PORT))
        print("Connexion au serveur {} sur le port {}".format(ADRESSE, PORT))

        server.send("Hey my name is Olivier!")

        print("Close")
        server.close()



extremite = Extremite()
extremite.ext_out()
