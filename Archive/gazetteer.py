import json, tqdm, sys, os
import pandas as pd

'''
mvnt.tsv is a dataset downloaded from IMDB.
Only the following columns have been saved:
 * primaryTitle - most popular title
 * startYear    - start of release
 * endYear      - end of release (TV shows, etc.)
'''

gaz = pd.read_csv("mvnt.tsv", delimiter="\t")
gaz.drop("Unnamed: 0", axis=1, inplace=True)
gaz.dropna(subset=["title"], inplace=True)

abbr_map = {
    "yrs" : "years",
    "min" : "minutes"
}

# Testing the Affix Tree
# gaz = {"title": ["Caller", "Callee", "Called", "Calles"]}

class Affix_tree:
    def __init__(self, loading_file=None):
        if loading_file != None:
            print("Loading the Gazetteer")
            with open(loading_file) as file:
                self.tree = json.loads(file.read())
        else:
            self.tree = dict()

    def add(self, title):
        x = self.tree
        try:
            for character in title:
                if character not in x.keys():
                    x[character] = {}
                x = x[character]
            x["end"] = True
        except:
            raise ValueError("Came across an error while processing:", title)
            sys.exit(1)

    def has(self, title):
        title = title.lower()
        x = self.tree
        for character in title:
            if character.lower() in x.keys() or character.upper() in x.keys():
                x = x[character]
            else:
                return False
        if x["end"]:
            return True

    def save(self):
        print("Saving the Gazetteer")
        with open("affix.tree", "w") as file:
            json.dump(self.tree, file)

    def getMatchesInSentence(self, string):
        matches = []
        for start in range(len(string)):
            x = self.tree
            if string[start] in x.keys():
                for next_char in range(len(string)-start):
                    if string[next_char]:
                        ...

    def delete(self):
        if os.path.exists("affix.tree"):
            os.remove("affix.tree")
            print("Successfully Deleted the Gazetteer")
        else:
            print("No 'affix.tree' file found in directory to delete.")

if __name__ == "__main__":
    # to create the affix.tree file
    # tree = Affix_tree()
    # tree.delete()
    # print("Building the Gazetteer")
    # for title in tqdm.tqdm(gaz["title"]):
    #     tree.add(title.lower())
    # tree.save()
    # to test loading...
    x = Affix_tree(loading_file = "affix.tree")
    print(x.has("I"))
