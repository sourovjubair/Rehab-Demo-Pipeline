import os
import torch
import numpy as np
from models.MSG3D.msg3d_model import MSG3D
from data_converter.converter import LabDataConverter
from data_converter.utils import write_ntu_skeleton_file, get_project_root
from utils.skeleton_to_numpy import SkeletonToNumpy
from utils.ntu_visualizer import visualize

exercise_map = {
    "Exercise Type 1": "ex1",
    "Exercise Type 2": "ex2",
    "Exercise Type 3": "ex3",
    "Exercise Type 4": "ex4",
    "Exercise Type 5": "ex5",
}


class Pipeline(object):
    """
    The main business logic for reading data files, inferencing the scores and
    visualization
    """

    def __init__(self):
        self.valid_datatypes = [
            "ntu",
            "kimore",
            "live-feed",
            "lab-kinect-mat",
        ]
        self.valid_models = ["msg3d", "stgcn"]
        self.valid_exercise_types = [
            "Exercise Type 1",
            "Exercise Type 2",
            "Exercise Type 3",
            "Exercise Type 4",
            "Exercise Type 5",
        ]

    def run(
        self,
        datatype=None,
        modelType=None,
        exerciseType=None,
        shouldVisualize=False,
        selectedDataFile=None,
        data=None,
    ):
        if (
            datatype not in self.valid_datatypes
            or modelType not in self.valid_models
            or exerciseType not in self.valid_exercise_types
        ):
            raise Exception("Received invalid argument(s)")

        if selectedDataFile is None and datatype != "live-feed":
            raise Exception(
                "Data type is NOT 'live-feed' but no data file was provided"
            )

        if data is None and datatype == "live-feed":
            raise Exception(
                "Data type is 'live-feed' but no data was provided"
            )

        exercise_type = exercise_map[exerciseType]

        if datatype != "live-feed":
            data_tensor = self.__get_tensor_from_file(
                datatype, selectedDataFile
            )
        else:
            data_tensor = self.__get_tensor_from_live_feed_data(data)

        model = self.__get_model(modelType, exercise_type)
        scores = model.predict_scores(data_tensor)

        # when in live-feed mode, we don't want the skeleton animation
        # to display since we are playing the video itself
        if datatype == "live-feed":
            shouldVisualize = False

        if shouldVisualize:
            animation = visualize(
                data=data_tensor.cpu().numpy(),
                indices=[0],
                normalized=True,
                change_order=(datatype == "lab-kinect-mat"),
            )
            return (animation, scores)

        return (None, scores)

    def __get_numpy_format_data(
        self, skeleton_data, skeleton_file_output_path=None, filename=None
    ):
        if skeleton_file_output_path is None:
            skeleton_file_output_path = os.path.join(".", "temp")
            #skeleton_file_output_path = "temp_patient_info_file.txt"

        write_ntu_skeleton_file(
            skeleton_data, output_dir=skeleton_file_output_path
        )

        if filename is None:
            fl = open("temp_patient_info_file.txt", "r")
            temp_file_name = fl.read()
            filename = temp_file_name
            fl.close()
            #filename = skeleton_data[0]["filename"]

        filename += ".skeleton"
        print("This is file name: ",filename)
        skel2numpy = SkeletonToNumpy()
        data = skel2numpy.skeleton_to_numpy(
            os.path.join(skeleton_file_output_path, filename), max_body=1,
        )

        return data

    def __get_tensor_from_live_feed_data(self, live_feed_data):
        data = self.__get_numpy_format_data(live_feed_data)

        if data is not None:
            data = np.expand_dims(data, axis=0)
            return torch.Tensor(data)

    def __get_tensor_from_file(self, datatype, data_file_path):
        filename = data_file_path.rsplit("/", 1)[-1].split(".")[0]
        data = None

        if datatype == "kimore":
            # we expect numpy (.npy/.npz) files here
            if not data_file_path.endswith(
                ".npy"
            ) and not data_file_path.endswith(".npz"):
                raise Exception(
                    "For {} data type, expected .npy/.npz files".format(
                        datatype
                    )
                )
            data = np.load(data_file_path)

        elif datatype == "lab-kinect-mat":
            if not data_file_path.endswith(".mat"):
                raise Exception(
                    "For {} data type, expected .mat files".format(datatype)
                )
            converter = LabDataConverter([data_file_path])
            converter.read_data_feed()
            converter.extract_data()
            data = self.__get_numpy_format_data(
                converter.skeleton_data,
                os.path.join(get_project_root(), "output_skeleton_files"),
                filename,
            )

        if data is not None:
            data = np.expand_dims(data, axis=0)
            return torch.Tensor(data)

        raise Exception(
            "Something went wrong, data could not be read from file"
        )

    def __get_model(self, model_type, exercise_type):
        if model_type == "msg3d":
            msg3d_model = MSG3D(exercise_type)
            return msg3d_model

        raise Exception("Unknown model type: {}".format(model_type))
