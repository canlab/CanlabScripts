#!/bin/bash

#This is a script to clean trailing NaNs off of CSV-type tables that have a schema
#with one line fewer than the number of fields. It was written for Brianna Robustelli
#by Dan Weflen on 7/10/16.

#This script takes one file to modify. To run this several times, use 'find' and 'parallel'.
file="$@"
#First, we get the number of fields in the first line, which represents the schema.
n=`awk -F',' '{print NF}' "$file" | head -n 1`
#Cut to the number of lines in the schema, store the result in "filename-temp.txt"
cut -d ',' -f 1-$n "$file" > "${file}-temp.txt"
#Replace the current file with "filename-temp.txt"
mv "${file}-temp.txt" "$file"

