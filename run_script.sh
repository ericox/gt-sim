#!/bin/bash
set -x
for i in `seq 1 100`;
do
  n=4
  first='p'
  second='c'
  python -m gtsim.sequence -n $n -f $first -s $second -b 10 -r True >> seq_${n}_${first}_${second}_b10.csv 2>&1
done
set +x
