import sys
import os
import fnmatch
import math
import json

def get_text_files(extension, directory):
    spam_file_matches = []
    ham_file_matches = []
    spam_words = {}
    ham_words = {}
    total_spam_words =0
    total_ham_words =0
    vocab = {}
    for root, directory, filename in os.walk(directory):
        for file in fnmatch.filter(filename, extension):
            if file.endswith('spam.txt'):
                fullpath = os.path.join(root, file)
                spam_file_matches.append(fullpath)

                # spam_words = getcountfromfile(file, spam_words)
                #print(fullpath)
                with open(fullpath, "r", encoding="latin1") as f:
                    for line in f:
                        line = line.lower()
                        words = line.split()
                        # getting counts from file
                        total_spam_words = total_spam_words + len(words)
                        for word in words:
                            spam_words[word] = spam_words.get(word, 0) + 1
                            vocab[word] = vocab.get(word, 0)+1
            elif file.endswith('ham.txt'):
                # ham_file_matches.append(os.path.join(root, file))
                # ham_words = getcountfromfile(file, ham_words)
                fullpath = os.path.join(root, file)
                ham_file_matches.append(fullpath)

                # spam_words = getcountfromfile(file, spam_words)
                with open(fullpath, "r", encoding="latin1") as f:
                    for line in f:
                        line = line.lower()
                        words = line.split()
                        # getting counts from file
                        total_ham_words = total_ham_words + len(words)
                        for word in words:
                            ham_words[word] = ham_words.get(word, 0) + 1
                            vocab[word] = vocab.get(word, 0) + 1
    # task 2:
    spam_file_length = len(ham_file_matches)
    print(spam_file_length)
    #10% :: 953

    ham_file_length = len(spam_file_matches)
    print(ham_file_length)
    #10% :: 750

    return spam_words, ham_words, total_spam_words, total_ham_words, vocab


class NBLearn:
    prob_spam = {}
    prob_ham = {}
    prob = {}
    spam_vocab = 0
    ham_vocab = 0
    total_words = 0

    # def getcountfromfile(self, file, cat_words):
    #
    #     with open(file, "r", encoding="latin1") as f:
    #         for line in f:
    #             line = line.lower()
    #             words = line.split()
    #             #getting counts from file
    #             cat_words = [cat_words.get(word, 0.0) + 1.0 for word in words]
    #     return cat_words
    #wordFreq = [words.count(w) for w in words]
    #return dict(list(zip(words, wordFreq)))
    def __init__(self, sw, hw, tsw, thw, v):
        self.spam_words = sw
        self.ham_words = hw
        self.total_spam_words = tsw
        self.total_ham_words = thw
        self.vocab = v

    def calculateprob(self):

        # vocab_length = len(self.vocab)
        self.spam_vocab = len(self.spam_words)
        self.ham_vocab = len(self.spam_words)
        self.total_words = self.total_spam_words + self.total_ham_words
        self.prob['spam'] = math.log(self.total_spam_words / self.total_words)
        self.prob['ham'] = math.log(self.total_ham_words / self.total_words)

        # for w in self.spam_words.keys():
        #     self.prob_spam[w] = math.log((self.spam_words.get(w) + 1) / (self.total_spam_words + self.spam_vocab))
        #
        # for w in self.ham_words.keys():
        #     self.prob_ham[w] = math.log((self.ham_words.get(w) + 1) / (self.total_ham_words + self.ham_vocab))


if __name__ == '__main__':
    #path = sys.argv[1]
    #print(path)
    path = [data_path]
    #path = os.getcwd()
    spam_words, ham_words, total_spam_words, total_ham_words, vocab = get_text_files(extension="*.txt", directory=path+"/train")
    nb = NBLearn(spam_words, ham_words, total_spam_words, total_ham_words, vocab)

    print("Unique Spam Words: ", len(nb.spam_words))
    print("Unique Ham Words: ", len(nb.ham_words))
    print("Total Spam Words: ", nb.total_spam_words)
    print("total Ham Words: ", nb.total_ham_words)

    #calculate probabilities
    nb.calculateprob()

    prob_data = {}
    prob_data['spam_words'] = nb.spam_words
    prob_data['ham_words'] = nb.ham_words
    prob_data['total_spam_words'] = nb.total_spam_words
    prob_data['total_ham_words'] = nb.total_ham_words
    prob_data['spam_vocab'] = nb.spam_vocab
    prob_data['ham_vocab'] = nb.ham_vocab
    prob_data['vocab'] = vocab
    prob_data['prob'] = nb.prob
    #prob_data['prob_spam'] = nb.prob_spam
    #prob_data['prob_ham'] = nb.prob_ham

    with open("nbmodel.json", "w") as model_file:
        json.dump(prob_data, model_file)


    # spam_words: dict of spam words
    # spam_vocab: length of unique spam words
    # total_spam_words: total no of spam words
    # vocab: length of unique words
