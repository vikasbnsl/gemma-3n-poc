#!/bin/bash

echo "===== Setting up Gemma-3n Audio Transcription ====="

# Install system dependencies for PyAudio and other libraries
echo "Installing system dependencies..."
if command -v brew &> /dev/null; then
    # macOS with Homebrew
    echo "Detected macOS with Homebrew"
    brew install ffmpeg portaudio
    
    # Check for Xcode command line tools (needed for PyAudio)
    if ! xcode-select -p &> /dev/null; then
        echo "Installing Xcode command line tools..."
        xcode-select --install
    fi
elif command -v apt-get &> /dev/null; then
    # Debian/Ubuntu
    echo "Detected Debian/Ubuntu"
    sudo apt-get update
    sudo apt-get install -y ffmpeg portaudio19-dev python3-dev
elif command -v yum &> /dev/null; then
    # RHEL/CentOS/Fedora
    echo "Detected RHEL/CentOS/Fedora"
    sudo yum install -y ffmpeg portaudio-devel
else
    echo "⚠️  Please install ffmpeg and portaudio manually for your system"
fi

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip setuptools wheel

# Install PyAudio first (can be problematic)
echo "Installing PyAudio..."
pip install pyaudio

# Install other dependencies
echo "Installing remaining dependencies..."
pip install -r requirements.txt

# Verify Pillow installation
if ! python -c "import PIL" &> /dev/null; then
    echo "Installing Pillow explicitly..."
    pip install pillow
fi

# Authenticate with Hugging Face (optional)
echo "\nWould you like to authenticate with Hugging Face? (y/n)"
read -r hf_auth
if [[ $hf_auth == "y" || $hf_auth == "Y" ]]; then
    echo "Authenticating with Hugging Face..."
    pip install huggingface_hub
    huggingface-cli login
fi

echo "\n✅ Setup complete! You can now run the Gemma-3n audio processing suite.\n"
echo "Usage:"
echo "  source venv/bin/activate  # Activate virtual environment"
echo "  python record_audio.py  # Record audio"
echo "  python gemma_3n_audio_transcription.py --audio <path>  # Transcribe audio"
echo "  python gemma_meeting_notes.py --transcript <path>  # Generate meeting notes"
