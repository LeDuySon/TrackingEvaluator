import os
import glob
import argparse

def xyxy2xywh(coord):
    """[summary]

    Args:
        coord ([list]): list contain coord [xmin, ymin, xmax, ymax]

    Returns:
        coord [list]: list contain coord [x, y, w, h]
    """
    
    xmin, ymin, xmax, ymax = coord
    if(isinstance(xmin, str)):
        xmin, ymin, xmax, ymax = float(xmin), float(ymin), float(xmax), float(ymax)
    h, w = ymax-ymin, xmax-xmin
    x, y = xmax - w/2, ymax - h/2
    return x, y, w, h

def get_info_from_gt(file): 
    """[summary]

    Args:
        file ([type]): [description]

    Returns:
        [type]: [description]
    """
    track_info = []
    with open(file, "rt") as f:
        for line in f:
            tmp = line.strip().split(" ")[:7]
            print(line)
            tmp = list(map(int, tmp))
            frame_id = tmp[5]
            track_id = tmp[0]
            coords = tmp[1:5]
            # because all id we annotate always have all frame in annotation files, so we add a lost bool to specify whether or not this object id is in that frame
            loss = tmp[6]
            track_info.append((frame_id+1, track_id, coords, loss)) # mot format index start from 1
    return track_info
            
            
def convert2mot(file, save_folder): 
    track_info = get_info_from_gt(file)
    
    save_format = '{frame},{id},{x1},{y1},{w},{h},1,-1,-1,-1\n'
    file_name = file.split("/")[-1]
    save_path = os.path.join(save_folder, file_name)
    
    with open(save_path, "wt") as f:
        for info in track_info:
            frame_id, track_id, coords, loss= info
            if(loss):
                continue
            x1, y1, w, h = xyxy2xywh(coords) 
            line = save_format.format(frame=frame_id, id=track_id, x1=x1, y1=y1, w=w, h=h) 
            f.write(line)

def create_folder(folder):
    if(not os.path.exists(folder)):
        os.mkdir(folder) 
    
    
def run(args):
    gt_files = glob.glob(args.gt_path + "/*.txt") 
    # create save folder if not exists
    create_folder(args.save_folder)
    
    for file in gt_files:
        convert2mot(file, args.save_folder)
    
    assert len(os.listdir(args.save_folder)) == len(gt_files), "Not enough files"
    
    print("Success convert data to mot format")

def process(args):
    files = glob.glob(args.gt_path + "/*.txt")
    save_format = '{frame},{id},{x1},{y1},{w},{h},1,-1,-1,-1\n'
    for file in files:
        lines = []
        with open(file, "rt") as f:
            for line in f:
                lines.append(line.strip().split(","))
        with open(file, "wt") as f:
            for line in lines:
                frame_id, track_id, x1, y1, w, h = line[:6]
                f.write(save_format.format(frame=frame_id, id=track_id, x1=x1, y1=y1, w=w, h=h))
    
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Convert gt to mot format')
    parser.add_argument('--gt_path', type=str, help="Path to folder contains gt files")
    parser.add_argument('--save_folder', type=str, help="Path to save folder") 
    args = parser.parse_args()
    
    run(args)
    #process(args)
     

    
