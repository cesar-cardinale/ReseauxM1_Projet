# coding: utf8
import fcntl
import os
import struct
import subprocess
import sys
import argparse
import socket

# Flags: IFF_TUN   - TUN device (no Ethernet headers)
#        IFF_TAP   - TAP device
#        IFF_NO_PI - Do not provide packet information
TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000


def tun_alloc(name):
    f = open('/dev/net/tun', 'r+b')
    ifr = struct.pack('16sH', name, IFF_TUN)
    fcntl.ioctl(f, TUNSETIFF, ifr)

    subprocess.check_call('ip -6 addr add fc00:1234:ffff::1/64 dev ' + name, shell=True)
    subprocess.check_call('ip -6 link set ' + name + ' up', shell=True)

    if f:
        print('{} correctement lancé avec fc00:1234:ffff::1/64'.format(name))
    else:
        exit('Erreur lors de la configuration de {}'.format(name))

    return f


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


# Crée un serveur le PORT et à l'ADDRESS donnés
def ext_out():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ADDRESS, PORT))

    print("Serveur lancé sur {}.".format(socket.gethostbyname(socket.getfqdn())))

    while True:
        server.listen(5)
        client, address = server.accept()
        print("{} connecté".format(address))

        while True:
            response = client.recv(1024)
            if response != "":
                print(response)
            else:
                break

        print("{} déconnecté".format(address))
        client.close()

    server.close()


def ext_in(ip_serv, port, tunfd):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((ip_serv, port))
        print("Connecté au serveur {} sur le port {}".format(ip_serv, port))
        while True:
            if write_in_fd(tunfd, server) == 0:
                break
        server.close()
    except socket.error:
        print("La connexion au serveur a échoué.")
        sys.exit()

    # server.send("Hey my name is Olivier!")


# Fonction qui transfère les données provenant du tunnel SRC vers la socket DST
def write_in_fd(src, dst):
    if src.fileno():
        buffer = os.read(src.fileno(), 1024)
        dst.send(buffer)
        return 1
    else:
        return 0


# On vérifie que le script est exécuté par un administrateur
if os.geteuid() != 0:
    exit('Il faut les droits administrateur pour exécuter ce script. \n '
         'Veuillez recommencer en précédant la commande de \'sudo\'')

# On parse les arguments pour trouver le nom du tunnel
parser = argparse.ArgumentParser()
parser.add_argument("action")
args = parser.parse_args()

if args.action == 'tun0':
    print('Configuration de {}'.format(args.action))
    tunfd = tun_alloc(args.action)
    tun_read(tunfd)
elif args.action == 'ext_in':
    tunfd = tun_alloc('tun0')
    ext_in('172.16.2.131', PORT, tunfd)
elif args.action == 'ext_out':
    ext_out()
