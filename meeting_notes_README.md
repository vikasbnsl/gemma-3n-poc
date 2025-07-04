# Gemma-3n Meeting Notes Generator

This tool transforms audio transcripts into structured, professional meeting notes using Gemma-3n's advanced text generation capabilities.

## Features

- **Structured Format**: Creates professional meeting notes with clear sections
- **Content Organization**: Formats into Title, Summary, Key Points, Action Items, and Next Steps
- **Markdown Formatting**: Outputs clean, well-formatted markdown for easy reading
- **Hardware Acceleration**: Automatically uses Mac GPU (Metal), CUDA, or CPU

## Usage

```bash
python gemma_meeting_notes.py [options]
```

### Command-Line Options

- `--transcript <path>`: Path to transcript file
- `--output <path>`: Path to output file (default: auto-generated based on transcript filename)
- `--title <string>`: Title for the meeting notes (default: "Team Discussion Notes")

### Example

```bash
# Basic usage
python gemma_meeting_notes.py --transcript transcripts/meeting_transcript.txt

# Custom title and output location
python gemma_meeting_notes.py --transcript transcripts/meeting_transcript.txt --title "Weekly Team Sync" --output notes/weekly_sync_notes.md
```

## How It Works

1. **Transcript Analysis**: Gemma-3n analyzes the transcript content
2. **Structured Generation**: Creates professional meeting notes with sections
3. **Content Organization**: Formats into Title, Summary, Key Points, Action Items, and Next Steps
4. **Markdown Formatting**: Outputs clean, well-formatted markdown for easy reading

## Technical Details

- **Model**: `google/gemma-3n-E4B-it`
- **Processing**: Uses Gemma-3n's text generation capabilities
- **Token Management**: Dynamically calculates available tokens based on prompt length
- **Output Format**: Clean markdown with structured sections

## Sample Output

```markdown
## 1. Meeting Title: Team Discussion Notes

## 2. Summary:
This meeting involved a brief, informal discussion centered around sensory preferences – 
specifically smells, tastes, and textures related to food.

## 3. Key Points:
* Discussion focused on sensory experiences related to food (smell, taste).
* Contrasting elements were highlighted (e.g., stale vs. cold beer).
* Personal food preferences were shared (Tacos al pastor, hot cross buns).

## 4. Action Items:
* None explicitly stated. (This was a brief discussion.)

## 5. Next Steps:
* No immediate next steps are required.
```
