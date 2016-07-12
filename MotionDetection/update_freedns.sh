#!/bin/sh
#FreeDNS updater script

wget -q --read-timeout=0.0 --waitretry=5 --tries=2 --background http://freedns.afraid.org/dynamic/update.php?SWJTV1p5ZE5Mc3hQYThpbzY3c0JTVm12OjE1ODMwMDM2 -O /dev/null
