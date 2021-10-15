import pandas as pd
import glob 
import os
import argparse

METRIC_EVALUATE = "HOTA"
def get_metrics(df):
    metrics = df.loc[df["seq"] == "COMBINED", METRIC_EVALUATE]
    return metrics.values[0]

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--input_path', '-V', type=str,                   
                                    help='path to all csv result')              
parser.add_argument('--model_name', '-sp', type=str,                   
                                    help="name of model")       
args = parser.parse_args()                                            

csv_files = glob.glob(os.path.join(args.input_path, f"{args.model_name}*.csv"))

best_metrics = 0
best_model = ""
for file in csv_files:
    print(file)
    df = pd.read_csv(file)
    metrics = get_metrics(df)
    if(metrics > best_metrics):
        best_metrics = metrics
        best_model = file
    print(df.loc[df["seq"] == "COMBINED"])
    
print("Best metrics: ", best_metrics)
print("Best model: ", best_model)
