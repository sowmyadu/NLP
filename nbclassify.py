import json
import os
import fnmatch
import math


# nbmodel.txt || nbmodel.json
#
# spam_words(dict)
# ham_words(dict)
# total_spam_words(int)
# total_ham_words(int)
# spam_vocab(int)
# ham_vocab(int)
# prob(dict)
# prob_spam(dict)
# prob_ham(dict)


def get_dev_files(extension, directory):

    class_label = {}
    true_label = {}
    vocab_length = len(vocab)

    for root, directory, filename in os.walk(directory):
        for file in fnmatch.filter(filename, extension):
            if file.endswith('spam.txt'):
                prob_word_spam = 0
                prob_word_ham = 0
                fullpath = os.path.join(root, file)
                with open(fullpath, "r", encoding="latin1") as f:
                    for line in f:
                        line = line.lower()
                        words = line.split()
                        # getting counts from file
                        for word in words:
                            if word not in vocab:
                                continue
                            word_spam = math.log((spam_words.get(word, 0) + 1) / (total_spam_words + vocab_length))
                            word_ham = math.log((ham_words.get(word, 0) + 1) / (total_ham_words + vocab_length))
                            prob_word_spam += word_spam
                            prob_word_ham += word_ham
                        prob_word_spam += prob['spam']
                        prob_word_ham += prob['ham']

                        if prob_word_spam > prob_word_ham:
                            class_label[fullpath] = 'spam'
                            true_label[fullpath] = 'spam'
                        else:
                            class_label[fullpath] = 'ham'
                            true_label[fullpath] = 'spam'

            elif file.endswith('ham.txt'):
                prob_word_spam = 0
                prob_word_ham = 0
                fullpath = os.path.join(root, file)
                with open(fullpath, "r", encoding="latin1") as f:
                    for line in f:
                        line = line.lower()
                        words = line.split()
                        for word in words:
                            if word not in vocab:
                                continue
                            word_spam = math.log((spam_words.get(word, 0) + 1) / (total_spam_words + vocab_length))
                            word_ham = math.log((ham_words.get(word, 0) + 1) / (total_ham_words + vocab_length))
                            prob_word_spam += word_spam
                            prob_word_ham += word_ham
                        prob_word_spam += prob['spam']
                        prob_word_ham += prob['ham']

                        if prob_word_spam > prob_word_ham:
                            class_label[fullpath] = 'spam'
                            true_label[fullpath] = 'ham'
                        else:
                            class_label[fullpath] = 'ham'
                            true_label[fullpath] = 'ham'
    return class_label, true_label

if __name__ == '__main__':
    #path = sys.argv[1]
    #print(path)
    with open("nbmodel.json", "r") as prob_file:
        calculated_data = json.load(prob_file)

    spam_words = calculated_data['spam_words']
    ham_words = calculated_data['ham_words']
    total_spam_words = calculated_data['total_spam_words']
    total_ham_words = calculated_data['total_ham_words']
    vocab = calculated_data['vocab']
    prob = calculated_data['prob']

    path = [data_path]
    # get_dev_files(extension="*.txt", directory=path+"/dev", spam_words, ham_words, total_spam_words, total_ham_words, vocab)
    class_label, true_label = get_dev_files(extension="*.txt", directory=path+"/dev")
    with open("nboutput.txt", "w") as file:
        for key in class_label:
            file.write(class_label.get(key)+" "+key+"\n")

