# coding: utf8
import fcntl
import os
import struct
import subprocess
import sys
import argparse
import socket
import time
from multiprocessing import Process

# Flags: IFF_TUN   - TUN device (no Ethernet headers)
#        IFF_TAP   - TAP device
#        IFF_NO_PI - Do not provide packet information
TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000


def tun_alloc(name):
    print('> Configuration de {} ...'.format(name))
    fd = open('/dev/net/tun', 'r+b')
    ifr = struct.pack('16sH', name, IFF_TUN)
    fcntl.ioctl(fd, TUNSETIFF, ifr)

    subprocess.check_call('ip -6 addr add fc00:1234:ffff::1/64 dev ' + name, shell=True)
    subprocess.check_call('ip -6 link set ' + name + ' up', shell=True)

    if fd:
        print('> {} correctement linké sur fc00:1234:ffff::1/64'.format(name))
    else:
        exit('> ! Erreur lors de la configuration de {}'.format(name))

    return fd


def tun_read(src):
    output = os.fdopen(1, 'w')
    while True:
        buffer = os.read(src.fileno(), 120)
        output.write(buffer)
        output.flush()
        if len(buffer) == 0:
            break
    os.close(src.fileno())


ADDRESS = ''
PORT = 123


# Crée un serveur TCP sur le PORT et redirige le trafic TCP reçu vers le tunnel FD
def ext_out(ip_serv, fd):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((ip_serv, PORT))

        print("> Serveur TCP lancé sur le port {} à l'adresse {}.".format(PORT, ip_serv))

        while True:
            server.listen(5)
            client, address = server.accept()
            print("-> {} connecté".format(address))

            while True:
                response = client.recv(1024)
                if response != "":
                    os.write(fd.fileno(), response)
                    print("--> Données transférées depuis le serveur TCP vers le tunnel.")
                else:
                    break

            print("-> {} déconnecté".format(address))
            client.close()
    except KeyboardInterrupt:
        server.close()
        print("\n> Arrêt du serveur TCP.")


# Crée un client et redirige le trafic du tunnel FD vers le serveur TCP
def ext_in(ip_serv, port, fd):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((ip_serv, port))
        print("> Connecté au serveur {} sur le port {}".format(ip_serv, port))
        while True:
            if write_from_fd(fd, server) == 0:
                break
        server.close()
    except socket.error:
        print("> ! La connexion au serveur a échoué.")
        time.sleep(4)
        ext_in(ip_serv, port, fd)
    except KeyboardInterrupt:
        print("\n> Arrêt de la connexion avec le serveur TCP.")
        server.close()


# Fonction qui transfère les données provenant du tunnel SRC vers la socket DST
def write_from_fd(src, dst):
    if src.fileno():
        buffer = os.read(src.fileno(), 1024)
        if dst.send(buffer):
            print("-> Données transférées depuis le tunnel vers le serveur TCP.")
            return 1
        else:
            return 0
    else:
        return 0


# On vérifie que le script est exécuté par un administrateur
if os.geteuid() != 0:
    exit('Il faut les droits administrateur pour exécuter ce script. \n '
         'Veuillez recommencer en précédant la commande de \'sudo\'')

# On parse les arguments pour trouver le nom de l'action
parser = argparse.ArgumentParser()
parser.add_argument("action")
args = parser.parse_args()

if args.action == 'tun0':
    tunfd = tun_alloc(args.action)
    tun_read(tunfd)
elif args.action == 'ext_in':
    tunfd = tun_alloc('tun0')
    p1 = Process(target=ext_out, args=('172.16.2.163', tunfd))
    p2 = Process(target=ext_in, args=('172.16.2.131', PORT, tunfd))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

elif args.action == 'ext_out':
    tunfd = tun_alloc('tun0')
    p1 = Process(target=ext_out, args=('172.16.2.131', tunfd))
    p2 = Process(target=ext_in, args=('172.16.2.163', PORT, tunfd))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
