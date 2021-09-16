#!/usr/bin/env bash
virtual="venv"
echo -e "\n++++++++++STATUS++++++++++++" 
echo -e "Building the virtual environment....."
# created the virtual environment directory
python3 -m venv $virtual
echo -e "\nVirtual Environment Created!!!"
echo -e "\n**** THE FOLLOW COMMANDS BELOW DOES TWO THINGS****"
echo "1> It activates your python virtual environment"
echo "2> It installs requirements dependencies and assists in creating your project"
echo -e "\nREMINDER: to deactivate from your virtual environment, use: "
echo -e "deactivate\n"
echo -e "\nPlease make sure current working dir is project directory ....\n"
echo -e "\nInstalling requirements dependencies ....\n"
source $virtual/bin/activate
# Install django inside virtual environment
python3 -m pip install -r requirements.txt
# Verify if Django is installed
echo -e "Django Version: "
python3 -m django --version
# Config local env settings
export DJANGO_SETTINGS_MODULE=project.settings.pro
python3 manage.py check
python3 manage.py makemigrations
python3 manage.py makemigrations monopoly
python3 manage.py migrate
python3 manage.py collectstatic --noinput
python3 manage.py runserver 0.0.0.0:8000