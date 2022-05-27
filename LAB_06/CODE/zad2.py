import nltk

nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import json

english_stop_words = set(stopwords.words("english"))
punctuation = string.punctuation


def create_dictionary_of_words():
  f = open("data.json", "r")
  data = json.load(f)
  f.close()
  n = len(data)
  # n = 1001
  dictionary = {}
  for i in range(n):
    text = data[i]["content"].lower()
    words = nltk.word_tokenize(text)
    words = [word for word in words if len(word) > 2]
    words = [word for word in words if ord(word[0]) <= 122 and (ord(word[0]) < 48 or ord(word[0]) > 57)]
    words = [word for word in words if word[0] not in punctuation]
    words = [word for word in words if word not in english_stop_words]
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    for word in words:
      if word in dictionary.keys():
        dictionary[word] += 1
      else:
        dictionary[word] = 1
    print(i)
  return dictionary


def save_dictionary(dictionary):
  with open("dictionary.json", "w") as outfile:
    json.dump(dictionary, outfile, indent=4, sort_keys=True)


dictionary = create_dictionary_of_words()
save_dictionary(dictionary)
