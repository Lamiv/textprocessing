#This script is sample to generate single word from compound words in a given corpus so it retains the meaning while training and inference.
# We use Spacy
import spacy
nlp = spacy.load('en')

def convert_compound(sentence):
  tokens = nlp(sentence)
  #print('---tokens---')
  #for tok in tokens:
  #  print(tok.i, tok, "[", tok.dep_, "]", "[", tok.pos_, "]", '[', tok.tag_, ']', '[', tok.ent_type_,']')
  last_tok = tokens[0]
  #print('--sentence--')
  sent = []
  new_word =''
  sep = '-'
  clr = ''
  for tok in tokens:
    word = tok.string.strip()
    clr = ''
    if len(new_word)!=0:
      clr = 'X'
      if tok.dep_== 'dobj':
        if tok.tag_ =='NNS' or last_tok.dep_=='compound' :
          sep = '_'
        else: sep = ' '
      elif tok.dep_=='pobj'  :
        if last_tok.dep_=='compound': sep = '_'
        elif tok.pos_=='VERB' and last_tok.dep_=='amod' and last_tok.pos_=='PROPN':
          sep = '-'
        else: sep = ' '
      elif tok.dep_ == 'amod' or tok.dep_ == 'nummod':
        sep = '-'
        if last_tok.dep_ == 'amod' or last_tok.dep_ == 'nummod':
          sep = ' '
      elif tok.dep_=='compound':
        sep = '-'
        if last_tok.dep_=='compound':
          clr = ''
      elif tok.dep_ == 'prep' :
        sep = ' '
      elif tok.dep_ =='conj' and tok.pos_=='VERB' and last_tok.dep_=='amod' and last_tok.pos_=='ADJ':
        sep = '-'
      else:
        sep = '_'
      new_word = new_word + sep + word
      if clr=='X':
        word = new_word
        new_word = ''
    else:
      if tok.dep_ == 'amod' or tok.dep_ == 'nummod' or tok.dep_ == 'npadvmod':
        new_word = word  
      elif tok.pos_ == 'VERB' and (tok.dep_=='ROOT' or tok.dep_=='ccomp') and last_tok.dep_=='nsubj' and last_tok.pos_=='NOUN':
        new_word = sent.pop()
        if '_' in new_word : word = new_word + ' ' + word
        else: word = new_word + '-' + word  
        new_word = ''   
      elif tok.dep_ == 'compound' :
        if last_tok.dep_=='amod': 
          new_word = sent.pop()
          if '_' in new_word : word = new_word + ' ' + word
          else: word = new_word + '-' + word 
          new_word = ''
        else : new_word = word
    last_tok = tok    
    if new_word=='': sent.append(word)
    
  if new_word!= '': sent.append(new_word)
  return ' '.join(sent)

#sample input
sentence = 'he asked me to french fry the potatoes or deep fry the potatoes. then he said a hand held mobile radiotelephone for use in an area divided into small sections, each with its own short range transmitter/receiver'
sentence = convert_compound(sentence)
print(sentence)

#sample output:  he asked me to french-fry the potatoes or deep-fry the potatoes . then he said a hand-held mobile radiotelephone for use in an area divided into small sections , each with its own short-range transmitter / receiver
