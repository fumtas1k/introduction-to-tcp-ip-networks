#!/bin/bash

# ネームスペースの作成
ip netns add server
ip netns add client

#
ip link add s-veth0 type veth peer name c-veth0

# ネームスペースに仮想イーサネットデバイスを割り当て
ip link set s-veth0 netns server
ip link set c-veth0 netns client

# ネームスペース内の仮想イーサネットデバイスを有効化
ip netns exec server ip link set s-veth0 up
ip netns exec client ip link set c-veth0 up

# ネームスペース内の仮想イーサネットデバイスにIPアドレスを割り当て
ip netns exec server ip addr add 192.0.2.254/24 dev s-veth0

# DHCPサーバーの起動
ip netns exec server dnsmasq \
  --dhcp-range=192.0.2.100,192.0.2.200,255.255.255.0 \
  --interface=s-veth0 \
  --port 0 \
  --no-resolv \
  --no-daemon
