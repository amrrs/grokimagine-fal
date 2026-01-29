import asyncio
import os
from pathlib import Path

import fal_client
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


async def generate_and_download_video(
    prompt: str,
    output_dir: str = "videos",
    duration: int = 6,
    aspect_ratio: str = "16:9",
    resolution: str = "480p",
) -> str:
    """
    Generate a video using Grok Imagine and download it.

    Args:
        prompt: Text description of the desired video
        output_dir: Directory to save the downloaded video
        duration: Video duration in seconds (default: 6)
        aspect_ratio: Aspect ratio - 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16
        resolution: Output resolution - 480p or 720p

    Returns:
        Path to the downloaded video file
    """
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print(f"🎬 Generating video with prompt: {prompt}")
    print(f"   Duration: {duration}s | Aspect Ratio: {aspect_ratio} | Resolution: {resolution}")
    print("-" * 60)

    # Submit the request
    handler = await fal_client.submit_async(
        "xai/grok-imagine/text-to-video",
        arguments={
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
        },
    )

    print(f"📤 Request submitted. Request ID: {handler.request_id}")
    print("⏳ Waiting for video generation...")

    # Monitor progress
    async for event in handler.iter_events(with_logs=True):
        if hasattr(event, "message"):
            print(f"   📝 {event.message}")
        elif hasattr(event, "logs"):
            for log in event.logs:
                print(f"   📋 {log.get('message', log)}")

    # Get the result
    result = await handler.get()
    print("-" * 60)
    print("✅ Video generation complete!")

    # Extract video info
    video_info = result.get("video", {})
    video_url = video_info.get("url")
    file_name = video_info.get("file_name", "grok_video.mp4")

    print(f"   📊 Resolution: {video_info.get('width')}x{video_info.get('height')}")
    print(f"   ⏱️  Duration: {video_info.get('duration', 'N/A')}s")
    print(f"   🎞️  FPS: {video_info.get('fps', 'N/A')}")
    print(f"   📹 Frames: {video_info.get('num_frames', 'N/A')}")

    # Download the video
    if video_url:
        output_path = Path(output_dir) / file_name
        print(f"\n📥 Downloading video to: {output_path}")

        response = requests.get(video_url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    progress = (downloaded / total_size) * 100
                    print(f"\r   Progress: {progress:.1f}%", end="", flush=True)

        print(f"\n✅ Video saved to: {output_path}")
        return str(output_path)
    else:
        print("❌ No video URL found in the response")
        return None


def main():
    # Check if API key is set
    if not os.getenv("FAL_KEY"):
        print("❌ Error: FAL_KEY not found in environment variables.")
        print("   Please add your API key to the .env file:")
        print("   FAL_KEY=your_api_key_here")
        return

    # Example usage - customize these parameters
    prompt = input("🎬 Enter your video prompt: ").strip()
    if not prompt:
        prompt = "A cat playing with a ball of yarn in a cozy living room"
        print(f"   Using default prompt: {prompt}")

    # Optional: Get additional parameters
    print("\n📐 Video settings (press Enter for defaults):")

    duration_input = input("   Duration in seconds (6): ").strip()
    duration = int(duration_input) if duration_input else 6

    print("   Aspect ratios: 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16")
    aspect_ratio = input("   Aspect ratio (16:9): ").strip() or "16:9"

    print("   Resolutions: 480p, 720p")
    resolution = input("   Resolution (480p): ").strip() or "480p"

    print()

    # Run the async function
    video_path = asyncio.run(
        generate_and_download_video(
            prompt=prompt,
            duration=duration,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
        )
    )

    if video_path:
        print(f"\n🎉 Done! Your video is ready at: {video_path}")


if __name__ == "__main__":
    main()
