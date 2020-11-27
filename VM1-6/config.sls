# Configuration VM1-6

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

## Ajout forwarding ipv6
net.ipv6.conf.all.forwarding:
  sysctl:
    - present
    - value: 1

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
    - ipv6ipaddr: fc00:1234:3::16
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
    - ipv6ipaddr: fc00:1234:1::16
    - ipv6netmask: 64


## Configuration des routes
routes:
  network.routes:
    - name: eth2
    - routes:
      - name: LAN2-6
        ipaddr: fc00:1234:2::/64
        gateway: fc00:1234:1::26
      - name: LAN4-6
        ipaddr: fc00:1234:4::/64
        gateway: fc00:1234:1::26