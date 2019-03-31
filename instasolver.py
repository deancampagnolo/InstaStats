import csv, os, nltk
from instafeatures import get_features


def evaluate(classifier, features_category_tuples, data_set_name=None):


    accuracy = nltk.classify.accuracy(classifier, features_category_tuples)

    #test_acc = nltk.classify.accuracy(classifier., reference_text)

    print("dev: " + str(accuracy))

    features = [a[0] for a in features_category_tuples]

    labels = [a[1] for a in features_category_tuples]

    predicted_labels = classifier.classify_many(features)

    confusion_matrix = nltk.ConfusionMatrix(labels, predicted_labels)

    return accuracy, confusion_matrix


def data_helper(data_file):
    with open(data_file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        positive = []
        negative = []
        for row in readCSV:
            print(row)
            print(len(row))
            print(row[0])
            if float(row[2]) < 1.5:#FIXME change this bc it makes no sense in the future
                negative.append(row)
            else:
                positive.append(row)
        print("\n\n--Positive--")
        print(positive)
        print("\n\n--Negative--")
        print(negative)
    return positive, negative

def build_features(data_file, feat_name, save_feats=None, binning=False):
    # read text data
    positive_texts, negative_texts = data_helper(data_file)

    category_texts = {"positive": positive_texts, "negative": negative_texts}


    # build features
    the_features = get_features(category_texts) #this contains positive and the negative feature

    return the_features

def train_model(datafile, feature_set, save_model):

    features_data = build_features(datafile, feature_set)

    classifier = nltk.NaiveBayesClassifier.train(features_data)

    return classifier

def train_eval(train_file, feature_set, eval_file=None):

    # train the model
    # FIXME: Change value of binning
    binning = True # FIXME:
    split_name = "train"
    #model = train_model(train_file, feature_set,  binning=binning)
    model = train_model(train_file, feature_set, train_file)

    model.show_most_informative_features(30)



    # evaluate the model
    if eval_file is not None:
        features_data = build_features(eval_file, feature_set)
        print()
        print(features_data)
        accuracy, cm = evaluate(model, features_data)


        print("The accuracy of {} is: {}".format(eval_file, accuracy))
        print("Confusion Matrix:")
        print(str(cm))





        if feature_set == "word_features":
            one = open("output-ngrams.txt", "w", encoding="utf-8")
            one.write("The accuracy of {} is: {}".format(eval_file, accuracy)+"\n")
            one.write("Confusion Matrix:\n"+str(cm))
            one.close()

            four = open("output-best.txt", "w", encoding="utf-8")
            four.write("The accuracy of {} is: {}".format(eval_file, accuracy) + "\n")
            four.write("Confusion Matrix:\n" + str(cm))
            four.close()

        elif feature_set == "word_pos_features":
            two = open("output-pos.txt", "w", encoding="utf-8")
            two.write("The accuracy of {} is: {}".format(eval_file, accuracy) + "\n")
            two.write("Confusion Matrix:\n" + str(cm))
            two.close()

        elif feature_set == "word_pos_liwc_features":
            three = open("output-liwc.txt", "w", encoding="utf-8")
            three.write("The accuracy of {} is: {}".format(eval_file, accuracy) + "\n")
            three.write("Confusion Matrix:\n" + str(cm))
            three.close()
    else:
        accuracy = None

    return accuracy


def main():
    train_eval("insta_data.csv","t","insta_data2.csv")

if __name__ == "__main__":
    main()