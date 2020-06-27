import src.hw2_corpus_tool as utility
import src.data_segragation as divide
import pycrfsuite
import sys
import os


def trainCRF(train_list):
    # training model
    train_labels = []
    train_features = []
    for file in train_list:
        prev_speaker = ''
        i = 0
        fe = []
        tag = []
        for item in file[1]:
            fa = []
            cur_speaker = item.speaker
            if i == 0:
                fa.append("FIRST")
            else:
                fa.append("CONTINUED")
            if cur_speaker != prev_speaker and i>0:
                fa.append("SPEAKER_CHANGE")

            tokens = item.pos
            #if tokens is None:
            #    fa.append("NO_WORDS")
            if tokens is not None:
                for x in tokens:
                    # if x == tokens[0]:
                    #     #print("YES " + file[0]+ ":: "+str(tokens[0]))
                    #     fa.append("BEGIN_TOKEN_" + tokens[0].token)
                    #     fa.append("BEGIN_POS_" + tokens[0].pos)
                    if x.token == "!":
                        fa.append("EXCLAIM")
                    fa.append("TOKEN_"+getattr(x, "token"))
                    fa.append("POS_"+getattr(x, "pos"))
                    # if x == tokens[-1]:
                    #     # print("YES " + file[0]+ ":: "+str(tokens[0]))
                    #     fa.append("END_TOKEN_" + tokens[-1].token)
                    #     fa.append("END_POS_" + tokens[-1].pos)
            else:
                fa.append("NO_WORDS")
            #bigrams:
            if tokens is not None and len(tokens) >= 2:
                for i in range(len(tokens)-1):
                    fa.append("TOKEN_BIGRAM_" + tokens[i].token + " " + tokens[i+1].token)
                    fa.append("POS_BIGRAM_" + tokens[i].pos + " " + tokens[i+1].token)

            #trigrams:
            if tokens is not None and len(tokens) >= 3:
                for i in range(len(tokens)-2):
                    fa.append("TOKEN_TRIGRAM_" + tokens[i].token + " " + tokens[i+1].token + " " + tokens[i+2].token)
                    fa.append("POS_TRIGRAM_" + tokens[i].pos + " " + tokens[i+1].pos + " " + tokens[i+2].pos)

            tag.append(item.act_tag)
            text = item.text
            # print(text)

            fe.append(fa)
            i += 1
            prev_speaker = cur_speaker
        train_features.append(fe)
        train_labels.append(tag)

    trainer = pycrfsuite.Trainer(verbose=False)

    for feature_seq, label_seq in zip(train_features, train_labels):
        trainer.append(feature_seq, label_seq)
        trainer.set_params({
            'c1':1.0,
            'c2':1e-3,
            'max_iterations': 50,
            'feature.possible_transitions': True
        })

    trainer.train('advanceTagger.crfsuite')


def testCRF(test_list, output):
    #testing model
    print("Predicting the test set")
    test_features = []
    true_labels = []
    file_list = []
    tagger = pycrfsuite.Tagger()
    tagger.open('advanceTagger.crfsuite')
    for dialog in test_list:
        speaker1 = ''
        #speaker2 = ''
        i = 0
        dialog_feature = []
        dialog_label = []
        for utterance in dialog[1]:
            feature = []
            #true_tag = ''
            speaker2 = utterance.speaker
            if i == 0:
                feature.append("FIRST")
            else:
                feature.append("CONTINUED")
            if speaker1 != speaker2 and i>0:
                feature.append("SPEAKER_CHANGE")

            tag = utterance.pos
            #if tag is None:
            #    feature.append("NO_WORDS")
            if tag is not None:
                for token in tag:
                    # if token == tag[0]:
                    #     #print("YES " + file[0]+ ":: "+str(tokens[0]))
                    #     feature.append("BEGIN_TOKEN_" + tag[0].token)
                    #     feature.append("BEGIN_POS_" + tag[0].pos)
                    if token.token == "!":
                        feature.append("EXCLAIM")
                    feature.append("TOKEN_"+getattr(token, 'token'))
                    feature.append("POS_" + getattr(token, 'pos'))
                    # if token == tag[-1]:
                    #     #print("YES " + file[0]+ ":: "+str(tokens[0]))
                    #     feature.append("END_TOKEN_" + tag[-1].token)
                    #     feature.append("END_POS_" + tag[-1].pos)
            else:
                feature.append("NO_WORDS")
            # bigrams:
            if tag is not None and len(tag) >= 2:
                for i in range(len(tag) - 1):
                    feature.append("TOKEN_BIGRAM_" + tag[i].token + " " + tag[i + 1].token)
                    feature.append("POS_BIGRAM_" + tag[i].pos + " " + tag[i + 1].token)

            # trigrams:
            if tag is not None and len(tag) >= 3:
                for i in range(len(tag) - 2):
                    feature.append("TOKEN_TRIGRAM_" + tag[i].token + " " + tag[i + 1].token + " " + tag[i + 2].token)
                    feature.append("POS_TRIGRAM_" + tag[i].pos + " " + tag[i + 1].pos + " " + tag[i + 2].pos)

            true_tag = utterance.act_tag
            dialog_feature.append(feature)
            dialog_label.append(true_tag)
            i += 1
            speaker1 = speaker2
        test_features.append(dialog_feature)
        true_labels.append(dialog_label)
        file_list.append(dialog[0])

    #writing to output file
    file = open(output, "w")
    predicted_labels = []
    for i in range(len(test_features)):
        pred_test_dialogue = []
        pred_test_dialogue = tagger.tag(test_features[i])
        file.write("FILE: " + os.path.basename(file_list[i]) + "\n")
        for j in range(len(pred_test_dialogue)):
            file.write(pred_test_dialogue[j] + "\t" + true_labels[i][j])
            file.write('\n')
        file.write('\n')
        predicted_labels.append(pred_test_dialogue)
    file.close()

    #calculate accuracy
    correct = 0
    total = 0
    for i in range(len(true_labels)):
        for j in range(len(true_labels[i])):
            total += 1
            if predicted_labels[i][j] == true_labels[i][j]:
                correct += 1
    print(correct)
    print(total)
    print("Accuracy: " + str(correct/total*100) + "%\n")


if __name__ == '__main__':
    # input = sys.argv[1]
    input_dir = [path]
    # output = sys.argv[2]
    print("Started CRF")

    # train_set = utility.get_data(argv[1])
    # train(train_set)
    #
    # test_set = utility.get_data(argv[2])
    # output_file = argv[3]
    # test(test_set, output_file)

    output = "advance_output.txt"
    train_set, test_set = divide.dataSegragation(input_dir)
    trainCRF(train_set)
    testCRF(test_set, output)
    print("Completed Sequence Labeling")
