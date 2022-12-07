import argparse
import os
from data_converter.converter import LabDataConverter
from data_converter.utils import write_ntu_skeleton_file

parser = argparse.ArgumentParser(
    description=(
        "Convert data feeds/formats to the standard NTU skeleton data format."
    )
)
supported_types = ["lab-kinect", "kimore", "live-feed", "uiprmd"]
model_choices = ["m3d", "stgcn"]
parser.add_argument(
    "-t",
    "--feed-type",
    default=None,
    help="Type of the data to be given as input",
    choices=supported_types,
)
parser.add_argument(
    "-m",
    "--model-type",
    help="Type of the model to be used on the skeleton data",
    default=model_choices[0],
    choices=model_choices,
)
parser.add_argument(
    "-i", "--input-dir", help="Directory for the input feed/data"
)
parser.add_argument(
    "-o",
    "--output-dir",
    nargs="?",
    default=None,
    help="Output directory for the .skeleton files. Defaults to script root",
)

if __name__ == "__main__":
    args = parser.parse_args()

    if args.input_dir is None:
        raise Exception("Input data feed directory not provided")

    if args.feed_type == "lab-kinect":
        data_files = list(
            map(
                lambda file_name: os.path.join(args.input_dir, file_name),
                os.listdir(args.input_dir),
            )
        )
        converter = LabDataConverter(data_files)
        converter.read_data_feed()
        converter.extract_data()
        write_ntu_skeleton_file(converter.skeleton_data)
