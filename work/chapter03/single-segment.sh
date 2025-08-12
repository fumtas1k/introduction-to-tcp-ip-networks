#!/bin/bash

# namespaceの作成
ip netns add ns1
ip netns add ns2

# vethペアの作成
ip link add ns1-veth0 type veth peer name ns2-veth0

# vethペアをそれぞれのnamespaceに移動
ip link set ns1-veth0 netns ns1
ip link set ns2-veth0 netns ns2

# vethインターフェースにIPアドレスを割り当て
ip netns exec ns1 ip addr add 192.0.2.1/24 dev ns1-veth0
ip netns exec ns2 ip addr add 192.0.2.2/24 dev ns2-veth0

# vethインターフェースを有効化
ip netns exec ns1 ip link set ns1-veth0 up
ip netns exec ns2 ip link set ns2-veth0 up
