#!/usr/bin/env python3
import sys
import string
import math
import os
import numpy as np
def parse(doc):
    category = {}
    logprior = {}
    word_list = {}
    N_c = {}
    words = {}
    input_files = open(doc, "r").read().split("\n")    
    N_docs = len(input_files) - 1
    for lines in input_files:
        split_lines = lines.split()
        if split_lines:
            pathname = split_lines[0]
            word_list = np.append(word_list, get_words(pathname))
            category[pathname] = split_lines[1] 
    for cat in category.values():
        if (cat in N_c):
            N_c[cat] += 1
        else:
            N_c[cat] = 1
    for keys in N_c:
        N_c[keys] = float(N_c[keys])
        logprior[keys] = math.log10(N_c[keys] / N_docs)
    print(word_list)
def get_words(pathname):
    words = []
    file_path = os.path.relpath(pathname)
    with open(file_path, "r") as f:
        words = f.read().split()
    return(words)
if __name__ == "__main__":
    training_doc = input("Enter the list of training documents: ")
    #unlabeled_doc = input("Enter the list of untrained documents: ")
    parse(training_doc)

