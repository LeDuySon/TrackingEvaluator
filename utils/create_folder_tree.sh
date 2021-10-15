mkdir data_template
cd data_template

mkdir gt

# gt branch
cd gt
mkdir mot_challenge 
cd mot_challenge
mkdir MOT16
mkdir seqmaps

cd ../.. # data_template

mkdir trackers
# trackers branch
cd trackers
mkdir mot_challenge
cd mot_challenge
mkdir MOT16
cd MOT16
mkdir ch_yolov5m_deep_sort
cd ch_yolov5m_deep_sort 
mkdir data

cd ../../../../.. # main folder
mv data_template/ static/
