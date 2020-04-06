#!/usr/bin/python2

import os

class FilterModule:
    def filters(self):
        return { "is_leader": self.is_leader }

    def is_leader( self, hosts, host, group ):
        all_hosts = list( sorted( [ item for item in hosts if group in hosts[item]['group_names'] ] ) )
        in_group = False

        for item in hosts:
            if (item == host or hosts[item]['ansible_host'] == host) and group in hosts[item]['group_names']:
                in_group = True
                if all_hosts.index( item ) == 0:
                    return "yes"
        return "no" if in_group else None
