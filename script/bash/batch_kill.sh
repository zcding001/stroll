#!/usr/bin/env bash


name=$1

for line in `ps -ef | grep ${name} | grep -v 'grep' | awk '{print $2}'`
do
       echo $line
       kill -9 $line
done
