#!/usr/bin/env python3
"""
Gemma-3n Meeting Notes Generator
Converts transcription to structured meeting notes using Gemma-3n
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import warnings
warnings.filterwarnings("ignore")

class GemmaMeetingNotesGenerator:
    def __init__(self, model_id="google/gemma-3n-E4B-it"):
        """
        Initialize Gemma-3n for meeting notes generation
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
        
        print(f"Loading {self.model_id} for meeting notes generation...")
        
        # Set torch dtype based on device
        if self.device.type == "mps":
            torch_dtype = torch.float16  # Use float16 for MPS
        elif self.device.type == "cuda":
            torch_dtype = torch.float16  # Use float16 for CUDA
        else:
            torch_dtype = torch.float32  # Use float32 for CPU
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            torch_dtype=torch_dtype,
            device_map="auto"
        )
        
        print("Model loaded successfully!")
    
    def generate_meeting_notes(self, transcript, output_path=None, meeting_title="Team Meeting"):
        """
        Generate structured meeting notes from transcript
        """
        print(f"Generating meeting notes from transcript...")
        
        # Create a prompt template using the chat format
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"""I have a transcript from a meeting and I need you to convert it into structured meeting notes.

Transcript:
"{transcript}"

Please create professional meeting notes with the following sections:
1. Meeting Title: {meeting_title}
2. Summary: A brief 2-3 sentence overview of what was discussed
3. Key Points: Bullet points of the main topics and decisions
4. Action Items: Any tasks or follow-ups mentioned
5. Next Steps: What happens next based on this meeting

Format the notes professionally and make them concise and clear."""}
                ]
            }
        ]
        
        # Apply chat template
        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.device)
        
        # Generate meeting notes
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_new_tokens=1024,
                temperature=0.2,  # Lower temperature for more focused output
                do_sample=True,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode the generated text
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract the meeting notes (remove the prompt)
        meeting_notes = self.extract_response(generated_text)
        
        # Save to file if specified
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(meeting_notes)
            print(f"Meeting notes saved to: {output_path}")
        
        return meeting_notes
    
    def extract_response(self, full_text):
        """
        Extract the model's response from the full generated text
        """
        # Look for the assistant's response in the chat format
        if "<start_of_turn>model" in full_text:
            response = full_text.split("<start_of_turn>model")[-1].strip()
            # Remove any trailing tokens
            response = response.split("<end_of_turn>")[0].strip()
            
            # Clean up the response to remove the prompt repetition
            if response.startswith("Okay") and "---" in response:
                # Find the first markdown section separator
                parts = response.split("---", 1)
                if len(parts) > 1:
                    # Return everything from the first markdown separator onwards
                    return "---" + parts[1]
            
            return response
        
        # Look for markdown headings that indicate the start of meeting notes
        if "## " in full_text:
            # Find the first markdown heading
            parts = full_text.split("## ", 1)
            if len(parts) > 1:
                return "## " + parts[1]
        
        # Look for numbered sections
        if "## 1. Meeting Title:" in full_text:
            parts = full_text.split("## 1. Meeting Title:", 1)
            if len(parts) > 1:
                return "## 1. Meeting Title:" + parts[1]
        
        # Clean up any remaining prompt instructions
        lines = full_text.split('\n')
        clean_lines = []
        capture = False
        
        for line in lines:
            # Skip lines that are clearly part of the prompt
            if any(x in line.lower() for x in ["format the notes", "please create", "i have a transcript"]):
                continue
                
            # Start capturing after we see model or markdown indicators
            if "model" in line or line.startswith("##") or line.startswith("---"):
                capture = True
                
            if capture and not line.startswith("1. Meeting Title:") and not line.startswith("2. Summary:"):
                clean_lines.append(line)
        
        if clean_lines:
            # Find the first meaningful content
            for i, line in enumerate(clean_lines):
                if line.startswith("##") or line.startswith("---"):
                    return '\n'.join(clean_lines[i:])
            
            # If no clear structure markers found, return all captured lines
            return '\n'.join(clean_lines)
        
        # Fallback: return the last 70% of the text
        split_point = int(len(full_text) * 0.3)
        return full_text[split_point:].strip()

def main():
    # File paths
    transcript_file = "/Users/vikas.bansal/Documents/personal-github/gemma3n-audio/gemma_3n_transcription.txt"
    output_file = "/Users/vikas.bansal/Documents/personal-github/gemma3n-audio/meeting_notes.md"
    
    # Check if transcript file exists
    if not os.path.exists(transcript_file):
        print(f"Error: Transcript file not found at {transcript_file}")
        return
    
    # Read transcript
    with open(transcript_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # Extract just the transcription part
        if "TRANSCRIPTION:" in content:
            transcript = content.split("TRANSCRIPTION:")[1].split("===")[0].strip()
        else:
            transcript = content.strip()
    
    print(f"Loaded transcript: {len(transcript)} characters")
    
    try:
        # Initialize meeting notes generator
        generator = GemmaMeetingNotesGenerator()
        
        # Generate meeting notes
        notes = generator.generate_meeting_notes(
            transcript, 
            output_file,
            meeting_title="Team Discussion Notes"
        )
        
        print("\n" + "="*60)
        print("MEETING NOTES GENERATED:")
        print("="*60)
        print(notes)
        print("="*60)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
