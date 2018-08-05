#!/usr/bin/bash
#This script sets up a selenium scraping server on an AWS EC2 instance (Ubuntu 16.04)
#also includes some basic instructions for starting the controller

# udpate apt and install pip for python3
sudo apt-get update
sudo apt-get install python3-pip

#install selenium
sudo python3 -m pip install -U selenium

#install FireFox and configure gecko driver
sudo apt-get install firefox
wget https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-linux64.tar.gz
tar -xvf geckodriver-v0.21.0-linux64.tar.gz
rm geckodriver-v0.21.0-linux64.tar.gz
chmod +x geckodriver
#note: need to add to ~/.bashrc to make permanent
export PATH=$PATH:~/

#install mysql client
sudo apt-get install mysql-client

#install mysql connector
pip3 install mysql-connector


#----------USEFUL COMMANDS---------------------------------------------------------------------#
#ftp a directory to your EC2 instance (recursively)
#scp -r -i $PATH/TO/yourKey.pem $/PATH/TO/directory/to/copy/* ubuntu@$yourAwsServer:/home/ubuntu

#connect to mysql on RDS
# mysql -u $username -h $hostname -p

#Run controller.py in background continuously
#chmod +x controller.py
#nohup controller.py &

#shutdown controller running in background
#ps ax | grep controller.py
# ^^^use above command to get PID, then use PID in below command
#sudo kill -9 PID



