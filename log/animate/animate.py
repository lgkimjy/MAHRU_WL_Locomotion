import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import matplotlib.animation as animation
import argparse

# Read the data and filter the data
df = pd.read_csv('../data/BodyVelocity.csv')

parser = argparse.ArgumentParser()
parser.add_argument('-i','--initial_t', type=float, default=0.0)
parser.add_argument('-f','--final_t', type=float, default=df['dt'].iloc[-1])
args = parser.parse_args()

filtered_df = df[ (df['dt'] > args.initial_t) & (df['dt'] < args.final_t) ]

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Define the columns to plot and their respective styles
columns = ['commanded[0]', 'measuredCoM[0]', 'measuredBody[0]']
labels = ['$v_{com,x}^*$', '$v_{com,x}$', '$v_{body,x}$']
markers = ['', '.', '.']
linestyles = ['--', '-', '-']
markersizes = [1, 1, 1]

# Set Intervalss-------------------------------------
interval = 10
num_frames = len(filtered_df['dt']) // interval


lines = []
for i, col in enumerate(columns):
    line, = ax.plot(filtered_df['dt'], filtered_df[col], marker=markers[i], linestyle=linestyles[i], markersize=markersizes[i], label=labels[i])
    lines.append(line)

# Setting the axis limits
ax.set_xlim(filtered_df['dt'].min(), filtered_df['dt'].max())
ax.set_ylim(filtered_df[columns].min().min(), filtered_df[columns].max().max())
ax.set_xlabel('dt')
ax.set_ylabel('Value')
ax.set_title('Animated Data from t='+str(args.initial_t)+' to t='+str(args.final_t))
ax.legend(fontsize=15)
ax.grid(True)

# Initialization function
def init():
    for line in lines:
        line.set_data([], [])
    return lines

# Update function for animation
def update(frame):
    for i, line in enumerate(lines):
        line.set_data(filtered_df['dt'][:frame*interval], filtered_df[columns[i]][:frame*interval])     # allows the animation to show the data in increments of 10.
    return lines

# Create the animation
num_frames = len(filtered_df['dt']) // interval
ani = animation.FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True, repeat=False)

plt.tight_layout()
# plt.show()
ani.save('../results/animations/animation.mp4', writer='ffmpeg', fps=1000/interval, dpi=300)