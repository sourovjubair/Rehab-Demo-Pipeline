import sys
from os.path import abspath
from pathlib import Path

sys.path.extend([str(Path(abspath(__file__)).parent.parent)])

from os import sep
from abc import ABC, abstractmethod
from .utils import read_mat_file
import numpy as np
from tqdm import tqdm
import ui.utils.utils_PyKinectV2 as utils


class AbstractDataConverter(ABC):
    """
    The base class
    """

    def __init__(self):
        pass

    @abstractmethod
    def read_data_feed(self, *args, **kwargs):
        pass

    @abstractmethod
    def extract_data(self, *args, **kwargs):
        """
        Takes the data from whatever dataset/feed it is and returns a dictionary
        (the dictionary may contain NaN values for non-existent data fields) for
        each of the data files/feed segment. If there were multiple source files,
        the dictionaries will be returned for each source file in a list. The format
        of the dictionary is as follows:

        {
            filename: name of the source file
            frame_count: total number of frames
            frame_data: [
                {
                    num_subjects: number of subjects in the frame (1 in most cases)
                    subject_id: the subject ID
                    meta_data: {
                        cliped_edges,
                        hand_left_confidence,
                        hand_left_state,
                        hand_right_confidence,
                        hand_right_state,
                        is_resticted,
                        lean_x,
                        lean_y,
                        tracking_state
                    }
                    number_of_joints: 25 # default for kinect data
                    depth_xy: [{ depth_x, depth_y }, {...}, ...], # length = 25
                    color_xy: [{ color_x, color_y }, {...}, ...], # length = 25
                    camera_xyz: [{ camera_x, camera_y, camera_z }, {...},...], # length = 25
                    joint_orientation: [{ w, x, y, z }, {...}, ...] # length = 25
                    tracking_state: [...] # length = 25
                },
                {
                    ...
                },
                ...
            ]
        }
        """
        pass


