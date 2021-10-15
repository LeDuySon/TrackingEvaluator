set -e 

path=$1 # path to txt folder
channel_path=$2 # path to channel folder infos

for file in $path/*.txt
do
    echo $file
    python post_process/output_post_processing.py --pred_file $file --channel_info $channel_path --mode iou
done
