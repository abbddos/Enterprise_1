#!/usr/bin/env python3

import sys
import site

site.addsitedir('/var/www/lib/lib/python3.6/site-packages')

sys.path.insert(0, '/var/www/enterprise')

from app import app as application