INSTALL:

    python install.py install

REMOVE:

    python install.py remove

Run Server:

    python manage.py runserver [ip]:[port]

    Example:
        1. python manage.py runserver 0.0.0.0:8080
        2. python manage.py runserver 127.0.0.1:8080

    If you want to run HackSpace server like apache, nginx, Install mod_wsgi.
    Installation Details will be filled in or not.

First administrator account:

    ID : root
    PW : root

Instructions of Admin Functions:

    http://[server ip or name]/admin/
        - Can watch solved problem status.
        - Can search existent users.
        - If you click problem link in problem table,
          you could check who solve clicked the problem.

    http://[server ip or name]/admin/challenge/
        - Can add, modify, delete problem.

    http://[server ip or name]/admin/manage-user/
        - Can add, modify, delete user.

    http://[server ip or name]/admin/add-category/
        - Can add, modify, delete post category.
        - Can watch post in real time.
    
    http://[server ip or name]/admin/server-onoff/
        - Can set access control about register page and challenge panel page.
        - Can set ranking system as table or graph.
    
If error is found, please contact 'wisedier@gmail.com' or 'loup1788@gmail.com'
