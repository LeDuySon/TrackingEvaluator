# Data
- static/ folder tree: 
```
.
├── benchmarks
├── data_template
│   ├── gt
│   │   └── mot_challenge
│   │       ├── MOT16
│   │       └── seqmaps
│   └── trackers
│       └── mot_challenge
│           └── MOT16
│               └── ch_yolov5m_deep_sort
│                   └── data
└── test_data
    ├── gt
    └── pred
```
- Prepare:
  + Put your all your gt files in test_data/gt folder, in folder utils, run:
  ```
  python get_gt_file --root_path {path contain all your data} --save_path {static/test_data/gt}
  ```
  + Put your prediction files in test_data/pred folder 
  + Rename your prediction files the same as gt folder. eg: gt/NVR-CH01... -> pred/NVR-CH01
- Notes: 
  + Name of prediction and groundtruth files must be matched 

# Evaluate:
- In create_data.py, modify line 47 to path of folder contain all videos 
- In mot_eval/ folder, run: 
```
bash create_mot_eval.sh {name of your save folder result eg. fairmot_dla34_finetune_dataset...}
```
