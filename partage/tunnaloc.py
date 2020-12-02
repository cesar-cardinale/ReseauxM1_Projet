# coding: utf8
import fcntl
import os
import struct
import subprocess
import sys
import argparse

# Flags: IFF_TUN   - TUN device (no Ethernet headers)
#        IFF_TAP   - TAP device
#        IFF_NO_PI - Do not provide packet information
TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000


def tun_alloc(name):
    f = open('/dev/net/tun', 'r+b')
    ifr = struct.pack('16sH', args.name, IFF_TUN)
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
        bytes = os.read(src.fileno(), 120)
        output.write(bytes)
        output.flush()
        if len(bytes) == 0:
            break
    os.close(src.fileno())


# On vérifie que le script est exécuté par un administrateur
if os.geteuid() != 0:
    exit('Il faut les droits administrateur pour exécuter ce script. \n '
         'Veuillez recommencer en précédant la commande de \'sudo\'')

# On parse les arguments pour trouver le nom du tunnel
parser = argparse.ArgumentParser()
parser.add_argument("name")
args = parser.parse_args()

print('Configuration de {}'.format(args.name))

tunfd = tun_alloc(args.name)

tun_read(tunfd)
