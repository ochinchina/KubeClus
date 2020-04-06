#!/usr/bin/python2

import os
import yaml

class FilterModule:
    def filters(self):
        return { "change_apiserver_proxy": self.change_apiserver_proxy}

    def change_apiserver_proxy( self, kubelet_conf, new_apiserver):
        conf = yaml.load( kubelet_conf )
        conf['clusters'][0]['cluster']['server'] = "https://%s:6443" % new_apiserver
        return yaml.dump( conf, default_flow_style=False )
