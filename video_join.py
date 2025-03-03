import os
from pathlib import Path
from moviepy import VideoFileClip, CompositeVideoClip


def combine_videos_from_directories(
    dir1: str, dir2: str, output_dir: str, gap: int = 50, bg_color: tuple = (255, 255, 255)
):
    """
    Combines videos from two directories side-by-side and saves each pair
    as a new video in the output directory.

    :param dir1: Path to the first directory of videos.
    :param dir2: Path to the second directory of videos.
    :param output_dir: Path to the directory where output videos will be saved.
    :param gap: The pixel gap between the two side-by-side videos.
    :param bg_color: The background color (R, G, B) used to fill the gap.
    """

    # Convert to Path objects (for convenience)
    dir1 = Path(dir1)
    dir2 = Path(dir2)
    output_dir = Path(output_dir)

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Gather and sort video files from both directories
    # (adjust extensions if needed)
    valid_extensions = (".mp4", ".avi", ".mov", ".mkv")
    files1 = sorted([f for f in dir1.iterdir() if f.suffix.lower() in valid_extensions])
    files2 = sorted([f for f in dir2.iterdir() if f.suffix.lower() in valid_extensions])

    # Pair up the videos; only combine up to the smallest list length
    num_pairs = min(len(files1), len(files2))
    print(f"Found {len(files1)} files in {dir1}, {len(files2)} files in {dir2}.")
    print(f"Combining {num_pairs} pairs of videos...")

    for i, (file1, file2) in enumerate(zip(files1, files2), start=1):
        print(f"Processing pair {i}:")
        print(f"  {file1.name} + {file2.name}")

        # Load the two video clips
        clip1 = VideoFileClip(str(file1))
        clip2 = VideoFileClip(str(file2))

        # OPTIONAL: resize second clip to match first clip's height
        # (Useful if you want them aligned vertically)
        clip2 = clip2.resized(height=clip1.h)

        # Calculate final video size
        final_width = clip1.w + gap + clip2.w
        final_height = max(clip1.h, clip2.h)

        # Position second clip to the right of the first clip, separated by gap
        clip2_positioned = clip2.with_position((clip1.w + gap, 0))

        # Create the composite
        final_clip = CompositeVideoClip([clip1, clip2_positioned], size=(final_width, final_height), bg_color=bg_color)

        # Build an output filename. You can customize this however you like.
        output_filename = f"{file1.stem}__{file2.stem}_combined.mp4"
        output_path = output_dir / output_filename

        # Write the output video
        final_clip.write_videofile(
            str(output_path), codec="libx264", audio_codec="aac"  # or "libmp3lame" depending on your setup
        )

        # Close the clips to release resources
        clip1.close()
        clip2.close()
        final_clip.close()

    print("All pairs have been processed!")


if __name__ == "__main__":
    # Example usage:
    combine_videos_from_directories(
        dir1="./retinanet_inference",
        dir2="./yolo_inference",
        output_dir="./combined_videos",
        gap=50,
        bg_color=(255, 255, 255),
    )
