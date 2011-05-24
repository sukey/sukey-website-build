#!/bin/sh
cd l10n
for i in $(ls *.py); do echo ${i%.py}; done | grep -v __init__

