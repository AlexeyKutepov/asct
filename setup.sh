#!/bin/bash
echo $0: Starting...

apt-get -y install virtualenv
apt-get -y install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev python3-dev

virtualenv asct_env --python=/usr/bin/python3
source asct_env/bin/activate

pip install -r requiments.txt

python3 manage.py makemigrations
python3 manage.py migrate

echo $0: Finished!