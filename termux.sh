#!/usr/bin/env bash
pkg update -y
pkg upgrade -y
pkg install -y python3 python3-pip
python3 -m pip install requests
