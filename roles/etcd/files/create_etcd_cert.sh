#!/bin/sh

create_etcd_cert() {
  echo "generate $1 certificates"
  /usr/local/bin/cfssl gencert -ca=ca.pem -ca-key="ca-key.pem" --config="ca-config.json" -profile=$1 "$1-csr.json" | /usr/local/bin/cfssljson -bare $1
}

/usr/local/bin/cfssl gencert -initca ca-csr.json | /usr/local/bin/cfssljson -bare ca
create_etcd_cert "client"
create_etcd_cert "peer"
create_etcd_cert "server"

