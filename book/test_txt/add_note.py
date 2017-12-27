#!/usr/bin/env python3

import os
import time
import subprocess

# --------------------------------------------------------
files_dir = "/"
combined_file = ""
# ---------------------------------------------------------
notes = []

if not os.path.exists(combined_file):
    subprocess.Popen(["touch", combined_file])

def read_file(file):
    with open(file) as note:
        return note.read()

def append_file(combined_file, text):
    with open(combined_file, "a") as notes:
        notes.write(text)

for root, dirs, files in os.walk(files_dir):
    for name in files:
        subject = root+"/"+name
        cr_date_text = time.ctime(os.path.getmtime(subject))
        cr_date_n = os.stat(subject).st_mtime
        notes.append((cr_date_n, cr_date_text, subject))

notes.sort(key=lambda x: x[0])

for note in notes:
    text = note[1]+"\n"+read_file(note[2])+"\n"+"-"*10+"\n"
    append_file(combined_file, text)

