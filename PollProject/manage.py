#!/usr/bin/env python
import os, sys
from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    if "deploy" in sys.argv and os.path.isfile('initial_data.yaml'):
        said = raw_input("Are you sure you want to deploy with initial_data? (YES to continue):")
        if said != "YES":
            print "goodbye."
            sys.exit(0)
    execute_manager(settings)
