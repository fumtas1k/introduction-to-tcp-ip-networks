#!/bin/bash

# ネームスペース作成
ip netns add ns1
ip netns add router
ip netns add ns2

# ns1-veth0 と gw-veth0, gw-veth1, ns2-veth0 のペアを作成
ip link add ns1-veth0 type veth peer name gw-veth0
ip link add ns2-veth0 type veth peer name gw-veth1

# ネームスペースに仮想イーサネットデバイスを割り当て
ip link set ns1-veth0 netns ns1
ip link set gw-veth0 netns router
ip link set gw-veth1 netns router
ip link set ns2-veth0 netns ns2

# 有効化
ip netns exec ns1 ip link set ns1-veth0 up
ip netns exec router ip link set gw-veth0 up
ip netns exec router ip link set gw-veth1 up
ip netns exec ns2 ip link set ns2-veth0 up

# IPアドレスを割り当て
ip netns exec ns1 ip addr add 192.0.2.1/24 dev ns1-veth0
ip netns exec router ip addr add 192.0.2.254/24 dev gw-veth0
ip netns exec router ip addr add 198.51.100.254/24 dev gw-veth1
ip netns exec ns2 ip addr add 198.51.100.1/24 dev ns2-veth0

# デフォルトルート追加
ip netns exec ns1 ip route add default via 192.0.2.254
ip netns exec ns2 ip route add default via 198.51.100.254

# ルーティングを有効化
ip netns exec router sysctl net.ipv4.ip_forward=1

# MACアドレスを設定
ip netns exec ns1 ip link set dev ns1-veth0 addr 00:00:5E:00:53:11
ip netns exec router ip link set dev gw-veth0 addr 00:00:5E:00:53:12
ip netns exec router ip link set dev gw-veth1 addr 00:00:5E:00:53:21
ip netns exec ns2 ip link set dev ns2-veth0 addr 00:00:5E:00:53:22
