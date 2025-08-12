#!/bin/bash

# ネームスペース作成
ip netns add ns1
ip netns add ns2

# ns1-veth0 と ns2-veth0 のペアを作成
ip link add ns1-veth0 type veth peer name ns2-veth0

# ネームスペースに仮想イーサネットデバイスを割り当て
ip link set ns1-veth0 netns ns1
ip link set ns2-veth0 netns ns2

# vethインターフェースを有効化
ip netns exec ns1 ip link set ns1-veth0 up
ip netns exec ns2 ip link set ns2-veth0 up

# IPアドレスを割り当て
ip netns exec ns1 ip addr add 192.0.2.1/24 dev ns1-veth0
ip netns exec ns2 ip addr add 192.0.2.2/24 dev ns2-veth0

# MACアドレスを設定
ip netns exec ns1 ip link set dev ns1-veth0 addr 00:00:5E:00:53:01
ip netns exec ns2 ip link set dev ns2-veth0 addr 00:00:5E:00:53:02
