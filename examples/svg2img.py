import cairosvg
import argparse

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i','--input', type=str)
parser.add_argument('-o','--output', type=str, default='output.png')
parser.add_argument('--dpi', type=int, default=600)
args = parser.parse_args()

input_filename = args.input
output_filename = args.output

# Convert SVG to PNG
cairosvg.svg2png(url=input_filename, write_to=output_filename, dpi=args.dpi)


# python3 svg2img.py --i ../log/results/plots/reaction_force.svg --o JointTorqueCommand.png  --dpi 300