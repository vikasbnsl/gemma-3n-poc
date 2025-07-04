#!/bin/bash

echo "===== Setting up Gemma-3n Audio Transcription ====="

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install ffmpeg (required for audio processing)
echo "Installing ffmpeg..."
if command -v brew &> /dev/null; then
    brew install ffmpeg
elif command -v apt-get &> /dev/null; then
    sudo apt-get update && sudo apt-get install -y ffmpeg
elif command -v yum &> /dev/null; then
    sudo yum install -y ffmpeg
else
    echo "⚠️  Please install ffmpeg manually for your system"
fi

echo "\n✅ Setup complete! You can now run the transcription.\n"
echo "Usage:"
echo "  source venv/bin/activate  # Activate virtual environment"
echo "  python gemma_3n_audio_transcription.py  # Run Gemma-3n audio transcription"
