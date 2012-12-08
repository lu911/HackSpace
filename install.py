# -*- coding: utf8 -*-
import sys
import getpass
import os
import subprocess

def CommandInfo():
    print "python install.py install - install Pentarea"
    print "                  remove - delete Database setting and all data about hackspace"
    print "                  resetting - setting database again (not delete tables and data)"
    print "                  createsuperuser - make administrator"

def DBSetting():
    engine=name=username=port=password=''
    print "please check DB character set first!, Django DB follow your DB character set"
    print "input DB engine... "
    print "postgresql_psycopg2, mysql, sqlite3, oracle (blank = sqlite3)"
    engine = input("engine: ")
    if engine not in ["postgresql_psycopg2", "mysql", "sqlite3", "oracle", '']:
        print "Wrong engine..."
        sys.exit(1)
    if engine == '':
        engine = "sqlite3"
    if engine == "sqlite3":
        name = input("db file name: ")
    else:
        name = input("db name: ")
        username = input("db username: ")
        password=getpass.getpass("db password: ")
    host = input("host: ")
    if host not in ["localhost", "127.0.0.1"]:
        port = input("port: ")

    fp=open("./hackspace/dbcon.py", "w")
    fp.write("engine= '"+engine+"'\n")
    fp.write("name= '"+name+"'\n")
    fp.write("username= '"+username+"'\n")
    fp.write("password= '"+password+"'\n")
    fp.write("host= '"+host+"'\n")
    fp.write("port= '"+port+"'\n")
    fp.close()
    manage=subprocess.Popen(['python', 'manage.py',  'syncdb'], stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    manage.stdin.write("no\n")
    error = manage.stderr.readlines()
    if len(error) != 0:
        os.remove("./hackspace/dbcon.py")
        print "Error! please check your setting..."
        print "Do you want to see python error message??(Y/N)"
        decision = input()
        if decision == "Y":
            for line in error:
                sys.stdout.write(line)
        sys.exit(1)
    for line in manage.stdout.readlines():
        if line.find("yes/no") == -1:
            sys.stdout.write(line)
 
def RemoveDBSetting():
    os.remove("./hackspace/dbcon.py")
    os.remove("./hackspace/dbcon.pyc")

def RemoveDBData():
    from hackspace.settings import INSTALLED_APPS
    if os.path.isfile("./hackspace/dbcon.py"):
        import hackspace.dbcon
        if(hackspace.dbcon.engine == "sqlite3"):
            os.remove(hackspace.dbcon.name)
        else:
            for app in INSTALLED_APPS:
                if app.find("django.contrib.") is -1:
                    os.system("python manage.py sqlclear "+app+"| python manage.py dbshell")
            for app in INSTALLED_APPS:
                if app.find("django.contrib.") is not -1:
                    app=app.replace("django.contrib.", "")
                    os.system("python manage.py sqlclear "+app+"| python manage.py dbshell")
 
def CreateSuperuser():
    print "Creating superuser..."
    os.system("python manage.py createsuperuser")
 
try:
    input = raw_input
except:
    pass

if len(sys.argv) < 2:
    CommandInfo()
elif sys.argv[1] == "install":
    if os.path.isfile("./hackspace/dbcon.py"):
        print "already installed..."
        sys.exit(1)
    DBSetting()
    CreateSuperuser()
    print "\n'python manage.py runserver IP:PORT' makes you can access the page.."
elif sys.argv[1] == "remove":
    print "This command remove all your DB data.."
    print "Really?(Y/n)"
    decision = input()
    if decision == "Y":
        RemoveDBData()
        RemoveDBSetting()
        print "Done!"
elif sys.argv[1] == "resetting":
    DBSetting()
elif sys.argv[1] == "createsuperuser":
    CreateSuperuser()
else:
    CommandInfo()
