#!/usr/bin/python2

import os

class FilterModule:
    def filters(self):
        return { "get_count_in_group": self.get_count_in_group }

    def get_count_in_group( self, hosts, group ):
        all_hosts = list( sorted( [ item for item in hosts if group in hosts[item]['group_names'] ] ) )
        return len( all_hosts )