class LabDataConverter(AbstractDataConverter):
    """
    The converter for the lab kinect data. It expects a list of mat files,
    reads them, converts them to the skeleton format and then returns the
    skeleton format data, which is essentially a bunch of text lines
    """

    def __init__(self, mat_file_paths):
        super().__init__()
        self.mat_file_paths = mat_file_paths

    def read_data_feed(self, *args, **kwargs):
        """
        Reads the mat files and constructs a list of dictionaries containing the path
        and data of each individual mat files, which is kept as an instance variable
        of the class
        """
        self._data = []

        print("Reading files...")

        for mat_file_path in tqdm(self.mat_file_paths):
            try:
                mat_file_data = read_mat_file(mat_file_path)
            except Exception as exception:
                print(exception.args)
                continue
            else:
                self._data.append(
                    {
                        "mat_file_path": mat_file_path,
                        "mat_file_data": mat_file_data,
                    }
                )

    def extract_data(self, *args, **kwargs):
        """
        Extracts the data from self._data (must call read_data_feed() first) to
        a dictionary that conforms to the NTU format, which can be then used to
        generate a .skeleton file.

        The lab kinect data shape is as follows:
        1 x N X F -> N is the number of frames, F is the number of fields
        For each frame, there are F = 15 fields worth of data. Number of fields is
        always constant (15) and is, from left to right 'AbsTime', 'BodyIndexFrame',
        'BodyTrackingID', 'ColorJointIndices', 'DepthJointIndices', 'FrameNumber',
        'HandLeftConfidence', 'HandLeftState', 'HandRightConfidence','HandRightState',
        'IsBodyTracked', 'JointPositions', 'JointTrackingState', 'RelativeFrame',
        'TriggerIndex'. The indexing is 0 through 14.

        'IsBodyTracked' field contains the index information on which index we can
        find the acutal readings for other fields. It is a list like this:
        [0, 0, 0, 1, 0, 0]. This means that the 3rd index is where we should look.

        We mainly need:
        'ColorJointIndices' → Position of the joints on the RGB image
        'DepthJointIndices' → Position of the joints on the depth image
        'BodyTrackingID' → The ID of the subject
        'FrameNumber' → Number of frame
        'JointPositions' → The position of the joints with respect to the kinect
         camera
        """

        if self._data is None or not isinstance(self._data, list):
            raise Exception(
                "Probably read_data_feed was not called. No mat file data"
                " found to read."
            )

        skeleton_data = []

        print("Extracting data...")

        for raw_data_dict in tqdm(self._data):
            raw_data_file_path = raw_data_dict["mat_file_path"]
            raw_data = raw_data_dict["mat_file_data"]

            if raw_data is None:
                print(
                    "Skipping ",
                    raw_data_file_path,
                    " since it has no 'data' keyword",
                )
                continue

            frame_count = raw_data.shape[-1]
            frame_data = []

            for frame_index in range(frame_count):
                track_index_list = raw_data[0][frame_index][10][
                    0
                ]  # index of IsBodyTracked = 10
                track_index = np.where(track_index_list == 1)[0][0]

                subject_id = "{:.0f}".format(
                    raw_data[0][frame_index][2][0][track_index]
                )
                hand_left_confidence = raw_data[0][frame_index][6][0][
                    track_index
                ]
                hand_left_state = raw_data[0][frame_index][7][0][track_index]
                hand_right_confidence = raw_data[0][frame_index][8][0][
                    track_index
                ]
                hand_right_state = raw_data[0][frame_index][9][0][track_index]

                color_xy_data = raw_data[0][frame_index][3]
                color_xy_joint_count = color_xy_data.shape[0]

                depth_xy_data = raw_data[0][frame_index][4]
                depth_xy_joint_count = depth_xy_data.shape[0]

                camera_xyz_data = raw_data[0][frame_index][11]
                camera_xyz_joint_count = camera_xyz_data.shape[0]

                tracking_states_data = raw_data[0][frame_index][12]
                tracking_states_joint_count = tracking_states_data.shape[0]

                if (
                    color_xy_joint_count != 25
                    or camera_xyz_joint_count != 25
                    or depth_xy_joint_count != 25
                    or tracking_states_joint_count != 25
                ):
                    raise Exception("Joint count is not equal to 25")

                color_xy_coordinates = []
                depth_xy_coordinates = []
                camera_xyz_coordinates = []
                tracking_states = []
                joint_orientation_coordinates = []

                # for each of the 25 joints, extract the required data
                for joint_index in range(25):
                    color_x, color_y = (
                        color_xy_data[joint_index][0][track_index],
                        color_xy_data[joint_index][1][track_index],
                    )
                    depth_x, depth_y = (
                        depth_xy_data[joint_index][0][track_index],
                        depth_xy_data[joint_index][1][track_index],
                    )
                    camera_x, camera_y, camera_z = (
                        camera_xyz_data[joint_index][0][track_index],
                        camera_xyz_data[joint_index][1][track_index],
                        camera_xyz_data[joint_index][2][track_index],
                    )
                    tracking_state = tracking_states_data[joint_index][
                        track_index
                    ]

                    color_xy_coordinates.append(
                        {"color_x": color_x, "color_y": color_y}
                    )
                    depth_xy_coordinates.append(
                        {"depth_x": depth_x, "depth_y": depth_y}
                    )
                    camera_xyz_coordinates.append(
                        {
                            "camera_x": camera_x,
                            "camera_y": camera_y,
                            "camera_z": camera_z,
                        }
                    )
                    # in the lab kinect data, there is no joint orientation info
                    joint_orientation_coordinates.append(
                        {"w": np.nan, "x": np.nan, "y": np.nan, "z": np.nan}
                    )
                    tracking_states.append(tracking_state)

                frame_data.append(
                    {
                        "num_subjects": 1,
                        "subject_id": subject_id,
                        "meta_data": {
                            "cliped_edges": np.nan,
                            "hand_left_confidence": hand_left_confidence,
                            "hand_left_state": hand_left_state,
                            "hand_right_confidence": hand_right_confidence,
                            "hand_right_state": hand_right_state,
                            "is_resticted": np.nan,
                            "lean_x": np.nan,
                            "lean_y": np.nan,
                            "tracking_state": np.nan,
                        },
                        "number_of_joints": 25,  # default for kinect data
                        "depth_xy": depth_xy_coordinates,
                        "color_xy": color_xy_coordinates,
                        "camera_xyz": camera_xyz_coordinates,
                        "joint_orientation": joint_orientation_coordinates,
                        "tracking_state": tracking_states,
                    }
                )

            skeleton_data.append(
                {
                    "filename": raw_data_file_path.rsplit(sep, 1)[-1],
                    "frame_count": frame_count,
                    "frame_data": frame_data,
                }
            )

        self.skeleton_data = skeleton_data


