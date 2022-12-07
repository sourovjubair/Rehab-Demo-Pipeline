import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

ntu_skeleton_bone_pairs = tuple(
    (i - 1, j - 1)
    for (i, j) in (
        (1, 2),
        (2, 21),
        (3, 21),
        (4, 3),
        (5, 21),
        (6, 5),
        (7, 6),
        (8, 7),
        (9, 21),
        (10, 9),
        (11, 10),
        (12, 11),
        (13, 1),
        (14, 13),
        (15, 14),
        (16, 15),
        (17, 1),
        (18, 17),
        (19, 18),
        (20, 19),
        (22, 23),
        (21, 21),
        (23, 8),
        (24, 25),
        (25, 12),
    )
)


def visualize(data_path, indices, normalized=True):
    data = np.load(data_path, mmap_mode="r")
    data = data[:, :, :300, :, :]
    bones = ntu_skeleton_bone_pairs

    def animate(skeleton):
        ax.clear()
        if normalized:
            ax.set_xlim([-1, 1])
            ax.set_ylim([-1, 1])
            ax.set_zlim([-1, 1])
        else:
            ax.set_xlim([-1, 1])
            ax.set_ylim([-1, 1])
            ax.set_zlim([-1, 3])
        for i, j in bones:
            joint_locs = skeleton[:, [i, j]]
            # plot them
            ax.plot(joint_locs[0], joint_locs[1], joint_locs[2], color="blue")
        skeleton_index[0] += 1
        return ax

    for index in indices:
        mpl.rcParams["legend.fontsize"] = 10
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax = fig.add_subplot(1, 1, 1, projection="3d")
        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])
        ax.set_zlim([-1, 1])
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        # get data
        skeletons = data[index]
        # Pick the first body to visualize
        skeleton1 = skeletons[..., 0]  # out (C,T,V)

        skeleton_index = [0]
        skeleton_frames = skeleton1.transpose(1, 0, 2)

        ani = FuncAnimation(fig, animate, skeleton_frames, interval=1)
        plt.show()
        return ani


# anim_out = visualize(
#     data_path="/home/phantomhive/Documents/Code/agency_lab/MS-G3D/data/train_data_joint.npy",
#     indices=[0],
#     normalized=True,
# )
