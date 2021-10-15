import os
import glob
import re
import argparse
import shutil
import cv2

SEQINFO_DICT = {"name": "",
                "imDir": "img1",
                "frameRate": 20,
                "seqLength": 1200, # all videos just 60 seconds 
                "imWidth": 1280,
                "imHeight": 720,
                "imExt": ".jpg"}

BENCHMARK = "MOT16"

def create_seqinfo(cur_path, **kwargs):
        
    with open(os.path.join(cur_path, "seqinfo.ini"), "w") as f:
        f.write("[Sequence]\n")
        for k, v in kwargs.items():
            f.write("{}={}".format(k, v) + "\n")

    with open(os.path.join(cur_path, "gt", "seqinfo.ini"), "w") as f:
        f.write("[Sequence]\n")
        for k, v in kwargs.items():
            f.write("{}={}".format(k, v) + "\n")
    

#def get_seqLength(file): 
#    with open(file, "rt") as f:
#        lines = []
#        for line in f:
#            lines.append(line.strip().split(","))   
#        frame_max = sorted(lines, key=lambda x: int(x[0]))[-1][0]
#    return int(frame_max)
    

def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)

def create_seqini(seq):
    video_name = seq.split(".")[0] + ".mp4"

    default_folder="/data/DATA_ROOT/combine_dataset/TRAIN_DATASET/"
    cap = cv2.VideoCapture(os.path.join(default_folder, video_name))
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = int(cap.get(cv2.CAP_PROP_FPS))
    
    if(length == 0):
        raise ValueError("Your video path folder to get metadata was wrong, current path: " +  default_folder)
    seqini = SEQINFO_DICT.copy()
    seqini["name"] = seq
    seqini["frameRate"] = 10
    seqini["seqLength"] = length
    seqini["imWidth"] = width
    seqini["imHeight"] = height
    return seqini
    
def create_seq(seq, root_path):
    """[summary]

    Args:
        seq ([str]): sequence name 
    """
    seq_name = seq.split("/")[-1] 
    # create seq folder 
    create_folder(seq)
    gt_seq_folder = os.path.join(seq, "gt")
    create_folder(gt_seq_folder)
    source_gt = os.path.join(root_path, "gt", seq_name + ".txt")
    shutil.copy(source_gt, gt_seq_folder + "/gt.txt")
    
    seqinfo = create_seqini(seq_name)
    create_seqinfo(seq, **seqinfo)

def create_gt_branch(branch_path, root_path):
    gt_files = os.listdir(os.path.join(root_path, "gt"))
    
    for file in gt_files:
        seq_name = file.split(".")[0]
        seq = os.path.join(branch_path, seq_name)
        print("Create: ", seq)
        create_seq(seq, root_path)
    # create seqmaps folder 
    create_seqmaps(branch_path)
    
def create_trackers_branch(branch_path, root_path):
    pred_files = os.listdir(os.path.join(root_path, "pred"))
    
    for file in pred_files:
        source = os.path.join(root_path, "pred", file)
        dest = os.path.join(branch_path, file)
        
        if(not os.path.isfile(dest)):
            # create file if it doesn't exist
            f = open(dest, "wt")
        shutil.copy(source, dest)

def create_seqmaps_file(name, seqList): #
    with open(name, "wt") as f:
        f.write("name\n")
        for seq in seqList:
            f.write(seq + "\n")
    
    
def create_seqmaps(path):
    template_names = ["train", "test", "all"]
    seqList = os.listdir(path)
    seqmaps_path = path.replace(BENCHMARK, "seqmaps")
    
    for name in template_names:
        tmp = os.path.join(seqmaps_path, BENCHMARK + "-{}.txt".format(name))
        create_seqmaps_file(tmp, seqList)
        
        
    
    
def run(args):
    """Main function to create data

    Args:
        args ([type]): env argument 
    """
    
    # create a folder tree from template folder
    shutil.copytree(args.template, "./data")
    # change template folder to our data folder
    args.save_path = args.save_path.replace("static/data_template", "data")
    # create branch in data/ folder
    gt_branch = args.save_path
    trackers_path = args.save_path.replace("gt", "trackers") 
    trackers_branch = os.path.join(trackers_path, "ch_yolov5m_deep_sort", "data")  # MPNTrack: default tracker for mot challenge in trackEval repos
    
    create_gt_branch(gt_branch, args.root_path)
    create_trackers_branch(trackers_branch, args.root_path)
    
    os.rename(args.save_path, args.save_path.replace(BENCHMARK, BENCHMARK + "-{}".format(args.mode)))
    os.rename(trackers_path, trackers_path.replace(BENCHMARK, BENCHMARK + "-{}".format(args.mode)))

    
    print("Finish!!!")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--root_path', '-rp', type=str,
                                        help="path to folder contain gt and prediction folder")
    parser.add_argument('--save_path', '-sp', type=str, 
                                        help="path to save gt seq and file")
    parser.add_argument('--template', '-t', type=str,
                                        help="Template folder tree for mot dataset")
    parser.add_argument('--mode', '-m', type=str,
                                        help="train|test|all mode with respect to our seqmaps file")
    #parser.add_argument('--img_sz', '-s', type=str, nargs="+", help="image resolution (w, h"
    args = parser.parse_args()
    
    #python create_data.py -root_path test_data/ --save_path data_template/gt/mot_challenge/Uet_track_vehicle/ --template data_template/ --mode train                                                                                  

    run(args)
    
    # tricks hehe




