import pandas as pd
import argparse
import numpy as np
import os

def get_hota_metrics(x):
    return 100 * np.mean(x.values)

def main(args):
    
    benchmark_cols = ["MOTA", "IDF1", "IDSW", "MOTP", "HOTA"]
    cols = ["seq"] + benchmark_cols
    
    hota_range = np.arange(0.05, 0.99, 0.05)
    hota_cols = ["HOTA___" + str(int(100*k)) for k in hota_range]
    
    df = pd.read_csv(args.path)
    
    # calculate hota metrics
    df_hota = df[hota_cols]
    df["HOTA"] = df_hota.apply(get_hota_metrics, axis=1)

    df_benchmark = df[cols]

    save_name = args.path.split("/")[-6] + ".csv"
    df_benchmark.to_csv(os.path.join(args.save_path, save_name), index=False)
    print("Finish")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')      
    parser.add_argument('--path', '-p', type=str,                         
        help="path to csv result file")
    parser.add_argument('--save_path', '-sp', type=str,                         
                                                help="path to save benchmark file")    
    args = parser.parse_args()

    main(args)
