set -e

name_data_folder_after_eval=$1                                                                        
                                                                                                      
if [ -d "./data/" ]                                                                                   
then                                                                                                  
    echo "Remove data folder"                                                                         
    rm -rf "./data/"                                                                                  
else                                                                                                  
    echo "Hi"                                                                                         
    #mkdir "./data/"                                                                                  
fi                                                                                                    

if [ -d "./static/data_template" ]
then 
    echo "Already have data_template folder! Skip"
else
    bash utils/create_folder_tree.sh
fi

python create_data.py --root_path static/test_data/ --save_path static/data_template/gt/mot_challenge/MOT16 --template static/data_template/ --mode test                                                            
                                                                                                      
mv ./data ./TrackEval                                                                                 
cd TrackEval                                                                                          
                                                                                                      
bash eval.sh

if [ $# -eq 1 ]                                            
then                                                       
   echo "Rename and mv to benchmarks folder"               
   mv "data/"  ${name_data_folder_after_eval}                    
   mv ${name_data_folder_after_eval}  "benchmarks/"      
else                                                       
   echo "Not rename and mv data folder to benchmark folder"
fi                                                         
                                                           
cd .. # back to mot_eval folder

python utils/get_benchmarks.py --path TrackEval/benchmarks/${name_data_folder_after_eval}/trackers/mot_challenge/MOT16-test/ch_yolov5m_deep_sort/pedestrian_detailed.csv --save_path static/benchmarks

