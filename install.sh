#!/bin/bash

. /etc/os-release

if [ -z "$ID_LIKE" ]; then
    OS=$ID
else
    OS=$ID_LIKE
fi

FONTS_FILE=https://github.com/GDGVIT/HandWriter/raw/master/assets/roboto.zip

if [ "$OS" = "arch" ]
then
    echo "Installing the HandWriter package"
    curl -O https://fbs.sh/SaurusXI/HandWriter/public-key.gpg && sudo pacman-key --add public-key.gpg && sudo pacman-key --lsign-key 29D5FDA07C763B56745B9E598AC59FA1ADE43023 && rm public-key.gpg
    
    echo -e '\n[HandWriter]\nServer = https://fbs.sh/SaurusXI/HandWriter/arch' | sudo tee -a /etc/pacman.conf
    sudo pacman -Syu handwriter
    
    echo "Installing fonts"
    curl $FONTS_FILE -o ~/roboto.zip -L
    unzip ~/roboto.zip -d ~/roboto-font
    mkdir ~/.local/share/fonts
    cp ~/roboto-font/* ~/.local/share/fonts/
    
    echo "Cleaning up"
    rm ~/roboto.zip && rm -r ~/roboto-font
    
    echo "Adding HandWriter to PATH"
    cd /usr/local/bin
    sudo ln -s /opt/HandWriter/HandWriter

elif [ "$OS" = "fedora" ]
then
    echo "Installing the HandWriter package"
    sudo rpm -v --import https://fbs.sh/SaurusXI/HandWriter/public-key.gpg
    sudo dnf config-manager --add-repo https://fbs.sh/SaurusXI/HandWriter/rpm/HandWriter.repo
    yes | sudo dnf install handwriter
    
    echo "Installing fonts"
    wget $FONTS_FILE -O ~/roboto.zip
    unzip ~/roboto.zip -d ~/roboto-font
    mkdir ~/.local/share/fonts
    cp ~/roboto-font/* ~/.local/share/fonts/
    
    echo "Cleaning up"
    rm ~/roboto.zip && rm -r ~/roboto-font
    
    echo "Adding HandWriter to PATH"
    cd /usr/local/bin
    sudo ln -s /opt/HandWriter/HandWriter

elif [ "$OS" = "rhel fedora" ]
then
    echo "Installing the HandWriter package"
    sudo rpm -v --import https://fbs.sh/SaurusXI/HandWriter/public-key.gpg
    sudo yum-config-manager --add-repo https://fbs.sh/SaurusXI/HandWriter/rpm/HandWriter.repo
    yes | sudo yum install handwriter
    
    echo "Installing fonts"
    wget $FONTS_FILE -O ~/roboto.zip
    unzip ~/roboto.zip -d ~/roboto-font
    mkdir ~/.local/share/fonts
    cp ~/roboto-font/* ~/.local/share/fonts/
    
    echo "Cleaning up"
    rm ~/roboto.zip && rm -r ~/roboto-font
    
    echo "Adding HandWriter to PATH"
    cd /usr/local/bin
    sudo ln -s /opt/HandWriter/HandWriter

elif [ "$OS" = "debian" ]
then
    echo "Installing the HandWriter package"
    sudo apt-get install apt-transport-https
    wget -qO - https://fbs.sh/SaurusXI/HandWriter/public-key.gpg | sudo apt-key add -
    
    echo 'deb [arch=amd64] https://fbs.sh/SaurusXI/HandWriter/deb stable main' | sudo tee /etc/apt/sources.list.d/handwriter.list
    sudo dpkg-divert --local --divert /opt/HandWriter/libz.so.1.old --rename /opt/HandWriter/libz.so.1
    sudo apt-get update
    yes | sudo apt-get install handwriter
    
    echo "Creating symlink"
    cd /opt/HandWriter/
    sudo ln -s /lib/x86_64-linux-gnu/libz.so.1
    cd
    
    echo "Installing fonts"
    wget $FONTS_FILE -O ~/roboto.zip
    unzip ~/roboto.zip -d ~/roboto-font
    mkdir ~/.local/share/fonts
    cp ~/roboto-font/* ~/.local/share/fonts/
    
    echo "Cleaning up"
    rm ~/roboto.zip && rm -r ~/roboto-font
    
    echo "Adding HandWriter to PATH"
    cd /usr/local/bin
    sudo ln -s /opt/HandWriter/HandWriter
fi