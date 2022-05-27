import numpy as np
import string
import json
import time
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.preprocessing import normalize

english_stop_words = set(stopwords.words("english"))
punctuation = string.punctuation


def normalize_matrix(idfs):
  normalized = []
  count = 0
  for document in idfs:
    for key in document.keys():
      normalized_array = normalize([document[key]], norm="l1")[0].tolist()
      for i in range(len(normalized_array)):
        if normalized_array[i] == 0:
          normalized_array[i] = 0
      normalized.append(normalized_array)
    count += 1
    print(count)
  return normalized


def save_dictionary(matrix):
  with open("IDF_normalized_matrix.json", "w") as outfile:
    json.dump(matrix, outfile, sort_keys=True)


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


def get_k_closest_documents(dictionary, normalized_idfs, data, k):
  vector = create_bag_of_words_vector(dictionary, data)
  q_vector = normalize([vector], norm="l1")[0]
  q_vector_T = np.array(q_vector).T
  arr_of_cos = normalized_idfs @ q_vector_T
  best_k_elements = [(i, arr_of_cos[i]) for i in range(len(arr_of_cos))]
  best_k_elements = sorted(best_k_elements, key=lambda x: x[1], reverse=True)
  return best_k_elements[:k]


query = input("Search: ")
k = 10
f = open("dictionary_2.json", "r")
dictionary = json.load(f)
f.close()
f = open("IDF_normalized_matrix_2.json", "r")
normalized_idfs = json.load(f)
f.close()
# f = open("IDF.json", "r")
# idfs = json.load(f)
# f.close()
# normalized = normalize_matrix(idfs)
# save_dictionary(normalized)
start = time.time()
documents = get_k_closest_documents(dictionary, normalized_idfs, query, k)
end = time.time()
print(documents)
print(end - start)

f = open("data.json", "r")
data = json.load(f)
f.close()
for document in documents:
  print(document, data[document[0]]["title"])
