#!/usr/bin/python2

import os

class FilterModule:
    def filters(self):
        return { "path_join": self.path_join }
    def path_join( self, files, directory):
        if isinstance( files, list ):
            return [ os.path.join( directory, f ) for f in files ]
        else:
            return os.path.join( directory, files )
