# Grok Imagine - Text to Video

Generate videos from text prompts using xAI's Grok Imagine model via fal.ai.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your fal.ai API key:
```
FAL_KEY=your_api_key_here
```

## Usage

```bash
python grok_video.py
```

You'll be prompted to enter:
- **Prompt**: Text description of the video you want to generate
- **Duration**: Video length in seconds (default: 6)
- **Aspect ratio**: 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, or 9:16
- **Resolution**: 480p or 720p

Generated videos are saved to the `videos/` folder.

## Example

```
🎬 Enter your video prompt: A cat playing with a ball of yarn in a cozy living room
```
