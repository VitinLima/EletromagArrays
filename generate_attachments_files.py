#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 21:49:21 2023

@author: vitinho
"""

import sys
import os

def write_entry(f, filepath, filename, language):
    f.write("\n\\newpage")
    f.write("\n\\lstinputlisting[language=")
    f.write(language)
    f.write(", caption=")
    f.write(filename.replace("_", "\\_"))
    f.write(", basicstyle=\\ttfamily\scriptsize]")
    f.write("{" + os.path.join("attachments", filepath, filename) + "}")

def process_file(f, filepath, file):
    filename = os.path.basename(file)
    if filename.endswith(".m"):
        language = "Octave"
    elif filename.endswith(".py"):
        language = "Python"
    else:
        return
    write_entry(f, filepath, filename, language)

def process_folder(f, curfolder, depth=0):
    if depth==0:
        f.write("\n\n\\section{" + curfolder + "}")
    folders = [os.path.join(curfolder, folder) \
               for folder in os.listdir(curfolder) \
                   if os.path.isdir(os.path.join(curfolder, folder))]
    for folder in folders:
        process_folder(f, folder, depth+1)
    
    files = [os.path.join(curfolder, folder) \
               for folder in os.listdir(curfolder) \
                   if os.path.isfile(os.path.join(curfolder, folder))]
    
    for file in files:
        process_file(f, curfolder, file)

with open("attachments.tex", "w", encoding="utf-8") as f:
    f.write("\\printindex")
    f.write("\n\\lstlistoflistings\n")
    f.write("\n% \\input{attachments/software-description}")
    
    process_file(f, '', __file__)
    
    folders = [folder \
               for folder in os.listdir(os.getcwd()) \
                   if os.path.isdir(folder)]
    for folder in folders:
        process_folder(f, folder)
    
    f.write("\n\n\\newpage")