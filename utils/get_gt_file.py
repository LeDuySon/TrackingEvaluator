import argparse
import shutil
import os
import fnmatch

def main(args):
    print("START")

    seqs = os.listdir(args.root_path)

    for seq in seqs:
        if(not seq.endswith(".mp4")):
            for root, dirnames, filenames in os.walk(os.path.join(args.root_path, seq)):                
                for filename in fnmatch.filter(filenames, '*.txt'):
                    path = os.path.join(root, filename)
                    if("gt.txt" in path):
                        name = path.split("/")[-3] + ".txt"
                        shutil.copyfile(path, os.path.join(args.save_path, name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--root_path', '-rp', type=str,
                                        help="path to folder contain gt file")
    parser.add_argument('--save_path', '-sp', type=str, 
                                        help="path to save gt seq .txt")
    args = parser.parse_args()

    main(args)
