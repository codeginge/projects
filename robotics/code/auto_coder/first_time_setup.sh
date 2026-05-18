# exit if any error exists
set -e
echo "==============================================="
echo "Running Setup Script for AUTO CODER for rpi 500"
echo "==============================================="
sudo apt install pv -y

echo "--> Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "--> Installing python3 pip and dependencies..."
sudo apt install python3-pip python3-venv git curl -y

echo "--> Setting up python virtual environment..."
python3 -m venv myenv
source myenv/bin/activate

echo "--> Checking if Ollama is installed..."
if ! command -v ollama &> /dev/null; then
    echo "--> Ollama is not installed..."
    echo "--> Installing Ollama and OpenCV libraries..."
    pip install --upgrade pip
    pip install ollama opencv-python
    
    echo "--> Installing Ollama system service..."
    curl -L "https://ollama.com/download/ollama-linux-arm64.tar.zst" | pv | sudo tar x --zstd -C /usr
    sudo chmod +x /usr/bin/ollama
else 
    echo "--> Ollama is already installed..."
fi

echo "--> Activating and starting ollama background engine"
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama

echo "--> Waiting for Ollama service to start..."
sleep 5

echo "--> Pulling Ollama Qwen2.5-VL 3B model"
/usr/bin/ollama pull qwen2.5vl:3b


