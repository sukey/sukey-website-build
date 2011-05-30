#!/usr/bin/python
"""Builds the website from django templates and language files.

Uses the django template system to create static files for the website. This
allows easy inclusion of common content, but removes the need for (e.g.) PHP
includes that don't really do anything dynamic.

You can build the website for all languages, by doing:
$ python build-website.py $(sh all-langs.sh)

This requires the python-django package on debian.
"""

__author__ = "Ximin Luo <infinity0@gmx.com>"
__license__ = "GPL v3"

# more links on django template syntax:
# http://www.djangobook.com/en/beta/chapter04/
# http://docs.djangoproject.com/en/dev/topics/templates/

import sys, os, shutil
os.environ['DJANGO_SETTINGS_MODULE'] = '__main__'

# this would normally be defined in the settings module, but we've set that to __main__, as above
TEMPLATE_DIRS = ('src',)

OUTPUT_DIR = "opensukey.org"
WEBSITE_FILES = ["index.html","what.html","articles.html","blog.html","contact.html","donate.html"]

from django.template.loader import get_template
from django.template import Context, Template

def get_strings(lang):
	imported = __import__("l10n", globals(), locals(), [lang])
	lang_module = getattr(imported, lang)
	return lang_module.strings

def build_lang(lang):
	out_dir = os.path.join(OUTPUT_DIR, lang)
	shutil.rmtree(out_dir, ignore_errors=True)
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)
	print >>sys.stderr, "building to %s..." % out_dir

	for fn in WEBSITE_FILES:
		t = get_template("%s.djt" % fn)
		c = Context({"strings": get_strings(lang)})   # makes lang_module.strings accessible as variable "strings" within the template
		with open(os.path.join(out_dir, fn), 'w') as fp:
			print >>fp, t.render(c)

def main(*args):
	if not os.path.exists(OUTPUT_DIR):
		os.mkdir(OUTPUT_DIR)
	for arg in args:
		build_lang(arg)
if __name__ == "__main__":
	sys.exit(main(*sys.argv[1:]))

