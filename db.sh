mysql -u root -proot -e "drop schema if exists vcg; create schema if not exists vcg CHARACTER SET utf8 COLLATE utf8_general_ci;"
python manage.py syncdb
python manage.py runserver
