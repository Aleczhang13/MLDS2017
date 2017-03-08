#!/usr/bin/python3
import os
import re
import spacy
import string
import sys
from nltk import Tree

# English language parser
en_nlp = spacy.load('en')

# Generating dependency tree
def to_nltk_tree(node):
  if node.n_lefts + node.n_rights > 0:
    return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
  else:
    return node.orth_

# Check whether given sentence is a valid English sentence
def valid(sentence):
  if len(sentence.split()) < 3:
    return False
  for word in sentence.split():
    if not all(c in string.printable for c in word):
      return False
    has_digit = any(c in string.digits for c in word)
    has_alpha = any(c in string.ascii_letters for c in word)
    if has_digit and has_alpha:
      return False
    if has_alpha:
      if not any(c in ['a','e','i','o','u','y'] for c in word):
        return False      
  return True
  
# Parse the given content into dependency trees
def Parse(f,of):
  content = re.sub('\n|\r', ' ', ''.join( i for i in f ))
  content = re.split('[,.!?;]+', content)
  for sentence in content:
    sent = re.sub(r'[^[a-zA-Z0-9 \']]*', '', re.sub(r' +', ' ', sentence))
    if not valid(sent): continue
    for sent in en_nlp(sent.lower()).sents:
      tree = to_nltk_tree(sent.root)
      if tree == None: continue
      if type(tree) != str:
        sys.stdout = open('tmp','w')
        tree.pprint()
        sys.stdout.flush()
        tf = open('tmp','r')
        of.write(' '.join(line.strip() for line in tf) + '\n' )

sys.stderr.write('start parsing...\n')
with open('training_list','r') as file_list:
  for file_name in file_list:
    with open(file_name[:-1],'r',encoding="utf-8",errors='ignore') as f:
      sys.stderr.write('start parsing file ' + file_name[:-1] + '\n')
      with open("Training_Data/"+file_name[21:-5]+".txt",'w') as of:
        Parse(f,of)
      sys.stderr.write('finished parsing file ' + file_name[:-1] + '\n')
os.remove('tmp')
