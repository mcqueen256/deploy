#!/usr/bin/python3

import os
import sys

def error(message):
    print(message)
    exit(1)

def deploy(args):
    '''
    Create a new web server with given name.
    Usage: webserver deploy APPLICATION_NAME
    '''
    print("args", args)
    if len(args) != 1:
        error('invalid arguments.\nusage: ' + sys.argv[0] + ' deploy APPLICATION_NAME')
    # get the application name
    app_name = args[0]
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




def main():
    # List of functions
    operations = {
        'deploy': deploy,
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

