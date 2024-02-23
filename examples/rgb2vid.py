import subprocess

# Input and output filenames
input_filename = '../build/depth.out'
# input_filename = '../build/rgb.out'
output_filename = 'output2.mp4'

# Video dimensions (replace with actual dimensions)
width = 1080
height = 886

# Frame rate
fps = 60

# Define ffmpeg command
ffmpeg_command = [
    'ffmpeg',
    '-f', 'rawvideo',
    # '-vcodec', 'rawvideo',
    '-pixel_format', 'rgb24',
    '-video_size', '{}x{}'.format(width, height),
    '-framerate', str(fps),
    '-i', input_filename,
    # '-c:v', 'libx264',
    '-vf', 'vflip,format=yuv420p',
    output_filename
]

# Execute ffmpeg command
subprocess.run(ffmpeg_command)
