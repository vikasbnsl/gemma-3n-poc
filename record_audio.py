#!/usr/bin/env python3
"""
Audio Recorder for Gemma-3n Audio Processing
Records audio from microphone and saves with timestamp filename
"""

import pyaudio
import wave
import time
import os
import datetime
import argparse
import signal
import sys

class AudioRecorder:
    def __init__(self, output_dir="recordings", format=pyaudio.paInt16, channels=1, 
                 rate=16000, chunk=1024, max_seconds=300):
        """
        Initialize audio recorder with Gemma-3n compatible settings
        
        Args:
            output_dir: Directory to save recordings
            format: Audio format (default: 16-bit int)
            channels: Number of audio channels (default: 1 mono)
            rate: Sample rate (default: 16000Hz for Gemma-3n)
            chunk: Buffer size
            max_seconds: Maximum recording time in seconds
        """
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.max_seconds = max_seconds
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def record(self, duration=None):
        """
        Record audio from microphone
        
        Args:
            duration: Recording duration in seconds (None for manual stop)
        
        Returns:
            Path to saved audio file
        """
        # Set up signal handler for Ctrl+C
        def signal_handler(sig, frame):
            nonlocal recording
            recording = False
            print("\nRecording stopped by user")
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Initialize PyAudio
        audio = pyaudio.PyAudio()
        
        # Open stream
        stream = audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        print("\n=== Recording Started ===\n")
        print("Press Ctrl+C to stop recording...\n")
        
        # Prepare to record
        frames = []
        start_time = time.time()
        recording = True
        
        try:
            # Record until duration, max_seconds, or manual stop
            while recording:
                data = stream.read(self.chunk)
                frames.append(data)
                
                # Check if we should stop recording
                elapsed = time.time() - start_time
                
                # Show recording time
                mins, secs = divmod(int(elapsed), 60)
                print(f"\rRecording: {mins:02d}:{secs:02d}", end="")
                
                # Check for duration limit
                if duration and elapsed >= duration:
                    recording = False
                
                # Check for maximum recording time
                if elapsed >= self.max_seconds:
                    print(f"\nReached maximum recording time ({self.max_seconds} seconds)")
                    recording = False
        
        except Exception as e:
            print(f"\nError during recording: {str(e)}")
        
        print("\n\n=== Recording Finished ===\n")
        
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Save the recording with timestamp
        return self.save_audio(frames)
    
    def save_audio(self, frames):
        """
        Save recorded audio frames to WAV file with timestamp
        
        Args:
            frames: List of audio frames
            
        Returns:
            Path to saved audio file
        """
        # Generate filename with timestamp
        now = datetime.datetime.now()
        timestamp = now.strftime("%M-%H-%Y%m%d")
        filename = f"audio_{timestamp}.wav"
        filepath = os.path.join(self.output_dir, filename)
        
        # Save as WAV file
        wf = wave.open(filepath, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"Audio saved to: {filepath}")
        return filepath

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Record audio for Gemma-3n processing")
    parser.add_argument("-d", "--duration", type=int, default=None, 
                        help="Recording duration in seconds (default: manual stop)")
    parser.add_argument("-o", "--output", type=str, default="test",
                        help="Output directory for recordings")
    parser.add_argument("-r", "--rate", type=int, default=16000,
                        help="Sample rate (default: 16000Hz for Gemma-3n)")
    args = parser.parse_args()
    
    try:
        # Initialize recorder
        recorder = AudioRecorder(
            output_dir=args.output,
            rate=args.rate
        )
        
        # Start recording
        audio_path = recorder.record(duration=args.duration)
        
        print(f"\nRecording complete! File saved to: {audio_path}")
        print("\nTo transcribe with Gemma-3n, run:")
        print(f"python gemma_3n_audio_transcription.py --audio {audio_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
