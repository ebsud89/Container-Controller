[Usage]

pip3 install setuptools

pip3 install pyinstaller

pyinstaller -F -w main.py

cp dist/main /usr/local/bin/container_controller

echo "export $PATH:/usr/local/bin:" >> ~/.bashrc
echo "alias dcc='container_controller'" >> ~/.bashrc

source ~/.bashrc
