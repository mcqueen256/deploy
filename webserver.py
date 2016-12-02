#!/usr/bin/python3

import os
import sys
import shutil
import random
import string
import subprocess

def error(message):
    print(message)
    exit(1)

def deploy(args):
    '''
    Create a new web server with given name.
    Usage: webserver deploy APPLICATION_NAME APPLICATION_DOMAIN
    '''
    if len(args) < 2:
        error('invalid arguments.\nusage: ' + sys.argv[0] + ' deploy APPLICATION_NAME APPLICATION_DOMAIN [options ...]')
    # get the application name
    app_name = args[0]
    server_name = args[1]
    # check that there are only numbers, letters and underscores
    def check_valid_char(char):
        result = False
        if ('a' <= char and char <= 'z') or \
           ('A' <= char and char <= 'Z') or \
           (char == '_') or \
           (char == '-') or \
           (char == '.'):
               result = True
        return result
    for character in app_name:
        if not check_valid_char(character):
            error('invalid name ' + app_name + ', must only contain numbers, letters, understors, minus signs or periods.')
    # check the application does not already exist
    if app_name in os.listdir('/var/www'):
        error('application {} already exists in /var/www/'.format(app_name))
    # settings for the server
    settings = {
        'server_name':server_name,
        'admin_email':'admin@nicbuckeridge.com',
        'app_name': app_name,
        'user': 'nicholas',
        'group': 'nicholas',
        'threads': '5'
    }
    for arg in args[2:]:
        if len(arg.split('=')) > 2:
            error('option \'{}\' is not valid'.format())
        key, value = tuple(arg.split("="))
        if key not in settings.keys():
            error('invalid option \'{}\''.format(key))
    # create application
    script_path = os.path.dirname(os.path.realpath(__file__))
    resource_path = script_path + '/resources/'
    print('resource path', resource_path)
    # create parent directory
    os.mkdir('/var/www/{}'.format(app_name))
    # create wsgi app
    with open(resource_path + 'app.wsgi', 'r') as fin:
        with open('/var/www/{app_name}/{app_name}.wsgi'.format(app_name=app_name), 'w') as fout:
            fout.write(fin.read().format(app_name=app_name, secret_key="".join([random.choice(string.ascii_letters+string.digits) for x in range(64)])))
    # create application directory
    os.mkdir('/var/www/{app_name}/{app_name}'.format(app_name=app_name))
    # create default directories
    os.mkdir('/var/www/{app_name}/{app_name}/static'.format(app_name=app_name))
    os.mkdir('/var/www/{app_name}/{app_name}/templates'.format(app_name=app_name))
    # Create the init file
    shutil.copy(resource_path + '__init__.py', '/var/www/{app_name}/{app_name}/__init__.py'.format(app_name=app_name))
    # create virtula evironment
    subprocess.run(['pyvenv', '/var/www/{app_name}/{app_name}/venv'.format(app_name=app_name)])
    # setup venv
    subprocess.run(['bash', script_path + '/flask_setup.bash', '/var/www/{app_name}/{app_name}/venv/bin/activate'.format(app_name=app_name)])
    shutil.copy(resource_path + 'activate_this.py', '/var/www/{app_name}/{app_name}/venv/bin/'.format(app_name=app_name))
    # create wsgi mapping
    with open(resource_path + 'app.conf', 'r') as fin:
        with open('/etc/apache2/sites-available/{app_name}.conf'.format(app_name=app_name), 'w') as fout:
            fout.write(fin.read().format(**settings))
    # enable in apache2
    subprocess.run(['a2ensite', '{app_name}.conf'.format(app_name=app_name)])
    #subprocess.run(['ln', '-s', '/etc/apache2/sites-enabled/{app_name}.conf'.format(app_name=app_name), '/etc/apache2/sites-available/{app_name}.conf'.format(app_name=app_name)])
    # inform the user of the possibility of a server restart
    print("Apache2 must be restarted with 'sudo service apache2 restart'")

def delete(args):
    '''
    Deletes a flask application form the disk.
    Usage: webserver delete APPLICTION_NAME
    '''
    if len(args) != 1:
        error('invalid arguments.\nusage: ' + sys.argv[0] + ' delete APPLICATION_NAME')
    # get the application name
    app_name = args[0]
    if app_name not in os.listdir('/var/www'):
        error('application {} does not exist'.format(app_name))
    print('warning: this will remove the application perminately from the disk.')
    i = input('are you sure? (y/n)')
    if i == 'y':
        print('deleting {}'.format(app_name))
        os.remove('/etc/apache2/sites-available/{app_name}.conf'.format(app_name=app_name))
        os.remove('/etc/apache2/sites-enabled/{app_name}.conf'.format(app_name=app_name))
        shutil.rmtree('/var/www/{}'.format(app_name))
    # inform the user of the possibility of a server restart
    print("Apache2 must be restarted with 'sudo service apache2 restart'")
    exit(0)



def main():
    # List of functions
    operations = {
        'deploy': deploy,
        'delete': delete,
    }

    # run command
    if len(sys.argv) > 1 and sys.argv[1] in operations.keys():
        operations[sys.argv[1]](sys.argv[2:])
    else:
        print("operation not selected. Operations are:")
        for key in operations.keys():
            print("  " + key)

if __name__ == '__main__':
    main()

