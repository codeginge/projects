# this is the setup script for students to run on their rpi in a fresh install. This ensures we are runing projects in the same environment. 
apt update && apt upgrade -y
apt install git -y
apt install vim -y
apt install tree
apt install arduino
./install-arduino-cli.sh
arduino-cli lib update-index
arduino-cli lib install "Servo"@1.2.2
apt install -y lazygit
echo "alias lg='lazygit'" >> ~/.bashrc
source ~/.bashrc
