import sys
import twitter
import os
from random import choice
def process_dict(filename):
    dict_set = set([])
    dict_file = open(filename)
    for line in dict_file:
        dict_set.add(line)
    return dict_set


class MarkovMachine(object):

    def read_files(self, filenames):
        """Given a list of files, make chains from them."""

        body = ""

        for filename in filenames:
            text_file = open(filename)
            body = body + text_file.read().decode('utf-8')
            text_file.close()

        self.make_chains(body)

    def make_chains(self, corpus):
        """Takes input text as string; returns dictionary of markov chains."""

        self.chains = {}

        words = corpus.split()

        for i in range(len(words) - 2):
            #if words[i][0].isupper():
            key = (words[i], words[i + 1])
            value = words[i + 2]
                
            if words[i].isupper() or words[i+1].isupper():
                continue
            if value.isupper():
                continue
            if key not in self.chains:
                self.chains[key] = []

            self.chains[key].append(value)


    def make_text(self, dictionary):
        """Takes dictionary of markov chains; returns random text."""

        key = choice(self.chains.keys())
        words = [key[0], key[1]]

        while key in self.chains:
            # Keep looping until we have a key that isn't in the chains
            # (which would mean it was the end of our original text)
            #
            # Note that for long texts (like a full book), this might mean
            # it would run for a very long time.

            word = choice(self.chains[key])
            words.append(word)
            key = (key[1], word)

        text = " ".join(words).encode('utf-8')

        # This is the clumsiest way to make sure it's never longer than
        # 140 characters; can you think of better ways

        text_to_print = text[:140]
        split_text = text_to_print.split(" ")
        if split_text[len(split_text)-1].upper() in dictionary:
            print text_to_print
        else:
            text_to_print = " ".join(split_text[:-1])
            print text_to_print


api = twitter.Api(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
                      consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
                      access_token_key=os.environ["TWITTER_ACCESS_TOKEN_KEY"],
                      access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])

print api.VerifyCredentials()
  

if __name__ == "__main__":
    filenames = sys.argv[1:]

    dictionary = process_dict('dictionary.txt')
    generator = MarkovMachine()
    generator.read_files(filenames)
    generator.make_text(dictionary)
    # status = api.PostUpdate(generator.make_text())
    # print status.text
