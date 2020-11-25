# Configuration VM3-6

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
    - enable_ipv4: false
    - ipv6proto: static
    - enable_ipv6: true
    - ipv6_autoconf: no
    - ipv6ipaddr: fc00:1234:2::36
    - ipv6netmask: 64

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
    - ipv6ipaddr: fc00:1234:4::36
    - ipv6netmask: 64

## Configuration de la route vers VM2-6 via LAN2-6
route_ipv6:
  network.routes:
    - name: eth1
    - routes:
      - name: LAN2-6
        ipaddr: fc00:1234:2::/64
        gateway: fc00:1234:2::26

## Configuration de la route vers VM3 via LAN4-6
route_ipv6_2:
  network.routes:
    - name: eth2
    - routes:
      - name: LAN4-6
        ipaddr: fc00:1234:4::/64
        gateway: fc00:1234:4::3