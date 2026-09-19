# File Integrity Monitor

A python based security compliance tool that detects unauthorised changes to files by comparing cryptographic hashes over time.

## Features

-Create Baseline

*Scans a target folder and generates a SHA256 hash for every file inside it
*Saves the hashes to baseline.json so the baseline survives closing and reopening the program

-Run Integrity Check

*Detects three states for every monitored file:
-Unchanged
-Monified
-Missing
*Also detects new files present in the folder that was not a part of the original baseline

-View Baseline Data

*Displays the currently stored filename and hash for every monitored file

-Exit Option

## What I learned

Structuring a program around a menu loop

Using Python's 'hashlib' module to generate SHA256 hashes

Using Python's 'os' module to read files from a target folder and check whether a file still exists

Using Python's 'json' module to save and load data so it persists between program runs

Understanding the 'global' and variable scope inside functions

Debugging indentation and inverted logic errors by tracing through code step by step

Using .gitignore to exclude generated data files 

Structuring with blank lines to make results easier to read

Handling user input and different menu options

How to run

Python "File Integrity Monitor.py
