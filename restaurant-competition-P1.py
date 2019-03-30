import re, nltk, pickle, argparse, sys
import os
import data_helper, features
from features import get_features_category_tuples

DATA_DIR = "data"


def write_features_category(features_category_tuples, output_file_name, feat_file_name):
    output_file = open("{}-{}-features.txt".format(feat_file_name, output_file_name), "w", encoding="utf-8")
    for (features, category) in features_category_tuples:
        output_file.write("{0:<10s}\t{1}\n".format(category, features))
    output_file.close()
    print("hi")


def get_classifier(classifier_fname):
    classifier_file = open(classifier_fname, 'rb')
    classifier = pickle.load(classifier_file)
    classifier_file.close()
    return classifier


def save_classifier(classifier, classifier_fname):
    classifier_file = open(classifier_fname, 'wb')
    pickle.dump(classifier, classifier_file)
    classifier_file.close()
    info_file = open(classifier_fname.split(".")[0] + '-informative-features.txt', 'w', encoding="utf-8")
    for feature, n in classifier.most_informative_features(100):
        info_file.write("{0}\n".format(feature))
    info_file.close()


def evaluate(classifier, features_category_tuples, reference_text, data_set_name=None):


    accuracy = nltk.classify.accuracy(classifier, features_category_tuples)

    #test_acc = nltk.classify.accuracy(classifier., reference_text)

    print("dev: " + str(accuracy))

    features = [a[0] for a in features_category_tuples]

    labels = [a[1] for a in features_category_tuples]

    predicted_labels = classifier.classify_many(features)

    confusion_matrix = nltk.ConfusionMatrix(labels, predicted_labels)

    return accuracy, confusion_matrix


def build_features(data_file, feat_name, save_feats=None, binning=False):
    # read text data
    positive_texts, negative_texts = data_helper.get_reviews(os.path.join(DATA_DIR, data_file))

    category_texts = {"positive": positive_texts, "negative": negative_texts}

    #print(data_file)

    # build features
    features_category_tuples, texts = get_features_category_tuples(category_texts, feat_name)

    # save features to file

    data_name = ""

    if str(data_file) == "dev_examples.tsv":
        data_name =  "development"
    elif str(data_file) == "train_examples.tsv":
        data_name = "training"

    write_features_category(features_category_tuples, data_name, str(feat_name))

    return features_category_tuples, texts



def train_model(datafile, feature_set, save_model):

    features_data, texts = build_features(datafile, feature_set)

    classifier = nltk.NaiveBayesClassifier.train(features_data)




    return classifier


def train_eval(train_file, feature_set, eval_file=None):

    # train the model
    # FIXME: Change value of binning
    binning = True # FIXME:
    split_name = "train"
    #model = train_model(train_file, feature_set,  binning=binning)
    model = train_model(train_file, feature_set, train_file)

    #model.show_most_informative_features(30)

    counter = 0

    if(counter ==0):
        the_predictions = open("restaurant-competition-model-P1-predictions.txt", "w", encoding="utf-8")

        the_data = data_helper.get_reviews("data/test.txt")
        for a in the_data:
            h = features.get_words_tags(a, True)
            value = model.classify(features.get_ngram_features(h[0]))
            the_predictions.write(str(value)+"\n")
        #accuracy, cm = evaluate(model, features_data, texts, data_set_name=None)

        the_predictions.close()
    counter += 1

    original = sys.stdout
    if str(train_file) == "dev_examples.tsv":
        data_name =  "development"
    elif str(train_file) == "train_examples.tsv":
        data_name = "training"
    sys.stdout = open("{}-{}-informative-features.txt".format(feature_set, data_name), 'w', encoding="utf-8")
    model.show_most_informative_features(100)
    sys.stdout = original


    # evaluate the model
    if eval_file is not None:
        features_data, texts = build_features(eval_file, feature_set, binning=binning)
        accuracy, cm = evaluate(model, features_data, texts, data_set_name=None)


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


    # add the necessary arguments to the argument parser
    parser = argparse.ArgumentParser(description='Assignment 3')
    parser.add_argument('-d', dest="data_fname", default="train_examples.tsv",
                        help='File name of the testing data.')
    args = parser.parse_args()


    train_data = args.data_fname


    eval_data = "dev_examples.tsv"


    the_data = data_helper.get_reviews("data/test.txt")

    one = open("word_features-testing-features.txt", "w", encoding="utf-8")
    two = open("word_pos_features-testing-features.txt", "w", encoding="utf-8")
    three = open("word_pos_liwc_features-testing-features.txt", "w", encoding="utf-8")


    for a in the_data:
        h = features.get_words_tags(a, True)

        k = features.get_ngram_features(h[0])
        one.write(str(k)+"\n")

        r = features.get_word_pos_features(h[0], h[1])
        two.write(str(r)+"\n")

        s = features.get_word_pos_liwc_features(h[0], h[1])
        three.write(str(s)+"\n")

    one.close()
    two.close()
    three.close()

    for feat_set in ["word_features", "word_pos_features", "word_pos_liwc_features"]:
        print("\nTraining with {}".format(feat_set))
        acc = train_eval(train_data, feat_set, eval_file=eval_data)


if __name__ == "__main__":
    main()




