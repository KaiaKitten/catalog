apt-get -qqy update
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-pip
pip install werkzeug==0.8.3
pip install flask==0.9
pip install Flask-Login==0.1.3
pip install flask-seasurf
pip install dicttoxml
pip install httplib2
pip install oauth2client
pip install requests
pip install httplib2

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd

