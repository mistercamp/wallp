#!/bin/bash

INSTALL_LOC='/opt/wallp'


echo "SUDO required for install"
sudo apt install python3-venv
sudo mkdir -p $INSTALL_LOC/{tmp,img}
sudo cp -r * $INSTALL_LOC
sudo python3 -m venv $INSTALL_LOC/.venv
sudo $INSTALL_LOC/.venv/bin/python3 -m pip install -r $INSTALL_LOC/requirements.txt
sudo chown -R $USER:$USER $INSTALL_LOC

sed -i "s|__USER__|$USER|" wallp.service
sed -i "s|__DISPLAY__|$DISPLAY|" wallp.service
sed -i "s|__XAUTH__|$XAUTHORITY|" wallp.service
sed -i "s|__XDGRUN__|$XDG_RUNTIME_DIR|" wallp.service

if [ -f /etc/systemd/system/wallp.service ]; then
    sudo systemctl stop wallp.service
    sudo systemctl disable wallp.service
else
    sudo \cp -f ./wallp.service /etc/systemd/system/wallp.service
fi

sudo systemctl enable wallp.service
sudo systemctl start wallp.service

sudo rm $INSTALL_LOC/wallp.service $INSTALL_LOC/install.sh $INSTALL_LOC/requirements.txt
