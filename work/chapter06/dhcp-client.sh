#!/bin/bash

ip netns exec client dhclient -d c-veth0
