import os 
import time 
import argparse
import json 
import re

def xywh2xyxy(coord):
    x, y, w, h = coord 
    x2, y2 = x + w, y + h 
    
    return x, y, x2, y2 

def scaled_yolo_coord(coord, img_size):
    h_img, w_img = img_size
    xc, yc, w, h = coord
    
    x, y = xc - w/2, yc - h/2
    xs, ys, ws, hs = x * w_img, y * h_img, w * w_img, h * h_img
    
    return xs, ys, ws, hs 

def get_channel_info(file="ch06.json"):
	with open(file, "rt") as f:
		info = json.load(f) 
  
	return info

def check_in_rect_center_point(point, rect):
	x1, y1, x2, y2 = rect
 
	if(point[0] > min(x1, x2) and point[0] < max(x1, x2) and point[1] > min(y1, y2) and point[1] < max(y1, y2)):
		return True
	return False

def check_in_rect_iou(bb1, bb2, threshold=0.85):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters
    ----------
    bb1 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x, y) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    threshold: float
        Overlap threshold
    Returns
    -------
    bool
        Determine whether or not ignore this box
    """
    # print("bb1: ", bb1)
    # print("bb2: ", bb2)
    if(bb1['x1'] >= bb1['x2'] or bb1['y1'] >= bb1['y2'] or bb2['x1'] >= bb2['x2'] or bb2['y1'] >= bb2['y2']):
        print("ZERO AREA BOXES")
        return False
    
    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area)
    assert iou >= 0.0, "Error"
    assert iou <= 1.0, "Error"
    
    # print("IOU: ", iou)
    if iou > threshold:
        return True
    
    return False

def get_center_point(rect):
	x1, y1, w, h = rect 
	c_x, c_y = x1 + w/2, y1 + h/2
	return c_x, c_y

def is_in_invalid_area(target_rect, rects, mode):
    coord_name = ["x1", "y1", "x2", "y2"]
    
    c_x, c_y = get_center_point(target_rect)
    
    if mode == 'iou':
        x1, y1, x2, y2 = xywh2xyxy(target_rect)
        bb1 = {k:v for k, v in zip(coord_name, [x1, y1, x2, y2])}
    
    for rect in rects:
        if(mode == 'iou'):
            bb2 = {k:v for k, v in zip(coord_name, rect)}
            
            if(check_in_rect_iou(bb1, bb2)):
                return True
        else:
            if(check_in_rect_center_point([c_x, c_y], rect)):
                return True 
    
    return False 

def filter_region(data, info, mode='iou'):
    xc, yc, w, h = list(map(float, data[2:6]))
    x1, y1, w, h = scaled_yolo_coord([xc, yc, w, h], info["img_size"])
    
    if(is_in_invalid_area([x1, y1, w, h], info["boxes"], mode)):
       # print("Invalid coord: ", x1, y1, w, h)
        return True 
    
    return False
    
def filter_boxes(args):
    info = get_channel_info(args.channel_info)

    pp_out = []
    with open(args.pred_file, "rt") as f:
        for line in f:
            p = line.strip().split(" ")
            if(not (len(p) > 4)):
                p = line.strip().split(",")
            
            cloned = p.copy()
            x1, y1, w, h = list(map(float, p[2:6]))

            #print(x1, y1, w, h)
            if(is_in_invalid_area([x1, y1, w, h], info["boxes"], args.mode)):
                print("Invalid coord: ", x1, y1, w, h)
                continue
            
            pp_out.append(",".join(list(map(str,p))))
            #pp_out.append(",".join(cloned))
                    
    with open(args.pred_file, "wt") as f:
        for line in pp_out:
            f.write(line + "\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get directions')
    parser.add_argument('--pred_file', type=str, help='Path to prediction for postprocessing', required=True)
    parser.add_argument('--channel_info', type=str, help='Path to file contain ignore region coordinate and img size', default="static/ignore_region")
    parser.add_argument('--mode', type=str, help='Filter boxes by iou or center point', default="iou")
    args = parser.parse_args()
    
    # get channel name 
    channel_pattern = r"NVR-(CH[0-9]{2}).+"
    video_name = os.path.basename(args.pred_file)
    channel_name = re.search(channel_pattern, video_name)
    if(channel_name is not None):
        channel_name = channel_name.group(1)
        
    args.channel_info = os.path.join(args.channel_info, f"{channel_name}.json")
    print(args.channel_info)
    if(not os.path.isfile(args.channel_info)):
        raise ValueError("Invalid name of pred file or ignore region for this channel not exists")
    
    filter_boxes(args)
