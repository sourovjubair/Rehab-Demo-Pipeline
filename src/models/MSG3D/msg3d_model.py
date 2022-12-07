import pathlib
import yaml
import torch
from .model.msg3d import Model


class MSG3D(object):
    def __init__(self, exercise_type) -> None:
        """
        exercise_type: should be one of "ex1, ex2, ex3, ex4, ex5"
        """
        self.known_exercise_types = ["ex1", "ex2", "ex3", "ex4", "ex5"]
        if exercise_type not in self.known_exercise_types:
            raise Exception("Exercise type not recognized")
        self.exercise_type = exercise_type
        self.load_model()

    def load_model(self):
        current_folder = pathlib.Path(__file__).parent
        with open(
            pathlib.Path.joinpath(
                current_folder,
                "config/train_joint_{}.yaml".format(self.exercise_type),
            ),
            "r",
        ) as conf:
            self.config = yaml.load(conf, Loader=yaml.FullLoader)

        self.model = Model(**self.config["model_args"])

        self.weights_path = pathlib.Path.joinpath(
            current_folder,
            "checkpoints/{}_checkpoint.pt".format(self.exercise_type),
        )
        self.weights = torch.load(self.weights_path)
        self.model.load_state_dict(self.weights)

    def predict_scores(self, input):
        """
        input: Tensor of batch size 1, shape should be (1, C, T, V, M)
        """
        assert isinstance(input, torch.Tensor), "The input must be a Tensor"
        assert (
            len(input.shape) == 5
        ), "The tensor shape should be (1, C, T, V, M)"
        with torch.no_grad():
            out = self.model(input.float())

        return out
