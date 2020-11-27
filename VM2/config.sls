# Configuration VM2

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
    - ipaddr: 172.16.2.132
    - netmask: 28

## Configuration eth2
eth2:
  network.managed:
    - enabled: True
    - type: eth
    - proto: none
    - ipaddr: 172.16.2.162
    - netmask: 28

routes_ipv6:
  network.routes:
    - name: eth1
    - routes:
      - name: LAN3-6
        ipaddr: fc00:1234:1::/64
        gateway: 172.16.2.131
      - name: LAN1-6
        ipaddr: fc00:1234:1::/64
        gateway: 172.16.2.131

routes_ipv6_2:
  network.routes:
    - name: eth2
    - routes:
      - name: LAN4-6
        ipaddr: fc00:1234:4::/64
        gateway: 172.16.2.163
      - name: LAN2-6
        ipaddr: fc00:1234:2::/64
        gateway: 172.16.2.163