#!/bin/sh

sudo pppd \
	socket localhost:8888 \
	115200 \
	debug \
	local \
	nodetach \
	silent \
	noauth \
	172.10.10.1:172.10.10.2
