#!/bin/bash
if [[ "$OSTYPE" == "darwin"* ]]  && [[ $LOCAL == 1 ]] && [[ $USER == "vagrant" ]]; then
  source ~/.bash_profile
  conda activate sih
  chmod +x build/app.py
  cd build
  ./app.py
  cd ..

elif [[ "$OSTYPE" == "linux-gnu"* ]]  && [[ $PRO == 1 ]]; then
 	python3 build/app.py 
fi
