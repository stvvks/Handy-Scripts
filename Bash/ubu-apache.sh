#!/bin/bash

#Get sudo priv
sudo su

#Update and Install

apt update -y && apt upgrade -y

sleep 1

apt install apache2 -y
sleep 1
ufw app list
ufw allow 'Apache'
echo "Checking status"
ufw status
sleep 5
systemctl start apache2
echo "Checking apache status"
systemctl status apache2

#end of script