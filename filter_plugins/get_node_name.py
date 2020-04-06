#!/usr/bin/python2

import os

class FilterModule:
    def filters(self):
        return { "get_node_name": self.get_node_name }

    def get_node_name( self, hosts, host ):
        for item in hosts:
            if item == host:
                return hosts[item]['ansible_hostname']
        return None
