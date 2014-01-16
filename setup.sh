#!/bin/bash

echo "==========================="
echo "Virtual Sanity - InstaGate"
echo "==========================="
echo "Please INSTALL PostgreSQL and Psycopg "
echo "PostgreSQL installation on Mac OS X : http://postgresapp.com/"
echo "Psycopg installation : http://initd.org/psycopg/install/"
echo "=================================================================="
echo " "
echo "If you have these already installed, press Enter (CTRL+C to abort)"
read input_variable
sudo pip install django-debug-toolbar
cd python-instagram-master
sudo python ./setup.py install
