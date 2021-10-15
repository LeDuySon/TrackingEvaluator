set -e 

model_name=$1
model_path=$2
target_folder=$3

for model_version in $(find $model_path -name "${model_name}*"); 
do
    rm -rf "${target_folder}/*"
    arrIN=(${model_version//results/ })
    save_name=${arrIN[1]}
    spliter2=(${save_name//// })
    save_name=${spliter2[0]}
    echo $save_name
    
    cp ${model_version}/*.txt $target_folder
    bash create_mot_eval.sh $save_name
done
