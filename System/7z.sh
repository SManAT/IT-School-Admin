#!/bin/bash
echo "Using Maximum Compression"
if [ -z "$1" ] && [ -z "$2" ]
then
  echo "Syntax: sh 7z.sh Name Dir"
else
  7z a -t7z -m0=lzma -mx=9 -mfb=64 -md=32m -ms=on $1.7z $2
fi