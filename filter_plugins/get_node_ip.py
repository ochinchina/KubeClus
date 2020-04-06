#!/usr/bin/python2

import os

class FilterModule:
    def filters(self):
        return { "get_node_ip": self.get_node_ip }

    def get_node_ip( self, hosts, host, group ):
        #print "get_node_ip, host=%s, group=%s" % ( host, group )
        group_hosts = list( sorted( [ item for item in hosts if group in hosts[item]['group_names'] ] ) )

        for item in hosts:
            if ( item == host or hosts[item]['ansible_hostname'] == host ) and item in group_hosts:
                if 'cluster_ip' in hosts[item]:
                    return hosts[item]['cluster_ip']
                elif 'SSH_CONNECTION' in hosts[item]['ansible_env']:
                    return hosts[item]['ansible_env']['SSH_CONNECTION'].split()[-2]
                elif 'default_ipv4' in hosts[host]['ansible_facts']:
                    return hosts[host]['ansible_facts']['default_ipv4']['address']
                else:
                    return item
        return None
