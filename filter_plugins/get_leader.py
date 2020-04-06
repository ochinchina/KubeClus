#!/usr/bin/python2

import os

class FilterModule:
    def filters(self):
        return { "get_leader": self.get_leader }

    def get_leader( self, hosts, group ):
        all_hosts = list( sorted( [ item for item in hosts if group in hosts[item]['group_names'] ] ) )
        if len( all_hosts ) > 0:
            return all_hosts[0]
        return None
