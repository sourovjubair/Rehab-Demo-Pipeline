import sys
sys.path.extend(['../'])

import pickle
import argparse
import pandas as pd

from tqdm import tqdm

from data_gen.preprocess import pre_normalization


# https://arxiv.org/pdf/1604.02808.pdf, Section 3.2
# training_subjects = [
#     1, 2, 4, 5, 8, 9, 13, 14, 15, 16, 17, 18, 19, 25, 27, 28, 31, 34, 35, 38
# ]
# training_cameras = [2, 3]

max_body_true = 1
max_body_kinect = 4

num_joint = 25
max_frame = 1200

import numpy as np
import os


def read_skeleton_filter(file):
    with open(file, 'r') as f:
        skeleton_sequence = {}
        skeleton_sequence['numFrame'] = int(f.readline())
        skeleton_sequence['frameInfo'] = []
        # num_body = 0
        for t in range(skeleton_sequence['numFrame']):
            frame_info = {}
            frame_info['numBody'] = int(f.readline())
            frame_info['bodyInfo'] = []

            for m in range(frame_info['numBody']):
                body_info = {}
                body_info_key = [
                    'bodyID', 'clipedEdges', 'handLeftConfidence',
                    'handLeftState', 'handRightConfidence', 'handRightState',
                    'isResticted', 'leanX', 'leanY', 'trackingState'
                ]
                body_info = {
                    k: float(v)
                    for k, v in zip(body_info_key, f.readline().split())
                }
                body_info['numJoint'] = int(f.readline())
                body_info['jointInfo'] = []
                for v in range(body_info['numJoint']):
                    joint_info_key = [
                        'x', 'y', 'z', 'depthX', 'depthY', 'colorX', 'colorY',
                        'orientationW', 'orientationX', 'orientationY',
                        'orientationZ', 'trackingState'
                    ]
                    joint_info = {
                        k: float(v)
                        for k, v in zip(joint_info_key, f.readline().split())
                    }
                    body_info['jointInfo'].append(joint_info)
                frame_info['bodyInfo'].append(body_info)
            skeleton_sequence['frameInfo'].append(frame_info)

    return skeleton_sequence


def get_nonzero_std(s):  # tvc
    index = s.sum(-1).sum(-1) != 0  # select valid frames
    s = s[index]
    if len(s) != 0:
        s = s[:, :, 0].std() + s[:, :, 1].std() + s[:, :, 2].std()  # three channels
    else:
        s = 0
    return s


def read_xyz(file, max_body=4, num_joint=25):
    seq_info = read_skeleton_filter(file)
    data = np.zeros((max_body, seq_info['numFrame'], num_joint, 3))
    for n, f in enumerate(seq_info['frameInfo']):
        for m, b in enumerate(f['bodyInfo']):
            for j, v in enumerate(b['jointInfo']):
                if m < max_body and j < num_joint:
                    data[m, n, j, :] = [v['x'], v['y'], v['z']]
                else:
                    pass

    # select two max energy body
    energy = np.array([get_nonzero_std(x) for x in data])
    index = energy.argsort()[::-1][0:max_body_true]
    data = data[index]

    data = data.transpose(3, 1, 2, 0)
    return data

def get_label_path(label_path, filename):
    if filename[0] == 'B':
        label_path+='GPP/BackPain/B_'
    elif filename[0] == 'E':
        label_path+='CG/Expert/E_'
    elif filename[0] == 'N':
        label_path+='CG/NotExpert/NE_'
    elif filename[0] == 'P':
        label_path+='GPP/Parkinson/P_'
    elif filename[0] == 'S':
        label_path+='GPP/Stroke/S_'
    label_path+=f"{filename[filename.find('ID'):filename.find('Es')]}/"
    label_path+=f"{filename[filename.find('Es'):filename.find('Es')+3]}/Label/ClinicalAssessment_"
    label_path+=f"{filename[0:filename.find('_')+1]}"
    label_path+=f"{filename[filename.find('ID'):filename.find('Es')]}.xlsx"
    return label_path

