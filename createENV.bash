#!/bin/bash
#Finds Python, checks or installs .env, installs reqs.txt
#Author: CoryNull(Cory Noll Crimmins-Golden)<cory190@live.com>

pyInt=false;
for pyT in "python" "python3" "python3.8"; do
  if type "$pyT" &> /dev/null; then
    echo "Found $pyT"
    pyInt=$pyT;
    break;
  fi
done

if [ ! type "$pyInt" &> /dev/null ]; then
  echo "Python not found"
else
  if [ ! -d ".env" ]; then
    $pyInt -m venv .env;
  fi

  if [ -d ".env" ]; then
    source .env/bin/activate; 
    pip install -r reqs.txt;
  fi
fi

