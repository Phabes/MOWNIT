import wikipedia
import json


def save_data(data):
  with open("data.json", "w") as outfile:
    json.dump(data, outfile, indent=4, sort_keys=True)


def get_wikipedia_pages_content(number):
  data = []
  while len(data) != number:
    page = wikipedia.random(1)
    try:
      a = wikipedia.page(page)
      if not any(suspect["title"] == a.title for suspect in data):
        content = str(a.content).replace("\n", " ")
        content = content.replace('"', "'")
        c = content.split("== See Also ==")
        content = c[0]
        c = content.split("== References ==")
        content = c[0]
        data.append({"title": a.title, "content": content})
    except:
      print("ERROR:", a.title)
    print(len(data))
  return data


n = 2000
data = get_wikipedia_pages_content(n)
save_data(data)
