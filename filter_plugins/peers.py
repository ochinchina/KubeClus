#!/usr/bin/python2

import os

class FilterModule:
    def filters(self):
        return { "peers": self.peers }

    def peers( self, hosts, group ):
        peers = []
        for host in hosts:
            if group in hosts[host]['group_names']:
                peers.append( hosts[host]['ansible_hostname'] )
                peers.append( host )
        return peers

