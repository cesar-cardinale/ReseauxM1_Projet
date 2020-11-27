# Configuration VM3

## Installation de Python3 sur la VM
python:
  pkg:
    - installed

## Installation du serveur ECHO sur la VM
inetutils-inetd:
  pkg:
    - installed

## Ajout du service ECHO dans la BD de inetd
update-inetd --add "echo stream tcp6 nowait nobody internal":
  cmd:
    - run

## Lancement et activation de inetd
service inetutils-inetd start:
  cmd:
    - run
service inetutils-inetd restart:
  cmd:
    - run

## Désactivation de network-manager
NetworkManager:
  service:
    - dead
    - enable: False
    
## Suppression de la passerelle par défaut --> non car serveur ECHO
#ip route del default:
#  cmd:
#    - run

## Ajout forwarding ipv6
net.ipv6.conf.all.forwarding:
  sysctl:
    - present
    - value: 1

## Ajout forwarding ipv4
net.ipv4.ip_forward:
  sysctl:
    - present
    - value: 1

## Configuration eth1
eth1:
  network.managed:
    - enabled: True
    - type: eth
    - proto: none
    - ipaddr: 172.16.2.163
    - netmask: 28

## Configuration eth2
eth2:
  network.managed:
    - enabled: True
    - type: eth
    - proto: none
    - enable_ipv4: false
    - ipv6proto: static
    - enable_ipv6: true
    - ipv6_autoconf: no
    - ipv6ipaddr: fc00:1234:4::3
    - ipv6netmask: 64

## Configuration de la route vers VM2 via LAN2
route_ipv4:
  network.routes:
    - name: eth1
    - routes:
      - name: LAN2
        ipaddr: 172.16.2.160/28
        gateway: 172.16.2.162

## Configuration de la route vers VM3-6 via LAN4-6
route_ipv6:
  network.routes:
    - name: eth2
    - routes:
      - name: LAN4-6
        ipaddr: fc00:1234:4::/64
        gateway: fc00:1234:4::3