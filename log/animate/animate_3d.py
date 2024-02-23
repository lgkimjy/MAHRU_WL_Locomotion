import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# Your CSV data
df = pd.read_csv('../data/EEposition.csv')
filtered_df = df
# filtered_df = df[(df['dt'] >= 0.005) & (df['dt'] <= 0.01)]

df_com = pd.read_csv('../data/CoM.csv')

# Set up the figure
fig = plt.figure(figsize=(10, 6))

# Create a 3D axis
ax = fig.add_subplot(111, projection='3d')
ax.set_box_aspect([2, 1, 1])
elevation_angle = 30  # degrees
azimuth_angle = -67    # degrees
ax.view_init(elev=elevation_angle, azim=azimuth_angle)

# Set Intervalss-------------------------------------
interval = 10
num_frames = len(filtered_df['dt']) // interval

# Create lines for left and right foot
left_line, = ax.plot([], [], [], lw=2, color='blue', label='Left Foot')
right_line, = ax.plot([], [], [], lw=2, color='red', label='Right Foot')
com_line, = ax.plot([], [], [], lw=2, color='green', label='CoM')

connect_left_com, = ax.plot([], [], [], 'o--')  # Dashed line to connect left foot to CoM
connect_right_com, = ax.plot([], [], [], 'o--')  # Dashed line to connect right foot to CoM


x_min = min(filtered_df['left_x'].min(), filtered_df['right_x'].min(), df_com['com_x'].min())
x_max = max(filtered_df['left_x'].max(), filtered_df['right_x'].max(), df_com['com_x'].max())

y_min = min(filtered_df['left_y'].min(), filtered_df['right_y'].min(), df_com['com_y'].min())
y_max = max(filtered_df['left_y'].max(), filtered_df['right_y'].max(), df_com['com_y'].max())

z_min = min(filtered_df['left_z'].min(), filtered_df['right_z'].min(), df_com['com_z'].min())
z_max = max(filtered_df['left_z'].max(), filtered_df['right_z'].max(), df_com['com_z'].max())

ax.set_xlim(x_min-0.3, x_max+0.3)
ax.set_ylim(y_min-0.3, y_max+0.3)
ax.set_zlim(z_min, z_max)

# Setting the axis limits based on the data
# ax.set_xlim(min(filtered_df['left_x'].min(), filtered_df['right_x'].min()), 
#             max(filtered_df['left_x'].max(), filtered_df['right_x'].max()))
# ax.set_ylim(min(filtered_df['left_y'].min(), filtered_df['right_y'].min()), 
#             max(filtered_df['left_y'].max(), filtered_df['right_y'].max()))
# ax.set_zlim(min(filtered_df['left_z'].min(), filtered_df['right_z'].min()), 
#             max(filtered_df['left_z'].max(), filtered_df['right_z'].max()))


# Initialization function for the animation
def init():
    left_line.set_data([], [])
    left_line.set_3d_properties([])
    right_line.set_data([], [])
    right_line.set_3d_properties([])
    com_line.set_data([], [])
    com_line.set_3d_properties([])
    connect_left_com.set_data([], [])
    connect_left_com.set_3d_properties([])
    connect_right_com.set_data([], [])
    connect_right_com.set_3d_properties([])
    return left_line, right_line, com_line, connect_left_com, connect_right_com

# # Update function for the animation with a buffer of 1000 data points
def update(frame):
    start = max(0, frame * interval - NUM)
    end = frame * interval

    left_line.set_data(filtered_df['left_x'][start:end], filtered_df['left_y'][start:end])
    left_line.set_3d_properties(filtered_df['left_z'][start:end])
    
    right_line.set_data(filtered_df['right_x'][start:end], filtered_df['right_y'][start:end])
    right_line.set_3d_properties(filtered_df['right_z'][start:end])
    
    com_line.set_data(df_com['com_x'][start:end], df_com['com_y'][start:end])
    com_line.set_3d_properties(df_com['com_z'][start:end])

    connect_left_com.set_data([filtered_df['left_x'][frame*interval], df_com['com_x'][frame*interval]],
                              [filtered_df['left_y'][frame*interval], df_com['com_y'][frame*interval]])
    connect_left_com.set_3d_properties([filtered_df['left_z'][frame*interval], df_com['com_z'][frame*interval]])
    
    connect_right_com.set_data([filtered_df['right_x'][frame*interval], df_com['com_x'][frame*interval]],
                               [filtered_df['right_y'][frame*interval], df_com['com_y'][frame*interval]])
    connect_right_com.set_3d_properties([filtered_df['right_z'][frame*interval], df_com['com_z'][frame*interval]])
    
    return left_line, right_line, com_line, connect_left_com, connect_right_com

# Create the animation
NUM = 1000  # Number of most recent data points to display (HISTORY)
num_frames = len(filtered_df['dt']) // interval
ani = animation.FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True, repeat=False)

# Display the animation
plt.legend()
plt.tight_layout()

# Save the animation
ani.save('../results/animations/animation3d.mp4', writer='ffmpeg', fps=1000/interval, dpi=300)

