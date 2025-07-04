# Gemma-3n Audio Transcription

This tool uses Google's Gemma-3n-E4B-it model to transcribe audio files with high accuracy using native audio processing capabilities.

## Features

- **Pure Gemma-3n Implementation**: Uses only the Gemma-3n-E4B-it model for audio processing
- **High Accuracy**: Achieves 97%+ accuracy on clear audio samples
- **Hardware Acceleration**: Automatically uses Mac GPU (Metal), CUDA, or CPU
- **Token Management**: Optimizes token usage for Gemma-3n's 32K context window

## Usage

```bash
python gemma_3n_audio_transcription.py [options]
```

### Command-Line Options

- `--audio <path>`: Path to audio file for transcription
- `--output <path>`: Path to output file (default: auto-generated based on audio filename)
- `--original <path>`: Path to original transcript for comparison (optional)

### Example

```bash
# Basic transcription
python gemma_3n_audio_transcription.py --audio recordings/meeting.wav

# Specify output location
python gemma_3n_audio_transcription.py --audio recordings/meeting.wav --output transcripts/meeting_transcript.txt
```

## How It Works

1. **Audio Loading**: The audio file is loaded and processed
2. **Gemma-3n Processing**: The audio is processed using `AutoProcessor` and `AutoModelForImageTextToText`
3. **Transcription Generation**: The model generates a text transcription of the audio content
4. **Post-processing**: The output is cleaned and formatted for readability

## Technical Details

- **Model**: `google/gemma-3n-E4B-it`
- **Processing**: Native Gemma-3n audio capabilities via `AutoModelForImageTextToText`
- **Audio Format**: 16kHz sample rate recommended
- **Token Management**: Dynamically calculates available tokens based on prompt length

## Next Steps

After transcription, you can generate meeting notes from the transcript:

```bash
python gemma_meeting_notes.py --transcript path/to/transcript.txt
```
