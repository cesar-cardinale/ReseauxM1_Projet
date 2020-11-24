# Configuration VM1

## Installation de Python3 sur la VM
python:
  pkg:
    - installed

## Désactivation de network-manager
NetworkManager:
  service:
    - dead
    - enable: False
    
## Suppression de la passerelle par défaut
ip route del default:
  cmd:
    - run

## Configuration eth1
eth1:
  network.managed:
    - enabled: True
    - type: eth
    - proto: none
    - ipaddr: 172.16.2.131
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
    - ipv6ipaddr: fc00:1234:3::1
    - ipv6netmask: 64

## Configuration de la route vers VM2 via LAN1
route_ipv4:
  network.routes:
    - name: eth1
    - routes:
      - name: LAN1
        ipaddr: 172.16.2.160/28
        gateway: 172.16.2.160

## Configuration de la route vers VM1-6 via LAN3-6
route_ipv6:
  network.routes:
    - name: eth2
    - routes:
      - name: LAN3-6
        ipaddr: fc00:1234:3::/64
        gateway: fc00:1234:3::16