import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import json

nltk.download('stopwords')
nltk.download('punkt')

english_stop_words = set(stopwords.words("english"))
punctuation = string.punctuation


def create_bag_of_words_matrix():
  f = open("data.json", "r")
  data = json.load(f)
  f.close()
  f = open("dictionary.json", "r")
  dictionary = json.load(f)
  f.close()
  n = len(data)
  # n = 1001
  matrix = []
  for i in range(n):
    matrix.append({data[i]["title"]: create_bag_of_words_vector(dictionary, data[i]["content"])})
    print(i)
  return matrix


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


def save_dictionary(matrix):
  with open("bag_of_words_vectors.json", "w") as outfile:
    json.dump(matrix, outfile, sort_keys=True)


matrix = create_bag_of_words_matrix()
save_dictionary(matrix)
