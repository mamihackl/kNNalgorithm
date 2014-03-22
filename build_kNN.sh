#!/bin/bash
#Ling572 HW4 kNN
#Nat Byington
#Mami Sasaki
command='./build_kNN.py'
path='../../dropbox/09-10/572/hw4/examples/'
trainf='train.vectors.txt'
testf='test.vectors.txt'
us="_"
kval="1 5 10"
similarity_func="1 2"
sysf='sys.'
accf='acc_file.'
outdir='q2/'

#create directlry if it doesn't exist already
if [ ! -d "$outdir" ];then
 mkdir -p $outdir 
fi

#q2
for sf in $similarity_func
 do 
 for k in $kval
  do
  $command $path$trainf $path$testf $k $sf $outdir$sysf$sf$us$k >$outdir$accf$sf$us$k
 done
done

outdir='q3/'

#create directlry if it doesn't exist already
if [ ! -d "$outdir" ];then
 mkdir -p $outdir
fi

#binarize input file
./binarize.py $path$trainf $outdir$trainf
./binarize.py $path$testf $outdir$testf

#q3
for sf in $similarity_func
 do
 for k in $kval
  do
  $command $outdir$trainf $outdir$testf $k $sf $outdir$sysf$sf$us$k >$outdir$accf$sf$us$k
 done
done
