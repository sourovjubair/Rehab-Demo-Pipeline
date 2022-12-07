import sys

sys.path.extend(["../"])

from utils.skeleton_to_numpy import SkeletonToNumpy
from utils.ntu_visualizer import visualize
import numpy as np

skeleton_file_path = r"C:\Users\Phantomhive\Documents\Code\AGenCy_Labs\kinect_2_ntu_pipeline\output_skeleton_files\2018-10-14-02-24-09.skeleton"

skel2numpy = SkeletonToNumpy()
numpy_arr = skel2numpy.skeleton_to_numpy(skeleton_file_path, max_body=1)
numpy_arr = np.expand_dims(numpy_arr, axis=0)
print(numpy_arr.shape)

anim = visualize(data=numpy_arr, indices=[0], normalized=False)

# anim = visualize(
#     data_path="/home/phantomhive/Documents/Code/agency_lab/kinect_2_ntu_pipeline/data/kimore/data_joint.npy",
#     indices=[0],
#     normalized=False,
# )
