# Gemma-3n Audio Processing Suite

## Overview

This project provides a complete end-to-end audio processing workflow using Google's Gemma-3n-E4B-it model. The suite includes tools for recording audio, transcribing speech, and generating structured meeting notes - all powered by Gemma-3n's advanced capabilities.

## Tools

This suite consists of three main tools:

1. [**Audio Recorder**](./record_audio_README.md): Record high-quality audio with timestamp filenames
2. [**Audio Transcription**](./transcription_README.md): Convert speech to text with Gemma-3n
3. [**Meeting Notes Generator**](./meeting_notes_README.md): Transform transcripts into structured notes

## Features

- **Audio Recording**: Record high-quality audio with timestamp filenames
- **Pure Gemma-3n Transcription**: Convert speech to text with 97%+ accuracy
- **Meeting Notes Generation**: Transform transcripts into professional meeting notes
- **Mac GPU Acceleration**: Optimized for Apple Silicon with Metal support
- **Command-Line Interface**: Flexible tools with customizable parameters

## Requirements

- Python 3.8+
- FFmpeg
- GPU Support (optional, for faster processing):
  - Apple Silicon Mac with Metal support (M1/M2/M3)
  - OR CUDA-compatible NVIDIA GPU

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd gemma3n-audio
   ```

2. Run the setup script:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   This will:
   - Create a Python virtual environment
   - Install required dependencies
   - Install FFmpeg if not already present

## Usage

Each tool in the suite has its own command-line interface with various options:

### 1. [Record Audio](./record_audio_README.md)

```bash
source venv/bin/activate
python record_audio.py --output meetings
```

### 2. [Transcribe Audio](./transcription_README.md)

```bash
source venv/bin/activate
python gemma_3n_audio_transcription.py --audio path/to/audio.wav
```

### 3. [Generate Meeting Notes](./meeting_notes_README.md)

```bash
source venv/bin/activate
python gemma_meeting_notes.py --transcript path/to/transcript.txt
```

For detailed command-line options and examples, please refer to the individual README files for each tool.

## How It Works

This suite provides a complete end-to-end workflow for audio processing:

1. **[Audio Recording](./record_audio_README.md)**: Record high-quality audio with timestamp filenames using PyAudio

2. **[Audio Transcription](./transcription_README.md)**: Process audio using Gemma-3n's native audio capabilities to generate accurate text transcriptions

3. **[Meeting Notes Generation](./meeting_notes_README.md)**: Transform transcripts into structured, professional meeting notes with Gemma-3n

For detailed information about each component, please refer to the linked README files.

## Technical Details

- **Model**: `google/gemma-3n-E4B-it`
- **Processing**: Native Gemma-3n audio capabilities via `AutoModelForImageTextToText`
- **Hardware Acceleration**:
  - Automatic detection of Mac GPU (Metal Performance Shaders)
  - Fallback to CUDA GPU if available
  - CPU support when no GPU is present
- **Audio Format**: 16kHz sample rate recommended
- **Output**: Clean text transcription with high accuracy

## Complete Workflow Example

Here's how to use the entire suite for a complete end-to-end workflow:

```bash
# 1. Record a meeting (see record_audio_README.md for more options)
python record_audio.py --output meetings
# (Press 'q' to stop recording)

# 2. Transcribe the recording (see transcription_README.md for more options)
python gemma_3n_audio_transcription.py --audio meetings/audio_45-14-20250704.wav

# 3. Generate meeting notes from the transcript (see meeting_notes_README.md for more options)
python gemma_meeting_notes.py --transcript meetings/audio_45-14-20250704_transcription.txt --title "Weekly Team Sync"
```

For detailed information about each tool, refer to the individual README files:
- [Audio Recording Documentation](./record_audio_README.md)
- [Audio Transcription Documentation](./transcription_README.md)
- [Meeting Notes Documentation](./meeting_notes_README.md)

## Sample Results

For the included sample audio file, Gemma-3n produces the following transcription:

```
The stale smell of old beer lingers. It takes heat to bring out the odor. 
A cold dip restores health and zest. A salt pickle tastes fine with ham. 
Tacos al pastor are my favorite. A zesty food is the hot cross bun.
```

And generates these meeting notes:

```markdown
## 1. Meeting Title: Team Discussion Notes

## 2. Summary:
This meeting involved a brief, informal discussion centered around sensory preferences – 
specifically smells, tastes, and textures related to food. The conversation touched on 
contrasts and personal favorites.

## 3. Key Points:
* Discussion focused on sensory experiences related to food (smell, taste).
* Contrasting elements were highlighted (e.g., stale vs. cold beer).
* Personal food preferences were shared (Tacos al pastor, hot cross buns).

## 4. Action Items:
* None explicitly stated. (This was a brief discussion.)

## 5. Next Steps:
* No immediate next steps are required.
```

## Performance

- **Mac GPU Acceleration**: Optimized for Apple Silicon (M1/M2/M3) using Metal Performance Shaders
- **Automatic Hardware Detection**: Selects the best available hardware acceleration
- **Optimized Precision**: Uses float16 on GPU and float32 on CPU for optimal performance

## Limitations

- Best results with clear audio and minimal background noise
- Audio clips of up to 30 seconds are recommended (per Google's documentation)
- Each second of audio costs approximately 6.25 tokens

## References

- [Google AI for Developers - Audio processing with Gemma](https://ai.google.dev/gemma/docs/capabilities/audio)
- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers/index)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
