# Configuration VM3-6

## Désactivation de network-manager
NetworkManager:
  service:
    - dead
    - enable: False
    
## Suppression de la passerelle par défaut --> non car serveur ECHO
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

## Configuration des routes
eth1-routes:
  network.routes:
    - name: eth1
    - routes:
      - name: LAN3-6
        ipaddr: fc00:1234:3::/64
        gateway: fc00:1234:2::26
      - name: LAN1-6
        ipaddr: fc00:1234:1::/64
        gateway: fc00:1234:2::26

## Connexion internet pour pouvoir installer les packets
dhclient eth0:
  cmd.run

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