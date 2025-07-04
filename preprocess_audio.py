#!/usr/bin/env python3
"""
Preprocess audio for Gemma-3n
"""

import librosa
import soundfile as sf
import numpy as np
import argparse
import os

def preprocess_audio(input_file, output_file=None, target_sr=16000):
    """
    Preprocess audio for Gemma-3n:
    - Convert to mono
    - Resample to 16kHz
    - Normalize to [-1, 1] range
    - Save as WAV
    """
    print(f"Preprocessing audio: {input_file}")
    
    # Set output file if not specified
    if output_file is None:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_dir = os.path.dirname(input_file)
        output_file = os.path.join(output_dir, f"{base_name}_processed.wav")
    
    # Load audio file
    try:
        # Load with original sample rate
        y, sr = librosa.load(input_file, sr=None, mono=True)
        print(f"Loaded audio: {len(y)/sr:.2f}s, {sr}Hz, {y.dtype}")
        
        # Check if resampling is needed
        if sr != target_sr:
            print(f"Resampling from {sr}Hz to {target_sr}Hz")
            y = librosa.resample(y, orig_sr=sr, target_sr=target_sr)
        
        # Normalize audio to [-1, 1] range if not already
        if np.max(np.abs(y)) > 1.0:
            print("Normalizing audio to [-1, 1] range")
            y = y / np.max(np.abs(y))
        
        # Convert to float32 if not already
        if y.dtype != np.float32:
            print(f"Converting from {y.dtype} to float32")
            y = y.astype(np.float32)
        
        # Save processed audio
        sf.write(output_file, y, target_sr, subtype='FLOAT')
        print(f"Saved processed audio to: {output_file}")
        print(f"Audio properties: {len(y)/target_sr:.2f}s, {target_sr}Hz, {y.dtype}")
        
        # Print audio statistics
        print(f"Audio stats: min={np.min(y):.4f}, max={np.max(y):.4f}, mean={np.mean(y):.4f}, std={np.std(y):.4f}")
        
        return output_file
    
    except Exception as e:
        print(f"Error preprocessing audio: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Preprocess audio for Gemma-3n")
    parser.add_argument("--input", type=str, required=True, help="Input audio file")
    parser.add_argument("--output", type=str, default=None, help="Output audio file")
    parser.add_argument("--sample-rate", type=int, default=16000, help="Target sample rate (default: 16000Hz)")
    args = parser.parse_args()
    
    processed_file = preprocess_audio(args.input, args.output, args.sample_rate)
    
    if processed_file:
        print("\nTo transcribe with Gemma-3n, run:")
        print(f"python gemma_3n_audio_transcription.py --audio {processed_file}")

if __name__ == "__main__":
    main()
