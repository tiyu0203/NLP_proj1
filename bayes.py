#!/usr/bin/env python3
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import *
from nltk.stem import PorterStemmer
import math
import string

stemmer = SnowballStemmer('english')
tokenizer = RegexpTokenizer(r'\w+')
#all the dictionaryies used 
tokenized = dict() #dictionary to store all the tokenized words and the frequencies
categories = dict() #dictionary to store all the categories
cat_words = dict() #dictionary that stores all the different words in each category and the frequency 
N_docs = "global" #total number of documents
set_categories = [] 
stemstem = PorterStemmer() #the stemmer
def training(training_doc):
    
    #open and reads in the training file
    input_files = open(training_doc, "r")
    input_files_lines = input_files.read().splitlines()

    #parses through the file 
    for line in input_files_lines:
        split_lines = line.split()
        #splits up the line to get the filepath and the category of each file
        cats = split_lines[1] 
        #stores the frequency of each category in a dictionary
        frequency(cats, categories)
        
        train_file = tokenize(split_lines[0])

        count = 1
        for tokens in train_file:
            #finds the stem of the tokens
            tokens = stemstem.stem(tokens)
            if tokens in list(string.punctuation):
                continue
            #creates a dictionary that specifies the category, token, and frequency of the token in the category
            frequency((cats, tokens),cat_words) 
            count += 1
        if cats in tokenized:
            tokenized[cats] += count
        else:
            tokenized[cats] = count
    #closes the training file
    input_files.close()
    
def testing(testing_doc):
    #opens and readsd in the testing file and parses through to get the pathname
    input_files = open(testing_doc, "r")
    input_files_lines = input_files.read().splitlines()

    #sums the amount of each category to get the total amount of documents in the set
    N_docs = sum(categories.values())
    #gets all of the categories
    set_categories = categories.keys()

    #prompts the user to enter the output file and creates/overwrites it
    output_file_name = input("Enter name of output file: ")
    output_file = open(output_file_name, "w")
    
    #parses through the files and tokenizes
    for lines in input_files_lines:
        test_file = tokenize(lines)
        
        #creates a temporary dictionary 
        tmp = dict()

        #finds the stem of each token
        for tmp_token in test_file:
            tmp_token = stemstem.stem(tmp_token)

            if tmp_token in list(string.punctuation):
                continue

            frequency(tmp_token, tmp)
        #finds the length of all temporary dictionary, which should be the amount of vocab
        V = len(tmp)
        #creates a dictionary for the category probabability 
        category_probability = dict()
        
        #defining an arbitrary alpha for smoothing
        k = 0.005
        
        #finds the stats for each category
        for cat in set_categories:
            total_category_prob = 0
            #calculates the probability of how many categories appear in each set
            prior = categories[cat] / N_docs
            mag = tokenized[cat] + k * V

            #calculates the loglikelihood and logsprior
            for word, count in tmp.items():
                if(cat, word) in cat_words:
                    word_count_in_category = cat_words[(cat, word)] + k
                else:
                    word_count_in_category = k 

    
                total_category_prob += count*math.log10(word_count_in_category / mag)

            category_probability[cat] = total_category_prob + math.log10(prior)
            
        #determines the most likely category the file would be
        result = max(category_probability, key = category_probability.get)

        #writes the file and result into the output file
        output_file.write(lines + ' ' + result + '\n')

    #closes the files
    input_files.close()
    output_file.close()

    return

#determines the frequency of how much is in each list
def frequency(item, the_list):
    if (item in the_list):
        the_list[item] += 1
    else:
        the_list[item] = 1

#reads the pathname and opens the file and tokenizes the words in the files
def tokenize(pathname):
    words = [stemmer.stem(w) for w in tokenizer.tokenize(open(pathname, "r")    .read().lower())]
    return words


if __name__ == "__main__":
    training_doc = input("Enter the list of training documents: ")
    training(training_doc)
    testing_doc = input("Enter the list of test documents: ")
    testing(testing_doc) 
