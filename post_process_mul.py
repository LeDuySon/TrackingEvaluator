import glob 
import shutil
import os
import subprocess
import argparse 

def process(files, pred_version, save_path):     
    for file in files:
        shutil.copyfile(file, f"static/test_data/pred/{os.path.basename(file)}")
        
    try:
        # run script to get benchmark with TrackEval 
        subprocess.check_call(["bash", "create_mot_eval_postprocessing.sh", f"{pred_version}_postprocess_eval"])
    except subprocess.CalledProcessError as e:
        raise Exception("Error when running benchmark: ", e)
    
def clear_folder(folder):
    files = glob.glob(os.path.join(folder, "*.txt"))
    for file in files:
        os.remove(file)
    
def run(args):
    h_path = "trackers/mot_challenge/MOT16-test/ch_yolov5m_deep_sort/data"
    pred_versions = glob.glob(os.path.join(args.pred_path, "*"))
    
    for pver in pred_versions:
        clear_folder(args.save_pred_path)
        assert len(os.listdir(args.save_pred_path)) == 0, "Folder not cleared"

        print("Process: ", os.path.basename(pver))
        pred_file_path = os.path.join(pver, h_path)
        
        if(len(os.listdir(pred_file_path)) == 0):
            raise ValueError("path to pred file wrong") 
        
        pred_files = glob.glob(os.path.join(pred_file_path,"*.txt")) 
        process(pred_files, os.path.basename(pver), args.save_pred_path)
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get directions')
    parser.add_argument('--pred_path', type=str, help='Path to prediction version benchmarks', required=True)
    parser.add_argument('--save_pred_path', type=str, help="path to pred folder", required=True)
    args = parser.parse_args()
    
    run(args)
