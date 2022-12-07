import sys
from os.path import abspath
from pathlib import Path
import cv2
from PIL import Image
import serial
import time
import csv
from datetime import datetime

sys.path.extend([str(Path(abspath(__file__)).parent.parent)])

import copy
import numpy as np
import ui.utils.utils_PyKinectV2 as utils
from PyQt5.QtCore import pyqtSignal, QThread, QTime
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
from open3d import camera
from data_converter.converter import KinectDataConverter


class KinectRecorder(QThread):
    frame_data_signal = pyqtSignal(np.ndarray)
    elapsed_time_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._run_flag = False

        # Kinect specific parameters
        self._kinect = PyKinectRuntime.PyKinectRuntime(
            PyKinectV2.FrameSourceTypes_Body
            | PyKinectV2.FrameSourceTypes_BodyIndex
            | PyKinectV2.FrameSourceTypes_Color
            | PyKinectV2.FrameSourceTypes_Depth
            | PyKinectV2.FrameSourceTypes_Infrared
        )
        self.depth_width, self.depth_height = (
            self._kinect.depth_frame_desc.Width,
            self._kinect.depth_frame_desc.Height,
        )  # Default: 512, 424
        self.color_width, self.color_height = (
            self._kinect.color_frame_desc.Width,
            self._kinect.color_frame_desc.Height,
        )  # Default: 1920, 1080
        self._depth_scale = (
            0.001  # Default kinect depth scale where 1 unit = 0.001 m = 1 mm
        )
        self._clipping_distance_in_meters = (
            1.5  # Set the maximum distance to display the point cloud data
        )
        self._clipping_distance = (
            self._clipping_distance_in_meters / self._depth_scale
        )  # Convert dist in mm to unit
        self._ppx = 260.166
        self._ppy = 205.197
        self._fx = 367.535
        self._fy = 367.535  # Hardcode the camera intrinsic parameters for backprojection
        self._intrinsic = camera.PinholeCameraIntrinsic(
            self.depth_width,
            self.depth_height,
            self._fx,
            self._fy,
            self._ppx,
            self._ppy,
        )

        # the array to hold the frame data
        self.data = list()

        # the kinect data converter instance
        self.kinect_data_converter = KinectDataConverter(
            self._kinect,
            self.color_height,
            self.color_width,
            self.depth_height,
            self.depth_width,
            self._intrinsic,
            self._depth_scale,
        )
        self.elapsed_timer = None
        self.video_writer = None

    def run(self):
        self.elapsed_timer = QTime()
        self.elapsed_timer.start()
        self.video_writer = cv2.VideoWriter(
            "output.avi",
            cv2.VideoWriter_fourcc("M", "J", "P", "G"),
            10,
            (self.depth_width, self.depth_height),
        )
        
        #initializing empty list to store sensor data
        data =[]

        #starting the sensor
        ser = serial.Serial('COM4', 500000, timeout=0)
        
        while self._run_flag:
            if ser.isOpen():
                line = ser.readline()
                line = line.decode(errors= 'replace').rstrip()
                
                values = line.split(",")
                t = datetime.now()
                print(t)
                #print(values)
                values.append(str(t))
                data.append(values)
                # data.append(str(t))
                print(data)
                ser.cancel_read()

            #end of collecting sensor data

            (
                color_img,
                body_frame,
                frame_data,
            ) = self.kinect_data_converter.read_data_feed()
            frame_data = self.kinect_data_converter.extract_data(frame_data)

            align_color_img = self.visualize_skeleton(color_img, body_frame)
            self.frame_data_signal.emit(align_color_img)

            if self.elapsed_timer is not None:
                self.elapsed_time_signal.emit(
                    str(self.elapsed_timer.elapsed())
                )

            rgbImage = cv2.cvtColor(align_color_img, cv2.COLOR_RGBA2RGB)
            self.video_writer.write(rgbImage)

            if frame_data is not None:
                self.data.append(frame_data)
        
        #close sensor
        ser.close()
        
        #open the file contaning patient info 
        patient_info_file = open("temp_patient_info_file.txt", "r")
        sensor_file = patient_info_file.read()
        patient_info_file.close()
        
        # opening the csv file in 'w+' mode
        file = open('./temp/'+sensor_file+'.csv', 'w+', encoding="utf-8", newline ='')
        
        # writing the data into the file
        col_name = ['Sensor','AccX','AccY','AccZ','GyroX','GyroY','GyroZ','MagX','MagY','MagZ','packNo','TimeStamp']
        with file:   
            write = csv.writer(file)
            write.writerow(col_name)
            write.writerows(data)
        file.close()
        # sensor data collector end


    def visualize_skeleton(self, color_img, body_frame):
        align_color_img = utils.get_align_color_image(self._kinect, color_img)
        align_color_img = utils.draw_bodyframe(
            body_frame, self._kinect, align_color_img
        )  # Overlay body joints on align_color_img
        return align_color_img

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.elapsed_timer = None
        self.wait()

        self.video_writer.release()
        self.video_writer = None

        self.data = list()  # set the list to empty for next run

    def stop_thread(self):
        data_copy = copy.deepcopy(self.data)
        self.stop()
        return data_copy
