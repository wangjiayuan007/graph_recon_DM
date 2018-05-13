#!/bin/bash

threshold=$1
fileName=$2

cd /Users/jiayuanwang/Documents/graph_recon_DM/
#mkdir "$fileName"
#cd "$fileName"

#./spt_cpp/cmake-build-debug/spt_cpp dataset/"$fileName"/SC.bin result/"$fileName" $threshold 2
mkdir result/"$fileName"
./spt_cpp/spt_cpp dataset/"$fileName"/SC.bin result/"$fileName" $threshold 3

##visualization
#cd ../../
#python visual.py $fileName
