#!/bin/bash
#Finds Python, checks or installs .env, installs reqs.txt
#Author: CoryNull(Cory Noll Crimmins-Golden)<cory190@live.com>

py=false;
for pyT in ["python", "python3", "python3.8"]; do
  if [ ! command -v $pyT &> /dev/null ]; then
    py=$pyT;
  fi
done

if [ py == false ]; then
  echo "Python not found"
else
  if [ ! -d ".env" ]; then
    py -m venv .env;
  fi

  if [ -d ".env" ]; then
    source .env/bin/activate; 
    pip install -r reqs.txt;
  fi
fi

