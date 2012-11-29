# -*- coding: utf8 -*-
import sys
import getpass
import os
import subprocess

try:
    input = raw_input
except:
    pass

engine=name=username=port=password=''

if len(sys.argv) < 2:
    print "python install.py install"
    print "                  remove"
elif sys.argv[1] == "install":
    if os.path.isfile("./pentarea/dbcon.py"):
        print "already installed..."
        print "remove first.."
        sys.exit(1)

    print "please input DB engine... "
    print "postgresql_psycopg2, mysql, sqlite3, oracle"
    engine = input("engine: ")
    if engine not in ["postgresql_psycopg2", "mysql", "sqlite3", "oracle"]:
        print "Wrong engine..."
        sys.exit(1)
    if engine == "sqlite3":
        name = input("db file name: ")
    if engine != "sqlite3":
        name = input("db name: ")
        username = input("db username: ")
        password=getpass.getpass("db password: ")
    host = input("host: ")
    if host not in ["localhost", "127.0.0.1"]:
        port = input("port: ")

    fp=open("./pentarea/dbcon.py", "w")
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
        os.remove("./pentarea/dbcon.py")
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
    print "\nCreating superuser..."
    os.system("python manage.py createsuperuser")
    print "\n'python manage.py runserver IP:PORT' makes you can access the page.."
elif sys.argv[1] == "remove":
    from pentarea.settings import INSTALLED_APPS
    if os.path.isfile("./pentarea/dbcon.py"):
        import pentarea.dbcon
        if(pentarea.dbcon.engine == "sqlite3"):
            os.remove(pentarea.dbcon.name)
            sys.exit(0)
        else:
            for app in INSTALLED_APPS:
                if app.find("django.contrib.") is -1:
                    os.system("python manage.py sqlclear "+app+"| python manage.py dbshell")
            for app in INSTALLED_APPS:
                if app.find("django.contrib.") is not -1:
                    app=app.replace("django.contrib.", "")
                    os.system("python manage.py sqlclear "+app+"| python manage.py dbshell")
    os.remove("./pentarea/dbcon.py")
    os.remove("./pentarea/dbcon.pyc")
    print "Done!"