def gendata(data_path, out_path, ignored_sample_path=None, benchmark='xview', part='eval'):
    if ignored_sample_path != None:
        with open(ignored_sample_path, 'r') as f:
            ignored_samples = [line.strip() + '.skeleton' for line in f.readlines()]
    else:
        ignored_samples = []
    sample_name = []
    sample_label = []
    for filename in sorted(os.listdir(data_path)):
        if filename in ignored_samples:
            continue
#         print(filename)
        label_path = get_label_path(data_path[:-11], filename)
        if not os.path.exists(label_path):
            print(label_path)
            issample = False
        else:
            issample = True
            label_df = pd.read_excel(label_path, engine='openpyxl')
            exercise_idx = int(filename[filename.find('Es')+2:filename.find('Es')+3])
            group = filename[0:filename.find('_')]
            clinical_total = float(label_df[f'clinical TS Ex#{exercise_idx}'])
            clinical_po = float(label_df[f'clinical PO Ex#{exercise_idx}'])
            clinical_cf = float(label_df[f'clinical CF Ex#{exercise_idx}'])
            sub_id = filename[filename.find('ID'):filename.find('Es')]
            # print(sub_id)
            # print([clinical_total, clinical_po, clinical_cf, exercise_idx, group, sub_id])
            sample_label.append([clinical_total, clinical_po, clinical_cf, exercise_idx, group, sub_id])
        # action_class = int(filename[filename.find('A') + 1:filename.find('A') + 4])
        # subject_id = int(filename[filename.find('P') + 1:filename.find('P') + 4])
        # camera_id = int(filename[filename.find('C') + 1:filename.find('C') + 4])

#         if benchmark == 'xview':
#             # istraining = (camera_id in training_cameras)
#             istraining = True
#         elif benchmark == 'xsub':
#             # istraining = (subject_id in training_subjects)
#             istraining = True
#         else:
#             raise ValueError()

#         if part == 'train':
#             issample = istraining
#         elif part == 'val':
#             issample = not (istraining)
#         else:
#             raise ValueError()

        if issample:
            sample_name.append(filename)

    with open('{}/{}_label.pkl'.format(out_path, part), 'wb') as f:
        pickle.dump((sample_name, list(sample_label)), f)

    # print(sample_label)
    fp = np.zeros((len(sample_label), 3, max_frame, num_joint, max_body_true), dtype=np.float32)

    # Fill in the data tensor `fp` one training example a time
    remove_first_n_frame = 60
    for i, s in enumerate(tqdm(sample_name)):
        # print(s)
        data = read_xyz(os.path.join(data_path, s), max_body=max_body_kinect, num_joint=num_joint)
        if data.shape[1] > max_frame:
            print(f'More than {max_frame}, crop', s, data.shape)
            data = data[:, 0:max_frame, :, :]
        if data.shape[1] > remove_first_n_frame:
            fp[i, :, 0:data.shape[1]-remove_first_n_frame, :, :] = data[:, remove_first_n_frame:, :, :]
        else:
            print(s, 'no data')
            fp[i, :, 0:data.shape[1], :, :] = data
        

    fp = pre_normalization(fp)
    np.save('{}/{}_data_joint.npy'.format(out_path, part), fp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='KiMoRe Data Converter.')
    parser.add_argument('--data_path', default='../../data/KiMoRe/ntu_format/')
    parser.add_argument('--ignored_sample_path',
                        default='')
    parser.add_argument('--out_folder', default='./out/')

    # benchmark = ['xsub', 'xview']
    benchmark = ['xsub']
    # part = ['train', 'val']
    part = ['train']
    arg = parser.parse_args()
    
#     print(os.listdir('.'))

    for b in benchmark:
        for p in part:
            out_path = os.path.join(arg.out_folder, b)
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            print(b, p)
            gendata(
                arg.data_path,
                out_path,
                None,
                benchmark=b,
                part=p)