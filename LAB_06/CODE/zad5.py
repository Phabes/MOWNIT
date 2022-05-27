import json
import math


def count_documents_with_word(data, word_index):
  count = 0
  for document in data:
    amount = list(document.values())[0][word_index]
    if amount > 0:
      count += 1
  return count


def save_dictionary(matrix):
  with open("IDF.json", "w") as outfile:
    json.dump(matrix, outfile, sort_keys=True)


def multiply_by_IDF(data, word_index, idf):
  for document in data:
    for key in document.keys():
      if document[key][word_index] != 0:
        document[key][word_index] *= idf


def calculate_IDF(dictionary, data):
  n = len(data)
  word_index = 0
  for _ in dictionary.keys():
    nw = count_documents_with_word(data, word_index)
    idf = math.log(n / nw)
    multiply_by_IDF(data, word_index, idf)
    word_index += 1
    print(word_index)


f = open("dictionary.json", "r")
dictionary = json.load(f)
f.close()
f = open("bag_of_words_vectors.json", "r")
data = json.load(f)
f.close()

calculate_IDF(dictionary, data)
save_dictionary(data)
