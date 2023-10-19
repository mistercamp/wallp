#!/bin/bash

sudo systemctl stop wallp.service
sudo systemctl disable wallp.service
sudo rm /etc/systemd/system/wallp.service
sudo rm -rf /opt/wallp
