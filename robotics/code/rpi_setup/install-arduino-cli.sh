# 1. Create a directory for local binaries if it doesn't exist
mkdir -p ~/.local/bin

# 2. Download and run the install script
# This script will automatically detect the ARMv7 architecture for Legacy OS
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=~/.local/bin sh

# 3. Add the directory to your PATH (if not already there)
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
source ~/.bashrc

# 4. Verify the installation
arduino-cli version

