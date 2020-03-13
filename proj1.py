#!/usr/bin/env python3

import sys
import argparse
import string
words = {}
def input_files():
    parser= argparse.ArgumentParser()
    parser.add_argument('firstinput', metavar='firstinput', type=str, help='Enter the first file')
    parser.add_argument('secondinput', metavar='secondinput', type=str, help='Enter the second file')
    args = vars(parser.parse_args())
    firstinput = args['firstinput']
    secondinput = args['secondinput']
    print(firstinput)
    read_input(firstinput)
    print(secondinput)
    read_input(secondinput)
def read_input(input_file):
    with open(input_file, "r") as lines:
        words = lines.read().split()
                
    print(words)

if __name__ == "__main__":
    input_files()
