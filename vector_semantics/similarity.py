import gensim.downloader
import pandas as pd
import numpy as np
from sys import exit

def cos_vectors(word_vectors, word1, word2):
      vec1 = word_vectors[word1]
      vec2 = word_vectors[word2]
      return np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))

def generate_similarity_index(file_name, type_):
  glove_vectors_wiki = gensim.downloader.load('glove-wiki-gigaword-50')
  glove_vectors_twitter = gensim.downloader.load('glove-twitter-50')  
  if(type=='xlsx'):
    data = pd.read_excel(file_name)
  elif(type=='csv'):
    data = pd.read_csv(file_name)
  else:
    exit("Wrong File Format")
  
  value_pairs1 = []
  value_pairs2 = []
  for i in range(len(data)):
      word1 = data.iloc[i]['words1'].split()[0].lower()
      word2 = data.iloc[i]['words2'].split()[0].lower()
      print(word1, word2)
      try:
          val1 = cos_vectors(glove_vectors_wiki, word1, word2)
      except:
          val1 = -2
      try:
          val2 = cos_vectors(glove_vectors_twitter, word1, word2)
      except:
          val2 = -2
          
  value_pairs1.append(val1)
  value_pairs2.append(val2)
  data['Glove-50-Wiki Measure'] = value_pairs1
  data['Glove-50-Twitter Measure'] = value_pairs2
  if(type=='xlsx'):
    data.to_excel(file_name)
  else:
    data.to_csv(file_name)
