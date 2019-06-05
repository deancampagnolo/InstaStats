import csv, os, nltk, sys
from instafeatures import get_features,get_date_features,get_color_features,get_picture_features
import subprocess
import DataFileCreator


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
            #print(row)
            #print(len(row))
            #print(row[0])
            if float(row[2]) < .0006:#FIXME change this bc it makes no sense in the future
                negative.append(row)
            else:
                positive.append(row)
        #print("\n\n--Positive--")
        print(len(positive))
        #print("\n\n--Negative--")
        print(len(negative))
    return positive, negative

def build_features(data_file, feat_name, save_feats=None, binning=False):
    # read text data
    positive_texts, negative_texts = data_helper(data_file)
    positive_texts = [x for x in positive_texts if len(x) == 5]
    negative_texts = [x for x in negative_texts if len(x) == 5]
    print("posii")
    print(len(positive_texts))
    print(len(negative_texts))

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

    temp = sys.stdout
    sys.stdout = open("informative.txt", "w", encoding="utf-8")
    model.show_most_informative_features(1000)
    sys.stdout = temp

    with open("informative.txt") as fp:
        for i, line in enumerate(fp):
            if "Party" in line:
                print("YES\n\n\n\n\n\n")
                print(i)
                if "positi : negati" in line:
                    if int(line[-10:-9])>2:
                        print("Nice Job")
                if "negati : positi" in line:
                    if int(line[-10:-9])>2:
                        print("You are ugly")
    print("h")



    # evaluate the model
    if eval_file is not None:
        features_data = build_features(eval_file, feature_set)
        print()
        #print(features_data)
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
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\momok\Desktop\LAHacks2019\My First Project-1a0343ad2ed1.json"
    print("hi")
    username = input("Please type your instagram username:")
    prefix_instagram = "https://ingram.life/u/"

    prefix = "instagram-scraper "
    my_username = " -u dean_campo -p DeanCole1 --maximum "
    naming_convention = " -t image -T {date} --retry-forever -d ./photos/"

    command = prefix + username + my_username + str(1) + naming_convention + username  # listofnumberofuploads[i]
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    user = [username, '20181231', '1', '2']  # , '#pictures1|herp', 'lmao look at my cat']
    DataFileCreator.photo_fill(user)
    print(user[4])
    #20181231





    feature_vectors = {}

#    if get_color_features(person[4]) is not None:
#        feature_vectors.update(get_color_features(person[4]))
#    feature_vectors.update(get_picture_features(person[3]))




    train_eval("the_data2.csv","t","the_data3.csv")

if __name__ == "__main__":
    main()