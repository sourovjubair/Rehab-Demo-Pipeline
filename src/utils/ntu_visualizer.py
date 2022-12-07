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


def visualize(
    data_path=None, data=None, indices=[0], normalized=True, change_order=False
):
    if data_path is not None:
        data = np.load(data_path, mmap_mode="r")
        data = data[:, :, :300, :, :]
    elif data is None:
        raise Exception(
            "Either path to numpy file or numpy array must be given"
        )

    bones = ntu_skeleton_bone_pairs

    def animate(skeleton):
        ax.clear()
        if normalized:
            ax.set_xlim([-2, 3])
            ax.set_ylim([-2, 3])
            ax.set_zlim([-2, 3])
        else:
            ax.set_xlim([-2, 3])
            ax.set_ylim([-2, 3])
            ax.set_zlim([-2, 3])

        # 0 1 2
        # 0 2 1
        # 1 0 2
        # 1 2 0
        # 2 1 0
        # 2 0 1

        for i, j in bones:
            joint_locs = skeleton[:, [i, j]]

            # apparently, the lab kinect mat files report camera x, camera y and
            # camera z coordinates in x, z, y instead of x, y and z
            if change_order:
                ax.plot(
                    joint_locs[0], joint_locs[2], joint_locs[1], color="blue"
                )
            else:
                ax.plot(
                    joint_locs[0], joint_locs[1], joint_locs[2], color="red"
                )

            # ax.plot(joint_locs[0], joint_locs[1], joint_locs[2], color="blue")
            # ax.plot(joint_locs[0], joint_locs[2], joint_locs[1], color="cyan")
            # ax.plot(
            #     joint_locs[1], joint_locs[0], joint_locs[2], color="yellow"
            # )
            # ax.plot(joint_locs[1], joint_locs[2], joint_locs[0], color="black")
            # ax.plot(joint_locs[2], joint_locs[1], joint_locs[0], color="green")
            # ax.plot(
            #     joint_locs[2], joint_locs[0], joint_locs[1], color="magenta"
            # )

        skeleton_index[0] += 1
        return ax

    for index in indices:
        mpl.rcParams["legend.fontsize"] = 10
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection="3d")
        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])
        ax.set_zlim([-1, 1])
        ax.set_xlabel("x-axis")
        ax.set_ylabel("y-axis")
        ax.set_zlabel("z-axis")

        # get data
        skeletons = data[index]
        # Pick the first body to visualize
        skeleton1 = skeletons[..., 0]  # out (C,T,V)

        skeleton_index = [0]
        skeleton_frames = skeleton1.transpose(1, 0, 2)

        ani = FuncAnimation(fig, animate, skeleton_frames, interval=1)
        plt.show()
        return ani
