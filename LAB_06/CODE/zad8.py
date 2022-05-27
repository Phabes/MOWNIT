import numpy as np
import scipy.sparse.linalg
import string
import json
import time
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.preprocessing import normalize

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


def use_svd_and_low_rank_approx(normalized_idfs, k):
  u, s, vh = scipy.sparse.linalg.svds(scipy.sparse.linalg.aslinearoperator(np.array(normalized_idfs)), k=k)
  # u, s, vh = scipy.sparse.linalg.svds(scipy.sparse.linalg.aslinearoperator(np.array(normalized_idfs, dtype="float32")), k=k) # use this is above line doesnt work because of used memory
  # u, s, vh = scipy.sparse.linalg.svds(normalized_idfs, k=k) # also works

  # Ia = np.zeros((len(normalized_idfs), len(normalized_idfs[0])), dtype="float32")
  # for i in range(k):
  #   Ia += s[i] * np.outer(u.T[i], vh[i])
  # return Ia
  # return u[:, :k] @ np.diag(s[:k]) @ vh[:k, :]
  return u @ np.diag(s) @ vh


def get_k_closest_documents(dictionary, normalized_idfs, data, k, approx_k):
  normalized_idfs_noise_reduced = use_svd_and_low_rank_approx(normalized_idfs, approx_k)
  print(len(normalized_idfs_noise_reduced), len(normalized_idfs_noise_reduced[0]))
  vector = create_bag_of_words_vector(dictionary, data)
  q_vector = normalize([vector], norm="l1")[0]
  q_vector_T = np.array(q_vector).T
  best_k_elements = []
  index = 0
  for document in normalized_idfs_noise_reduced:
    values = document
    cos = (q_vector_T @ np.array(values)) / (np.linalg.norm(q_vector) * np.linalg.norm(values))
    best_k_elements.append((index, cos))
    index += 1
    print(index)
  best_k_elements = sorted(best_k_elements, key=lambda x: x[1], reverse=True)
  return best_k_elements[:k]


query = input("Search: ")
k = 10
approx_k = 100
f = open("dictionary_2.json", "r")
dictionary = json.load(f)
f.close()
f = open("IDF_normalized_matrix_2.json", "r")
normalized_idfs = json.load(f)
f.close()
start = time.time()
documents = get_k_closest_documents(dictionary, normalized_idfs, query, k, approx_k)
end = time.time()
print(documents)
print(end - start)

f = open("data.json", "r")
data = json.load(f)
f.close()
for document in documents:
  print(document, data[document[0]]["title"])
