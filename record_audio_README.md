# Audio Recorder for Gemma-3n

This tool allows you to record high-quality audio with timestamp filenames, optimized for processing with Gemma-3n.

## Features

- Records audio from your microphone with proper sample rate for Gemma-3n
- Saves files with minute-hour-date format (e.g., `audio_45-14-20250704.wav`)
- Supports both manual and timed recording modes
- Optimized for Gemma-3n with 16kHz sample rate

## Usage

```bash
python record_audio.py [options]
```

### Command-Line Options

- `-d, --duration <seconds>`: Set recording duration (default: manual stop with 'q' key)
- `-o, --output <directory>`: Specify output directory (default: "recordings")
- `-r, --rate <sample_rate>`: Set sample rate (default: 16000Hz for Gemma-3n)

### Example

```bash
# Record until manually stopped
python record_audio.py --output meetings

# Record for 60 seconds
python record_audio.py --duration 60 --output meetings
```

## How It Works

1. **Recording**: Captures audio from your microphone using PyAudio
2. **Timestamp Naming**: Saves files with minute-hour-date format
3. **Gemma-Compatible Format**: Records at 16kHz sample rate optimized for Gemma-3n

## Next Steps

After recording, you can transcribe the audio using the Gemma-3n audio transcription tool:

```bash
python gemma_3n_audio_transcription.py --audio recordings/audio_45-14-20250704.wav
```
