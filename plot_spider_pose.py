import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import forward_kinematics

# Declare constants -----------------------------------------------------------

N_LEGS = 8

# [coxa, femur, tibia]
SEGMENT_LENGTHS = np.array([1.2, 0.7, 1.0])
N_SEGMENTS = len(SEGMENT_LENGTHS)

# Ellipse dimensions for body
A = 1.5
B = 1.0

BASE_ANGLES = np.deg2rad([45, 75, 105, 135, -135, -105, -75, -45])
LEG_LABELS = ("L1", "L2", "L3", "L4", "R4", "R3", "R2", "R1")
frames = []
leg_frames = []
fig = plt.figure()


# Main function ---------------------------------------------------------------
def plot_spider_pose(angles):
    """Plot a static 3D spider pose based on joint angles

    Input:
        angles: 1x24 vector of joint angles in radians

    There are 8 legs with 3 angles each. 
    The segments of the leg are coxa, femur, tibia 
    The 3 angles of each leg correspond roughly to these three segments
    Angle 1 is the yaw (rotation about vertical axis) of the coxa
    Angle 2 is the pitch of the femur
    Angle 3 is the pitch of the tibia

    The first leg is L1 (front left), then legs go anticlockwise around the body
    until R1 (front right)
    """
    # "left" is the spider's left, not the observer's left

    # Validate input
    if angles.size != N_LEGS * N_SEGMENTS:
        print("angles.size", angles.size, "\nangles:", angles)
        raise ValueError(
            f"Input angles must be a 1x{N_LEGS*N_SEGMENTS} vector."
            f"({N_SEGMENTS} angles per leg for {N_LEGS} legs.)")

    # Add 3 dimensional axes
    ax = fig.add_subplot(projection="3d")

    for i in range(N_LEGS):

        # "angles" is 24x1. We need to extract 3 angles at a time
        idx = i*3
        theta1 = angles[idx]
        theta2 = angles[idx+1]
        theta3 = angles[idx+2]

        base_angle = BASE_ANGLES[i]
        x_base = A * np.cos(base_angle)
        y_base = B * np.sin(base_angle)
        base_pos = np.array([x_base, y_base, 0])

        joints = forward_kinematics.calculate_joint_positions(
            base_pos,
            base_angle,
            (theta1, theta2, theta3),
            SEGMENT_LENGTHS
        )

        # Plot legs -----------------------------------------------------------

        # Separate out the different joint coordinates into 3 lists
        # Corresponding to the x, y, z coordinates of the joints
        jx, jy, jz = zip(*joints)

        # Python list slicing is right-exclusive so we need the right index
        # to be 1 greater than what we actually want to include
        ax.plot(jx[0:2], jy[0:2], jz[0:2], "k-") # coxa; black line
        ax.plot(jx[1:3], jy[1:3], jz[1:3], "b-") # femur; blue line
        ax.plot(jx[2:], jy[2:], jz[2:], "r-") # tibia; red line
        ax.plot(jx[3], jy[3], jz[3], "ro", markersize=5) # foot; red circle

        # Plot leg labels ---------

        ax.text(jx[0], jy[0], jz[0], LEG_LABELS[i], fontweight="bold")

        leg_frames.append(ax)
    
        
    # Create body. Idk how to fill it in
    t = np.linspace(0, 2*np.pi, 100)
    body_x = A * np.cos(t)
    body_y = B * np.sin(t)
    ax.plot(body_x, body_y, np.zeros(np.size(t)), "k-") # black line

    # Add "head" marker to spider
    ax.plot(A + 0.2, 0, 0, "rs") # red dot

    # Add axis labels
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    # Set axis bounds
    ax.set_xbound(-4, 4)
    ax.set_ybound(-4, 4)
    ax.set_zbound(-2, 2)
    # Set camera position
    ax.view_init(45, -45)

    ax.set_aspect("equal")
    frames.append(ax)

    plt.show()

def update(frames):
        ax.cla()  # Clear the axes
        for frame in frames:
            ax = frame.gca(projection='3d')
            for line in ax.get_lines():
                ax.add_line(line)   

def show_spider_animation():
    """Displays an animation of the spider moving through the recorded frames."""
    from matplotlib.animation import FuncAnimation

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=200)
    plt.show()
