#!/usr/bin/python
from __future__ import with_statement
"""Builds the website from django templates and language files.

Uses the django template system to create static files for the website. This
allows easy inclusion of common content, but removes the need for (e.g.) PHP
includes that don't really do anything dynamic.

You can build the website for all languages, by doing:
$ python build-website.py

This requires the python-django package on debian.
"""

__author__ = "Ximin Luo <infinity0@gmx.com>"
__license__ = "GPL v3"

# more links on django template syntax:
# http://www.djangobook.com/en/beta/chapter04/
# http://docs.djangoproject.com/en/dev/topics/templates/

# this would normally be defined in the settings module, but we've set that to __main__, as above
TEMPLATE_DIRS = ('src',)

OUTPUT_DIR = "../opensukey.org"
WEBSITE_FILES = ["index.html","what.html","articles.html","blog.html","contact.html","donate.html"]
STATIC_DIRS = ["css", "img", "js"]

STRINGS_FILE = "l10n/strings.csv"

###############################################################################

import sys, os, shutil
os.environ['DJANGO_SETTINGS_MODULE'] = '__main__'

import csv
import itertools

from django.template.loader import get_template
from django.template import Context, Template


def load_strings():
	strings = None

	with open(STRINGS_FILE) as fp:
		row_iter = csv.reader(fp)
		langs = row_iter.next()[1:]
		strings = dict((lang, {}) for lang in langs)

		for row in row_iter:
			key = row[0]
			default_value = row[1]
			for lang, value in itertools.izip_longest(langs, row[1:], fillvalue=""):
				strings[lang][key] = value if value.strip() else default_value

	return strings

def build_lang(lang, strings):
	out_dir = os.path.join(OUTPUT_DIR, lang)
	shutil.rmtree(out_dir, ignore_errors=True)
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)
	print >>sys.stderr, "building to %s..." % out_dir

	for fn in WEBSITE_FILES:
		t = get_template("%s.djt" % fn)
		c = Context({"strings": strings})
		with open(os.path.join(out_dir, fn), 'w') as fp:
			print >>fp, t.render(c)

def main(*args):
	shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
	os.mkdir(OUTPUT_DIR)

	STRINGS = load_strings()
	if not args: args = STRINGS.keys()

	for arg in args:
		build_lang(arg, STRINGS[arg])

	for tree in STATIC_DIRS:
		out_dir = os.path.join(OUTPUT_DIR, tree)
		print >>sys.stderr, "copying to %s..." % out_dir
		shutil.copytree(tree, out_dir)

if __name__ == "__main__":
	sys.exit(main(*sys.argv[1:]))

