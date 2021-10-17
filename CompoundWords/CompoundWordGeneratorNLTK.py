#This script is sample to generate single word from compound words in a given corpus so it retains the meaning while training and inference.
# We use NLTK
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
import tkinter as tk
from pprint import pprint
import spacy
import pandas as pd
nlp = spacy.load('en')

#some sample sentence input
sentence = "There were no date nut bread or broasted chicken so we called customer service"
sentence = sentence.lower()
#gen tokens/tokenize
tokens = nltk.word_tokenize(sentence)
#get pos tags
tagged = nltk.pos_tag(tokens)
#chunk and get entities
entities = nltk.chunk.ne_chunk(tagged)

sent = []
new_word = ''
for tok in token_sp:
  word = tok.string.strip()
  if len(new_word) != 0 : 
    if tok.dep_ == 'pobj':
      sent.append(new_word)
      new_word = word
    elif tok.dep_ == 'amod' or tok.dep_ == 'nummod':
      if last_tok.dep_ == 'amod' or last_tok.dep_ == 'nummod':
        sent.append(new_word)
        new_word = word
      else:
        new_word = new_word + '-' + word
    elif tok.dep_ == 'ccomp':
      sent.append(new_word)
      new_word = ''
      sent.append(word)
    elif tok.pos_ == 'VERB'  :
      new_word = new_word + '-' + word
    elif tok.dep_ == 'compound':
      new_word = new_word + '-' + word
      if last_tok.pos_ == 'ADJ' : 
        sent.append(new_word)
        new_word = ''
      else:
        new_word = new_word + '-' + word
    else:
      new_word = new_word + '_' + word
      sent.append(new_word)
      new_word = ''
  else:
    if tok.dep_ == 'amod' or tok.dep_ == 'nummod': 
      new_word = word
    elif tok.dep_ == 'ccomp': 
      if last_tok.pos_== 'NOUN':
        new_word = last_tok.string.strip() + '-' + word
        sent.pop()
        sent.append(new_word)
        new_word = ''
      else: sent.append(word)
    elif tok.dep_ == 'compound':
      new_word = word
    else:
      sent.append(word)
      new_word = ''
  last_tok = tok
sentence = ' '.join(sent)


#sample output = there were no date-nut-nut_bread or broasted_chicken so we called customer_service
