#!/bin/sh
#FreeDNS updater script

#UPDATEURL="http://freedns.afraid.org/dynamic/update.php?SWJTV1p5ZE5Mc3hQYThpbzY3c0JTVm12OjE1ODMwMDM2"
#DOMAIN="shastcam.ignorelist.com"

#registered=$(nslookup $DOMAIN|tail -n2|grep A|sed s/[^0-9.]//g)

 # current=$(wget -q -O - http://checkip.dyndns.org|sed s/[^0-9.]//g)
#       [ "$current" != "$registered" ] && {
#          wget -q -O /dev/null $UPDATEURL
#          echo "DNS updated on:"; date
 # }
wget -q --read-timeout=0.0 --waitretry=5 --tries=200 --background http://freedns.afraid.org/dynamic/update.php?SWJTV1p5ZE5Mc3hQYThpbzY3c0JTVm12OjE1ODMwMDM2 -O /dev/null
