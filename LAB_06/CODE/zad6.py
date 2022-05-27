import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import json
import math

english_stop_words = set(stopwords.words("english"))
punctuation = string.punctuation


def create_bag_of_words_vector(dictionary, data):
  vector = {}
  for word in dictionary.keys():
    vector[word] = 0
  text = data.lower()
  words = nltk.word_tokenize(text)
  words = [word for word in words if len(word) > 2]
  words = [word for word in words if ord(word[0]) <= 122 and (ord(word[0]) < 48 or ord(word[0]) > 57)]
  words = [word for word in words if word[0] not in punctuation]
  words = [word for word in words if word not in english_stop_words]
  stemmer = PorterStemmer()
  words = [stemmer.stem(word) for word in words]
  for word in words:
    vector[word] += 1
  arr = list(vector.values())  # or [vector[key] for key in vector.keys()]
  return arr


def get_k_closest_documents(dictionary, idfs, data, k):
  vector = create_bag_of_words_vector(dictionary, data)
  vector_T = np.array(vector).T
  best_k_elements = []
  index = 0
  for document in idfs:
    for key in document.keys():
      values = document[key]
      cos = (vector_T @ np.array(values)) / (np.linalg.norm(vector) * np.linalg.norm(values))
      if len(best_k_elements) < k:
        best_k_elements.append((key, cos))
        best_k_elements = sorted(best_k_elements, key=lambda x: x[1])
      else:
        last = best_k_elements[0][1]
        if cos > last or math.isnan(last):
          best_k_elements[0] = (key, cos)
          best_k_elements = sorted(best_k_elements, key=lambda x: x[1])
    index += 1
    print(index)
  best_k_elements = list(reversed(best_k_elements))
  return best_k_elements


query = input("Search: ")
f = open("dictionary.json", "r")
dictionary = json.load(f)
f.close()
f = open("IDF.json", "r")
idfs = json.load(f)
f.close()
k = 10
documents = get_k_closest_documents(dictionary, idfs, query, k)
print(documents)
