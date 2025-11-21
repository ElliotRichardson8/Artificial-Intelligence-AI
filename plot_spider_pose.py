import matplotlib.pyplot as plt
import numpy as np

import kinematics

# Declare constants -----------------------------------------------------------

N_LEGS = kinematics.N_LEGS
N_SEGMENTS = kinematics.N_SEGMENTS

LEG_LABELS = ("L1", "L2", "L3", "L4", "R4", "R3", "R2", "R1")
assert len(LEG_LABELS) == N_LEGS

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

    The first leg is L0 (front left), then legs go anticlockwise around the body
    until R0 (front right)
    """
    # "left" is the spider's left, not the observer's left

    # Validate input
    if angles.size != N_LEGS * N_SEGMENTS:
        raise ValueError(
            f"Input angles must be a 1x{len(N_LEGS)*N_SEGMENTS} vector."
            f"({N_SEGMENTS} angles per leg for {N_LEGS} legs.)")

    # Create figure
    fig = plt.figure()
    # Add 3 dimensional axes
    ax = fig.add_subplot(projection="3d")

    for i in range(N_LEGS):
        joints = kinematics.calculate_joint_positions(i, angles[i*3:i*3+3])

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
    
        
    # Create body. Idk how to fill it in
    t = np.linspace(0, 2*np.pi, 100)
    body_x = kinematics.A * np.cos(t)
    body_y = kinematics.B * np.sin(t)
    ax.plot(body_x, body_y, np.zeros(np.size(t)), "k-") # black line

    # Add "head" marker to spider
    ax.plot(kinematics.A + 0.2, 0, 0, "rs") # red dot

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
    plt.show()

plot_spider_pose(np.ones(24))