#!/bin/sh
create_k8s_cert() {
        echo "generate $1 certificates"
        /usr/local/bin/cfssl gencert -ca="$2.pem" -ca-key="$2-key.pem" --config="ca-config.json" -profile=$3 "$1-csr.json" | /usr/local/bin/cfssljson -bare $1
        mv "$1.pem" "$1.crt"
        mv "$1-key.pem" "$1.key"
}
if [[ -e /etc/kubernetes/pki/ca.key && -e /etc/kubernetes/pki/ca.crt ]]; then
          echo "both ca.key and ca.crt exist"
          openssl x509 -in ca.crt -signkey ca.key -x509toreq -out ca.csr
          openssl x509 -req -days 36500 -in ca.csr -signkey ca.key -out ca.pem
          mv ca.key ca-key.pem
else
          echo "ca.key or ca.crt does not exist"
          /usr/local/bin/cfssl gencert -initca ca-csr.json | /usr/local/bin/cfssljson -bare ca
fi
if [[ -e /etc/kubernetes/pki/front-proxy-ca.key && -e /etc/kubernetes/pki/front-proxy-ca.crt ]]; then
          echo "both front-proxy-ca.key and front-proxy-ca.crt exist"
          openssl x509 -in front-proxy-ca.crt -signkey front-proxy-ca.key -x509toreq -out front-proxy-ca.csr
          openssl x509 -req -days 36500 -in front-proxy-ca.csr -signkey front-proxy-ca.key -out front-proxy-ca.pem
          mv front-proxy-ca.key front-proxy-ca-key.pem
else
          echo "front-proxy-ca.key or front-proxy-ca.crt does not exist"
          /usr/local/bin/cfssl gencert -initca front-proxy-ca-csr.json | /usr/local/bin/cfssljson -bare front-proxy-ca
fi
create_k8s_cert "apiserver" "ca" "server"
create_k8s_cert "front-proxy-client" "front-proxy-ca" "client"
create_k8s_cert "apiserver-kubelet-client" "ca" "client"
create_k8s_cert "apiserver-etcd-client" "etcd/ca" "client"
mv ca.pem ca.crt
mv ca-key.pem ca.key
mv front-proxy-ca.pem front-proxy-ca.crt
mv front-proxy-ca-key.pem front-proxy-ca.key
openssl genrsa -out sa.key 2048
openssl rsa -in sa.key -pubout -out sa.pub

