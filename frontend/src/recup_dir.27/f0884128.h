#!/usr/bin/bash
#
# fc_wwpn_id
#
# Generates device node names links based on FC WWPN
# Copyright (c) 2016-2021 Hannes Reinecke, SUSE Linux GmbH
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation version 2 of the License.
#

DEVPATH=$1
SCSIPATH=$(cd -P "/sys$DEVPATH/device" || exit; echo "$PWD")

d=$SCSIPATH
[ -d "$d/scsi_disk" ] || exit 0
target_lun=${d##*:}

while [ -n "$d" ] ; do
    d=${d%/*}
    e=${d##*/}
    case "$e" in
	rport*)
	    rport=$e
	    rport_dir="/sys/class/fc_remote_ports/$rport"
	    if [ -d "$rport_dir" ] ; then
		rport_wwpn=$(cat "$rport_dir/port_name")
	    fi
	    ;;
	host*)
	    host=$e
	    host_dir="/sys/class/fc_host/$host"
	    if [ -d "$host_dir" ] ; then
		host_wwpn=$(cat "$host_dir/port_name")
		break;
	    fi
    esac
done

if [ -n "$rport_wwpn" ] || [ -n "$host_wwpn" ] ; then
    echo "FC_TARGET_LUN=$target_lun"
fi

if [ -n "$rport_wwpn" ] ; then
    echo "FC_TARGET_WWPN=$rport_wwpn"
fi

if [ -n "$host_wwpn" ] ; then
    echo "FC_INITIATOR_WWPN=$host_wwpn"
fi
