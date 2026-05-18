# exit if any error exists
set -e
echo "==============================================="
echo "Running Setup Script for AUTO CODER for rpi 500"
echo "==============================================="
sudo apt install pv -y

echo "--> Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "--> Installing python3 pip and dependencies..."
sudo apt install python3-pip python3-venv build-essential cmake git wget curl -y

echo "--> Installing llama.cpp..."
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp
cmake -B build -DLLAMA_AVX2=ON -DLLAMA_F16C=ON -DLLAMA_FMA=ON
cmake --build build --config Release --target llama-qwen2vl-cli

mkdir -p models/qwen2.5-vl-3b
cd models/qwen2.5-vl-3b

echo "--> Download the main text model and the vision projector (mmproj)"
wget -O qwen2.5-vl-3b-instruct.gguf https://huggingface.co
wget -O mmproj.gguf https://huggingface.co

echo "--> Setting up python virtual environment..."
python3 -m venv myenv
source myenv/bin/activate

mkdir -p models/qwen2.5-vl-3b

echo "--> Downloading Language Brain (model.gguf)..."
curl -L --progress-bar "https://huggingface.co" -o models/qwen2.5-vl-3b/model.gguf

echo "--> Downloading Vision Matrix (mmproj.gguf)..."
curl -L --progress-bar "https://huggingface.co" -o models/qwen2.5-vl-3b/mmproj.gguf

