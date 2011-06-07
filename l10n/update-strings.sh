#!/bin/sh
cd "$(dirname "$(readlink -f "$0")")"
wget -nv -O strings.csv "https://spreadsheets.google.com/spreadsheet/pub?hl=en_US&hl=en_US&key=0AtPlyIZQV2PIdFNlWGlNd0tYT3F0RllIN1VtUkdBZHc&output=csv"
if git diff strings.csv; then echo "no changes to commit"; fi
