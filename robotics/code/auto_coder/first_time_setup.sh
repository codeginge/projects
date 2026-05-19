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

echo "--> install huggingface-cli"
python3 -m venv myenv
source myenv/bin/activate
pip3 install -U "huggingface_hub[cli]"

echo "--> Installing llama.cpp..."
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j$(nproc)

echo "--> Downloading core language model to '/models' directory"
cd ..
mkdir -p models
hf download ggml-org/Qwen2.5-VL-3B-Instruct-GGUF \
    --include "Qwen2.5-VL-3B-Instruct-Q4_K_M.gguf" \
    --local-dir ./models

hf download ggml-org/Qwen2.5-VL-3B-Instruct-GGUF \
    --include "mmproj-Qwen2.5-VL-3B-Instruct-Q8_0.gguf" \
    --local-dir ./models

