#!/usr/bin/env python3
"""
Gemma-3n Audio Transcription
Official implementation using AutoModelForImageTextToText and AutoProcessor
Based on Google AI for Developers documentation
"""

import torch
from transformers import AutoProcessor, AutoModelForImageTextToText
import os
import warnings
warnings.filterwarnings("ignore")

class Gemma3nAudioTranscriber:
    def __init__(self, model_id="google/gemma-3n-E4B-it"):
        """
        Initialize Gemma-3n with native audio processing capabilities
        """
        self.model_id = model_id
        
        # Check for available devices with Mac GPU (MPS) support
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
            print(f"Using Mac GPU (MPS) device")
        elif torch.cuda.is_available():
            self.device = torch.device("cuda")
            print(f"Using CUDA GPU device")
        else:
            self.device = torch.device("cpu")
            print(f"Using CPU device")
        
        print("Loading Gemma-3n with audio processing capabilities...")
        
        # Set torch dtype based on device
        if self.device.type == "mps":
            torch_dtype = torch.float16  # Use float16 for MPS
        elif self.device.type == "cuda":
            torch_dtype = torch.float16  # Use float16 for CUDA
        else:
            torch_dtype = torch.float32  # Use float32 for CPU
        
        # Load processor and model as per documentation
        self.processor = AutoProcessor.from_pretrained(
            self.model_id, 
            device_map="auto"
        )
        
        self.model = AutoModelForImageTextToText.from_pretrained(
            self.model_id, 
            torch_dtype=torch_dtype, 
            device_map="auto"
        )
        
        print("Gemma-3n model loaded successfully!")
    
    def transcribe_audio(self, audio_path, output_path=None):
        """
        Transcribe audio using Gemma-3n native audio processing
        """
        print(f"Transcribing audio: {audio_path}")
        
        try:
            # Create messages following the documentation format
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "audio", "audio": audio_path},
                        {"type": "text", "text": "Transcribe this audio file accurately. Provide only the spoken text."},
                    ]
                }
            ]
            
            print("Processing audio with Gemma-3n...")
            
            # Apply chat template and tokenize
            input_ids = self.processor.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True, 
                return_dict=True,
                return_tensors="pt",
            )
            
            # Move to device
            input_ids = input_ids.to(self.model.device, dtype=self.model.dtype)
            
            print("Generating transcription...")
            
            # Generate transcription
            with torch.no_grad():
                # Maximum total token length allowed (prompt + output)
                max_length = 32768  # Gemma-3n limit
                
                # Estimate how many tokens the prompt is taking
                prompt_tokens = input_ids['input_ids'].shape[-1]  # Already tokenized prompt
                max_new_tokens = max_length - prompt_tokens  # Use full remaining token capacity
                
                print(f"Prompt tokens: {prompt_tokens}, Available for generation: {max_new_tokens}")
                
                outputs = self.model.generate(
                    **input_ids, 
                    max_new_tokens=max_new_tokens,
                    temperature=0.1,  # Low temperature for accuracy
                    do_sample=True,
                    pad_token_id=self.processor.tokenizer.eos_token_id
                )
            
            # Decode output
            transcription = self.processor.batch_decode(
                outputs,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )
            
            # Extract the actual transcription
            result_text = transcription[0] if transcription else ""
            cleaned_transcription = self.extract_transcription(result_text)
            
            # Create detailed output
            output_content = f"""=== GEMMA-3N AUDIO TRANSCRIPTION ===

Audio File: {os.path.basename(audio_path)}
Model: {self.model_id}
Processing Method: Native Gemma-3n Audio Processing

TRANSCRIPTION:
{cleaned_transcription}

=== TECHNICAL DETAILS ===
Device: {self.device}
Audio Processing: Native Gemma-3n AutoModelForImageTextToText
Processor: AutoProcessor with audio support
Max Tokens: 512
Temperature: 0.1 (for accuracy)
"""
            
            # Save to file if specified
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(output_content)
                print(f"Results saved to: {output_path}")
            
            return cleaned_transcription
            
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            return None
    
    def extract_transcription(self, full_text):
        """
        Extract clean transcription from model output
        """
        # Look for the actual transcription in the response
        lines = full_text.split('\n')
        
        # Find lines that look like transcription content
        transcription_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('<') and not line.startswith('[') and len(line) > 10:
                # Skip system messages and prompts
                if not any(keyword in line.lower() for keyword in ['transcribe', 'audio', 'file', 'user', 'assistant']):
                    transcription_lines.append(line)
        
        if transcription_lines:
            return ' '.join(transcription_lines)
        
        # Fallback: return the full text cleaned up
        cleaned = full_text.replace('<|start_header_id|>', '').replace('<|end_header_id|>', '')
        cleaned = cleaned.replace('<|eot_id|>', '').strip()
        
        return cleaned if cleaned else "Unable to extract transcription"

def main():
    """
    Main function to run Gemma-3n audio transcription
    """
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Transcribe audio using Gemma-3n")
    parser.add_argument("--audio", type=str, default="/Users/vikas.bansal/Documents/personal-github/gemma3n-audio/test/Male Audio Sample.wav",
                        help="Path to audio file for transcription")
    parser.add_argument("--output", type=str, default=None,
                        help="Path to output file (default: gemma_3n_transcription.txt in same directory as audio)")
    parser.add_argument("--original", type=str, default="/Users/vikas.bansal/Documents/personal-github/gemma3n-audio/test/origal-transcript.txt",
                        help="Path to original transcript for comparison (optional)")
    args = parser.parse_args()
    
    # File paths
    audio_file = args.audio
    
    # Set default output file if not specified
    if args.output is None:
        audio_dir = os.path.dirname(audio_file)
        audio_name = os.path.splitext(os.path.basename(audio_file))[0]
        output_file = os.path.join(audio_dir, f"{audio_name}_transcription.txt")
    else:
        output_file = args.output
        
    original_transcript_file = args.original
    
    # Check if files exist
    if not os.path.exists(audio_file):
        print(f"Error: Audio file not found at {audio_file}")
        return
    
    # Load original transcript for comparison
    original_transcript = ""
    if os.path.exists(original_transcript_file):
        with open(original_transcript_file, 'r', encoding='utf-8') as f:
            original_transcript = f.read().strip()
        print("Original transcript loaded for comparison")
    
    try:
        # Initialize transcriber
        transcriber = Gemma3nAudioTranscriber()
        
        # Transcribe audio
        result = transcriber.transcribe_audio(audio_file, output_file)
        
        if result:
            print("\n" + "="*60)
            print("GEMMA-3N TRANSCRIPTION RESULT:")
            print("="*60)
            print(result)
            print("="*60)
            
            # Compare with original if available
            if original_transcript:
                print("\nORIGINAL TRANSCRIPT (for comparison):")
                print("-" * 40)
                print(original_transcript)
                print("-" * 40)
                
                # Simple accuracy check
                original_words = set(original_transcript.lower().split())
                result_words = set(result.lower().split())
                common_words = original_words.intersection(result_words)
                
                if original_words:
                    accuracy = len(common_words) / len(original_words) * 100
                    print(f"\nWord overlap with original: {accuracy:.1f}%")
        else:
            print("Transcription failed!")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure you have the latest transformers library")
        print("2. Ensure the Gemma-3n model supports audio processing")
        print("3. Check your internet connection for model download")

if __name__ == "__main__":
    main()
