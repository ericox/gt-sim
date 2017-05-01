#!/bin/bash
set -x
for i in `seq 1 100`;
do
  n=15
  first='p'
  second='c'
  python -m gtsim.sequence -n $n -f $first -s $second -b 2 -r True >> seq_${n}_${first}_${second}.csv 2>&1
done
set +x
