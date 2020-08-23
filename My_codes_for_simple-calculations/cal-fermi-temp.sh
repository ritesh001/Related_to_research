#!/bin/bash
a=`grep "energy(sigma->0)" OUTCAR | tail -1 | awk '{printf "%12.8f\n", $4}'`
b=`grep "energy(sigma->0)" OUTCAR | tail -1 | awk '{printf "%12.8f\n", $7}'`
c=`echo "$a - $b" | bc -l`
d=`echo "$c * 1000" | bc -l`
n=`grep NIONS OUTCAR | awk '{printf "%.2d\n", $12}'`
e=`echo "$d / $n" | bc -l`
echo $e
