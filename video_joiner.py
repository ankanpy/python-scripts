from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip

def combine_videos_with_white_space(video_path1, video_path2, output_path, resize_width=None, resize_height=None, white_space_width=20):
    # Load videos
    clip1 = VideoFileClip(video_path1)
    clip2 = VideoFileClip(video_path2)

    # Resize clips if dimensions are provided
    if resize_width and resize_height:
        clip1 = clip1.resize(newsize=(resize_width, resize_height))
        clip2 = clip2.resize(newsize=(resize_width, resize_height))

    # Create a white space color clip
    white_clip = ColorClip(size=(white_space_width, resize_height), color=(255, 255, 255))

    # Calculate total width for the canvas: width of both clips plus white space
    total_width = clip1.size[0] + clip2.size[0] + white_space_width
    max_height = max(clip1.size[1], clip2.size[1])

    # Create a white background clip
    background_clip = ColorClip(size=(total_width, max_height), color=(255, 255, 255))

    # Set the position of each clip on the background
    clip1 = clip1.set_position("left")
    white_clip = white_clip.set_position((clip1.size[0], 0))
    clip2 = clip2.set_position((clip1.size[0] + white_space_width, 0))

    # Create the composite video
    final_clip = CompositeVideoClip([background_clip, clip1, white_clip, clip2], size=(total_width, max_height))

    # Set the duration to the shortest of the two clips
    final_duration = min(clip1.duration, clip2.duration)
    final_clip = final_clip.set_duration(final_duration)

    # Write the output video file
    final_clip.write_videofile(output_path, fps=min(clip1.fps, clip2.fps), codec='libx264')

# Example usage
combine_videos_with_white_space(
    video_path1='/home/ankan_opencv/officework/Jupyter_lab/exp_yoloc/market-india.mp4',
    video_path2='/home/ankan_opencv/officework/Jupyter_lab/predict-yolom/market-india.avi',
    output_path='output.mp4',
    resize_width=640,  # Set your desired width
    resize_height=360,  # Set your desired height
    white_space_width=10  # Set your desired white space width
)