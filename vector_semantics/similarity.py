import gensim.downloader
import pandas as pd
import numpy as np
import nltk
import argparse
from nltk.corpus import wordnet
from nltk.corpus import wordnet_ic

def take_input():
  parser = argparse.ArgumentParser(description='Add Similarity Measure to Word Pairs. \n \
                                   Besides WordNet Measures, you can choose from the following measures: \n \
                                   i "fasttext-wiki-news-subwords-300" \n \
                                   ii "conceptnet-numberbatch-17-06-300" \n \
                                   iii "word2vec-google-news-300" \n iv "glove-wiki-gigaword-300" \n v "glove-twitter-200"')
  parser.add_argument('-f')
  parser.add_argument('-v', default="word2vec-google-news-300")
  args = parser.parse_args()
  return args

def generate_similarity_wordnet(file):
  data = pd.read_csv(file)
  brown_ic = wordnet_ic.ic('ic-brown.dat')
  min_length_val = []
  max_depth_val =  []
  info_content = []
  for i in range(len(data)):
    word1 = data.loc[i, 'Word1']
    word2 = data.loc[i, 'Word2']
    synsets1 = wordnet.synsets(word1)
    synsets2 = wordnet.synsets(word2)
    min_distance = 1e10
    max_depth = -1
    max_res_sim = 0
    for synseti in synsets1:
      for synsetj in synsets2:
        dist = synseti.shortest_path_distance(synsetj)
        if(dist!=None and dist<min_distance):
          min_distance = dist
        subsumers = synseti.lowest_common_hypernyms(synsetj)
        for subsumer in subsumers:
            depth = subsumer.max_depth()
            if(depth>max_depth):
              max_depth = depth
              ls_subsumer = subsumer
              try:
                  res_sim = synseti.res_similarity(synsetj, brown_ic)
                  if(res_sim>max_res_sim):
                      max_res_sim = res_sim
              except:
                  pass
    min_length_val.append(min_distance)
    max_depth_val.append(max_depth)
    info_content.append(max_res_sim)
  data['WordNet Length'] = min_length_val
  data['Wordnet Depth'] = max_depth_val
  data['Resnick Info Content'] = info_content
  data.to_csv(file)
  
def cos_vectors(word_vectors, word1, word2):
  vec1 = word_vectors[word1]
  vec2 = word_vectors[word2]
  return np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))

def generate_similarity_vector(file, vector_sys):
  word_vectors = gensim.downloader.load(vector_sys)  
  data = pd.read_csv(file)
  similarity_measure = []
  for i in range(len(data)):
      word1 = data.loc[i, 'Word1']
      word2 = data.loc[i, 'Word2']
      try:
          val1 = cos_vectors(word_vectors, word1, word2)
      except:
          val1 = -2    
      similarity_measure.append(val1)
      
  data[vector_sys] = similarity_measure
  data.to_csv(file)

def main():
  input = take_input()
  generate_similarity_wordnet(input.f)
  generate_similarity_vector(input.f, input.v)
  
if __name__ == '__main__':
  main()