#!/usr/bin/python2

import argparse
import subprocess
import time
import os

def wait_pods_up( pods ):
   """
   wait pods to start-up
   Args:
       pods - a list of pod prefix
   """
   while True:
       try:
           started_pods = []
           all_pods = get_all_pods()
           for pod in all_pods:
               pod_name = pod['name']
               pod_status = pod['status']
               if pod_status == "Running" and len( filter( lambda x: pod_name.startswith( x ), pods ) ) > 0:
                   started_pods.append( pod )
                   print( "pod %s is running" % pod_name )
           if len( started_pods ) >= len( pods ): break
       except Exception as ex:
           print( ex )
       time.sleep( 2 )

def is_tiller_started():
    """
    check if tiller is started and works normally
    """
    for i in range(0,3):
        try:
            subprocess.check_output( ["helm", "list"] )
            print( "tiller is started and works" )
            return True
        except Exception as ex:
            print( ex )
        time.sleep( 5 )
    return False

def delete_tiller_pods():
    """
    delete the tiller pod
    """
    all_pods = get_all_pods()
    for pod in filter( lambda x: x['name'].startswith( "tiller-deploy" ) and x['namespace'] == 'kube-system', all_pods ):
        os.system( "kubectl delete pod %s -n kube-system" % pod['name'] )

def get_all_pods():
    """
    get all pods in the k8s cluster
    """
    pods = []
    out = subprocess.check_output( ['kubectl', 'get', 'pod', '--all-namespaces'] )
    for i, line in enumerate( out.split("\n" ) ):
        if i == 0: continue
        fields = line.split()
        if len( fields ) >= 6: 
            pod = { "namespace": fields[0], "name": fields[1], "status": fields[3] }
            pods.append( pod )
    return pods

def parse_args():
    parser = argparse.ArgumentParser( description = "wait the kubernetes startup" )
    parser.add_argument( "--pod-prefix", nargs = "*", help = "the pod prefix" )
    return parser.parse_args()

def main():
    args = parse_args()
    if args.pod_prefix:
        while True:
            wait_pods_up( args.pod_prefix )
            if len( filter( lambda x: x.startswith( "tiller-deploy" ), args.pod_prefix ) ) <= 0:
                break
            if is_tiller_started(): 
                break
            delete_tiller_pods()

if __name__ == "__main__":
    main()