class KinectDataConverter(AbstractDataConverter):
    def __init__(
        self,
        kinect,
        color_height,
        color_width,
        depth_height,
        depth_width,
        intrinsic,
        depth_scale,
    ):
        self._kinect = kinect
        self.color_height = color_height
        self.color_width = color_width
        self.depth_height = depth_height
        self.depth_width = depth_width
        self._intrinsic = intrinsic
        self._depth_scale = depth_scale

    def read_data_feed(self, *args, **kwargs):
        """
        Reads each frame data from the kinect's feed and returns a tuple
        """
        frame_data = dict()
        body_frame = self._kinect.get_last_body_frame()
        color_frame = self._kinect.get_last_color_frame()
        depth_frame = self._kinect.get_last_depth_frame()

        color_img = color_frame.reshape(
            ((self.color_height, self.color_width, 4))
        ).astype(np.uint8)
        depth_img = depth_frame.reshape(
            ((self.depth_height, self.depth_width))
        ).astype(np.uint16)

        body_data = dict()

        if body_frame is not None:
            for i in range(0, self._kinect.max_body_count):
                body = body_frame.bodies[i]
                if body.is_tracked:
                    body_data[str(i)] = dict()

                    joints = body.joints
                    joint_orientations = body.joint_orientations
                    joint_points = self._kinect.body_joints_to_depth_space(
                        joints
                    )  # Convert joint coordinates to depth space
                    joints_2D = utils.get_joint2D(joints, joint_points)
                    joints_3D = utils.get_joint3D(
                        joints,
                        joint_points,
                        depth_img,
                        self._intrinsic,
                        self._depth_scale,
                    )  # Convert to numpy array format
                    orientation = utils.get_joint_quaternions(
                        joint_orientations
                    )
                    body_data[str(i)]["joints_2D"] = joints_2D
                    body_data[str(i)]["joints_3D"] = joints_3D
                    body_data[str(i)]["orientation"] = orientation

        frame_data["body_data"] = body_data

        return (color_img, body_frame, frame_data)

    def extract_data(self, frame_data, *args, **kwargs):
        """
        Takes the read frame data of kinect and returns the single frame data in 
        formatted manner (see comment of AbstractDataConverter)
        """
        body_data_for_current_frame = frame_data["body_data"]

        # if there is are no detected bodies on the kinect, this will be an
        # empty dictionary
        if not bool(body_data_for_current_frame):
            return None

        for subject_id, inner_dict in body_data_for_current_frame.items():
            depth_xy = np.array(
                inner_dict["joints_2D"], dtype=np.float16
            )  # depthXY
            camera_xyz = inner_dict["joints_3D"]
            orientation_wxyz = inner_dict["orientation"]

            # use depth xy to upscale to color xy
            color_xy = np.array(
                np.column_stack(
                    (depth_xy[:, 0] * 1920 / 512, depth_xy[:, 1] * 1080 / 424)
                ),
                dtype=np.float16,
            )

            # scale between 0 and 1
            depth_xy[:, 0] /= 512
            depth_xy[:, 1] /= 424
            color_xy[:, 0] /= 1920
            color_xy[:, 1] /= 1080

            color_xy_coordinates = []
            depth_xy_coordinates = []
            camera_xyz_coordinates = []
            tracking_states = [2] * 25  # all joints are tracked = 2 by default
            joint_orientation_coordinates = []

            for joint_index in range(25):
                color_x, color_y = (
                    color_xy[joint_index][0],
                    color_xy[joint_index][1],
                )
                depth_x, depth_y = (
                    depth_xy[joint_index][0],
                    depth_xy[joint_index][1],
                )
                camera_x, camera_y, camera_z = (
                    camera_xyz[joint_index][0],
                    camera_xyz[joint_index][1],
                    camera_xyz[joint_index][2],
                )
                w, x, y, z = (
                    orientation_wxyz[joint_index][0],
                    orientation_wxyz[joint_index][1],
                    orientation_wxyz[joint_index][2],
                    orientation_wxyz[joint_index][3],
                )
                color_xy_coordinates.append(
                    {"color_x": color_x, "color_y": color_y}
                )
                depth_xy_coordinates.append(
                    {"depth_x": depth_x, "depth_y": depth_y}
                )
                camera_xyz_coordinates.append(
                    {
                        "camera_x": camera_x,
                        "camera_y": camera_y,
                        "camera_z": camera_z,
                    }
                )
                joint_orientation_coordinates.append(
                    {"w": w, "x": x, "y": y, "z": z}
                )

            # return only one subject's data
            return {
                "num_subjects": 1,
                "subject_id": subject_id,
                "meta_data": {
                    "cliped_edges": np.nan,
                    "hand_left_confidence": np.nan,
                    "hand_left_state": np.nan,
                    "hand_right_confidence": np.nan,
                    "hand_right_state": np.nan,
                    "is_resticted": np.nan,
                    "lean_x": np.nan,
                    "lean_y": np.nan,
                    "tracking_state": np.nan,
                },
                "number_of_joints": 25,  # default for kinect data
                "depth_xy": depth_xy_coordinates,
                "color_xy": color_xy_coordinates,
                "camera_xyz": camera_xyz_coordinates,
                "joint_orientation": joint_orientation_coordinates,
                "tracking_state": tracking_states,
            }

