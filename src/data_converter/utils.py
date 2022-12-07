import os
import re
import scipy.io
from pathlib import Path
from tqdm import tqdm
import numpy as np


def get_project_root():
    return Path(__file__).parent.parent.parent


def read_mat_file(mat_file_path: str):
    """
    Read a mat file (v5.0) and returns its data contents.

    Note: The lab's kinect data uses v5.0. If the version changes, a different
    approach will be needed to parse the mat files.

    mat_file_path - The path to the mat file. Skips the file if there is no 'data'
    key in the file and returns None

    Returns:
    ========
    The contents of the mat file under the 'data' key or None if 'data' key does
    not exist

    Raises:
    =======
    Exception - if the version of the mat file is not v5.0
    ValueError - if the mat_file_path argument is not a mat file
    FileNotFoundError - if the given path does not exist
    """
    if not mat_file_path.endswith(".mat"):
        raise ValueError("Not a mat file: ", mat_file_path)

    if not os.path.exists(mat_file_path):
        raise FileNotFoundError(
            "The given path ", mat_file_path, " does not exist"
        )

    mat_file = scipy.io.loadmat(mat_file_path)

    # check version number
    header = mat_file["__header__"].decode("utf-8")
    pattern = r"MATLAB (\d+\.\d+) *"
    match_obj = re.match(pattern, header)
    if match_obj:
        groups = match_obj.groups()
        version_number = groups[0]

        if version_number != "5.0":
            raise Exception(
                "The mat file ",
                mat_file_path,
                " is not version 5.0. It cannot be read",
            )
    else:
        raise Exception(
            "The mat file version could not be found for: ", mat_file_path
        )
 
    if "data" not in mat_file.keys():
        return None

    return mat_file["data"]


def write_ntu_skeleton_file(
    extracted_data, output_dir=None, extension="skeleton"
):
    """
    Takes a list of extracted data dictionaries and writes them to a .skeleton file

    TODO: support other file formats such as .npy/.npz

    extracted_data - a list of dictionaries. The dictionaries follow the following
    format:

    {
        filename: name of the mat file
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
    output_dir - The output directory for the .skeleton files, defaults to project
    root

    extension - the extension of the output file. Currently, only .skeleton files
    will be generated

    Raises:
    =======
    ValueError: if extracted_data is not a list
    """
    if extracted_data is None or not isinstance(extracted_data, list):
        raise ValueError("Expected a list of extracted data dictionaries")

    if output_dir is None:
        project_root = get_project_root()
        skeleton_file_output_path = Path.joinpath(
            project_root, "output_skeleton_files"
        )
    else:
        skeleton_file_output_path = Path(output_dir)

    os.makedirs(skeleton_file_output_path, exist_ok=True)

    print("Generating skeleton files...")
    
    fl = open("temp_patient_info_file.txt", "r")
    temp_file_name = fl.read()
    filename = temp_file_name
    fl.close()
    
    for extracted_datum in tqdm(extracted_data):
        datum_to_write = []
        #filename = extracted_datum["filename"].split(".")[0]
        datum_to_write.append(str(extracted_datum["frame_count"]))
        frame_data = extracted_datum["frame_data"]

        for frame_datum in frame_data:
            datum_to_write.append(str(frame_datum["num_subjects"]))
            datum_to_write.append(
                " ".join(
                    list(
                        map(
                            lambda input: str(input),
                            [
                                frame_datum["subject_id"],
                                frame_datum["meta_data"]["cliped_edges"],
                                frame_datum["meta_data"][
                                    "hand_left_confidence"
                                ],
                                frame_datum["meta_data"]["hand_left_state"],
                                frame_datum["meta_data"][
                                    "hand_right_confidence"
                                ],
                                frame_datum["meta_data"]["hand_right_state"],
                                frame_datum["meta_data"]["is_resticted"],
                                frame_datum["meta_data"]["lean_x"],
                                frame_datum["meta_data"]["lean_y"],
                                frame_datum["meta_data"]["tracking_state"],
                            ],
                        )
                    )
                )
            )
            datum_to_write.append(str(frame_datum["number_of_joints"]))

            for (
                depth_xy,
                color_xy,
                camera_xyz,
                joint_orientation,
                tracking_state,
            ) in zip(
                frame_datum["depth_xy"],
                frame_datum["color_xy"],
                frame_datum["camera_xyz"],
                frame_datum["joint_orientation"],
                frame_datum["tracking_state"],
            ):
                depth_x, depth_y = depth_xy["depth_x"], depth_xy["depth_y"]
                color_x, color_y = color_xy["color_x"], color_xy["color_y"]
                camera_x, camera_y, camera_z = (
                    camera_xyz["camera_x"],
                    camera_xyz["camera_y"],
                    camera_xyz["camera_z"],
                )
                w, x, y, z = (
                    joint_orientation["w"],
                    joint_orientation["x"],
                    joint_orientation["y"],
                    joint_orientation["z"],
                )

                # 'x', 'y', 'z', 'depthX', 'depthY', 'colorX', 'colorY',
                # ‘'orientationW', 'orientationX', 'orientationY', 'orientationZ',
                # 'trackingState'
                line = "{} {} {} {} {} {} {} {} {} {} {} {}".format(
                    camera_x,
                    camera_y,
                    camera_z,
                    depth_x,
                    depth_y,
                    color_x,
                    color_y,
                    w,
                    x,
                    y,
                    z,
                    tracking_state,
                )
                datum_to_write.append(line)

        with open(
            Path.joinpath(
                skeleton_file_output_path, "{}.{}".format(filename, extension)
            ),
            "w",
        ) as skeleton_file:
            skeleton_file.writelines("\n".join(datum_to_write))
