import numpy as np


class SkeletonToNumpy(object):
    def __read_skeleton_filter(self, filepath):
        with open(filepath, "r") as f:
            skeleton_sequence = {}
            skeleton_sequence["numFrame"] = int(f.readline())
            skeleton_sequence["frameInfo"] = []
            for t in range(skeleton_sequence["numFrame"]):
                frame_info = {}
                frame_info["numBody"] = int(f.readline())
                frame_info["bodyInfo"] = []

                for m in range(frame_info["numBody"]):
                    body_info = {}
                    body_info_key = [
                        "bodyID",
                        "clipedEdges",
                        "handLeftConfidence",
                        "handLeftState",
                        "handRightConfidence",
                        "handRightState",
                        "isResticted",
                        "leanX",
                        "leanY",
                        "trackingState",
                    ]
                    body_info = {
                        k: float(v)
                        for k, v in zip(body_info_key, f.readline().split())
                    }
                    body_info["numJoint"] = int(f.readline())
                    body_info["jointInfo"] = []
                    for v in range(body_info["numJoint"]):
                        joint_info_key = [
                            "x",
                            "y",
                            "z",
                            "depthX",
                            "depthY",
                            "colorX",
                            "colorY",
                            "orientationW",
                            "orientationX",
                            "orientationY",
                            "orientationZ",
                            "trackingState",
                        ]
                        joint_info = {
                            k: float(v)
                            for k, v in zip(
                                joint_info_key, f.readline().split()
                            )
                        }
                        body_info["jointInfo"].append(joint_info)
                    frame_info["bodyInfo"].append(body_info)
                skeleton_sequence["frameInfo"].append(frame_info)

        return skeleton_sequence

    def __get_nonzero_std(self, s):  # tvc
        index = s.sum(-1).sum(-1) != 0  # select valid frames
        s = s[index]
        if len(s) != 0:
            s = (
                s[:, :, 0].std() + s[:, :, 1].std() + s[:, :, 2].std()
            )  # three channels
        else:
            s = 0
        return s

    def skeleton_to_numpy(
        self, filepath, max_body=4, num_joint=25, max_body_true=1
    ):
        seq_info = self.__read_skeleton_filter(filepath)
        data = np.zeros((max_body, seq_info["numFrame"], num_joint, 3))
        for n, f in enumerate(seq_info["frameInfo"]):
            for m, b in enumerate(f["bodyInfo"]):
                for j, v in enumerate(b["jointInfo"]):
                    if m < max_body and j < num_joint:
                        data[m, n, j, :] = [v["x"], v["y"], v["z"]]
                    else:
                        pass

        # select two max energy body
        if max_body > 1:
            energy = np.array([self.__get_nonzero_std(x) for x in data])
            index = energy.argsort()[::-1][0:max_body_true]
            data = data[index]

        data = data.transpose(3, 1, 2, 0)
        return data
