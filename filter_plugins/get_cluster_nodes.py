#!/usr/bin/python2

import os
import json
class FilterModule:
    def filters(self):
        return { "get_cluster_node_ips": self.get_cluster_node_ips,
                 "get_cluster_nodes": self.get_cluster_nodes,
                 "get_cluster_node_count": self.get_cluster_node_count,
                 "get_flannel_iface": self.get_flannel_iface }

    def get_cluster_node_ips( self, hosts, group ):
        result = []
        for host in hosts:
            if group in hosts[host]['group_names']:
                if 'cluster_ip' in hosts[host]:
                    result.append( hosts[host]['cluster_ip'] )
                elif "SSH_CONNECTION" in hosts[host]['ansible_env']:
                    result.append( hosts[host]['ansible_env']['SSH_CONNECTION'].split()[-2] )
                elif 'default_ipv4' in hosts[host]['ansible_facts']:
                    result.append( hosts[host]['ansible_facts']['default_ipv4']['address'] )
                else:
                    result.append( host )
        result = list( sorted( result ) )
        return result if len( result ) > 0 else None

    def get_cluster_nodes( self, hosts, group ):
        result = []
        for host in hosts:
            if group in hosts[host]['group_names']:
                if 'ansible_hostname' in hosts[host]:
                    result.append( hosts[host]['ansible_hostname'] )
                if 'cluster_ip' in hosts[host]:
                    result.append( hosts[host]['cluster_ip'] )
                elif 'SSH_CONNECTION' in hosts[host]['ansible_env']:
                    result.append( hosts[host]['ansible_env']['SSH_CONNECTION'].split()[-2] )
                elif 'default_ipv4' in hosts[host]['ansible_facts']:
                    result.append( hosts[host]['ansible_facts']['default_ipv4']['address'] )
                else:
                    result.append( host )
        result = list( set( sorted( result ) ) )
        return result if len( result ) > 0 else None

    def get_cluster_node_count( self, hosts, group ):
        cluster_nodes = self.get_cluster_nodes( hosts, group )
        return len( cluster_nodes ) if cluster_nodes is not None else 0

    def get_flannel_iface( self, hosts, group ):
        for host in hosts:
            if group in hosts[host]['group_names']:
                if "flannel_iface" in hosts[host]:
                    return hosts[host]['flannel_iface']
                elif "default_ipv4" in hosts[host]['ansible_facts']:
                    return hosts[host]['ansible_facts']['default_ipv4']['interface']
        return "unknown"

    def print_as_json( self, obj ):
        try:
            print( json.dumps( obj, indent = 2 ) )
        except Exception as ex:
            print( obj )
