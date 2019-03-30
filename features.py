
import nltk
import re
import word_category_counter
import data_helper
import os, sys

DATA_DIR = "data"
LIWC_DIR = "liwc"

word_category_counter.load_dictionary(LIWC_DIR)


def normalize(token, should_normalize=True):
    """
    This function performs text normalization.

    If should_normalize is False then we return the original token unchanged.
    Otherwise, we return a normalized version of the token, or None.

    For some tokens (like stopwords) we might not want to keep the token. In
    this case we return None.

    :param token: str: the word to normalize
    :param should_normalize: bool
    :return: None or str
    """
    
    
    normalized_token = []
    
    if not should_normalize:
        normalized_token = token

    else:
        
        stop_words = nltk.corpus.stopwords.words('english')
        normalized_token = [word.lower() for word in token if word.lower() not in stop_words and re.search(r'\w', word)]
        
        
        #print("hi")
        ###     YOUR CODE GOES HERE
        #raise NotImplemented

    return normalized_token



def get_words_tags(text, should_normalize=True):
    """
    This function performs part of speech tagging and extracts the words
    from the review text.

    You need to :
        - tokenize the text into sentences
        - word tokenize each sentence
        - part of speech tag the words of each sentence

    Return a list containing all the words of the review and another list
    containing all the part-of-speech tags for those words.

    :param text:
    :param should_normalize:
    :return:
    """

    sentence = nltk.sent_tokenize(text)
    words = []

    for i in sentence:
        sent = nltk.word_tokenize(i)
        if should_normalize:
            sent = normalize(sent)
        for j in sent:
            words.append(j)

    tags_and_words = nltk.pos_tag(words)
    tags = []
    
    for i in range(len(tags_and_words)):
        tags.append(tags_and_words[i][1])


    # tokenization for each sentence


    return words, tags


def write_unigram_freq(unigrams):
    """
    A function to write the unigrams and their frequencies to file.

    :param category: [string]
    :param unigrams: list of (word, frequency) tuples
    :return:
    """

    for word, count in unigrams:
        print(word + "\t" + str(count))



def write_bigram_freq(bigrams):
    """
    A function to write the unigrams and their frequencies to file.

    :param category: [string]
    :param unigrams: list of (word, frequency) tuples
    :return:
    """
    h = 0

    for bi, count in bigrams:

        print(bi + "\t" + str(count))
        h += count


def get_ngram_features(tokens):
    """
    This function creates the unigram and bigram features as described in
    the assignment3 handout.

    :param tokens:
    :return: feature_vectors: a dictionary values for each ngram feature
    """

    feature_vectors = {}
    """
    freq = nltk.FreqDist(a for a in tokens)

    for word, count in freq.items():
        feature_vectors.update({word: bin(count)})

    """
    bigram_tokens = nltk.bigrams(tokens)

    uni_freq = nltk.FreqDist(u"UNI_{}".format(a) for a in tokens)

    bi_freq = nltk.FreqDist(u"BIGRAM_{}_{}".format(a, b) for a, b in bigram_tokens)

    #write_unigram_freq(uni_freq.items())

    #write_bigram_freq(bi_freq.items())

    for word, count in uni_freq.items():
        feature_vectors.update({word: bin(count)})

    for word, count in bi_freq.items():
        feature_vectors.update({word: bin(count)})


    return feature_vectors


def get_pos_features(tags):
    """
    This function creates the unigram and bigram part-of-speech features
    as described in the assignment3 handout.

    :param tags: list of POS tags
    :return: feature_vectors: a dictionary values for each ngram-pos feature
    """
    feature_vectors = {}
    bi_tags = nltk.bigrams(tags)

    freq = nltk.FreqDist(u"UNI_POS_{}".format(a) for a in tags)

    bi_freq = nltk.FreqDist(u"BI_POS_{}_{}".format(a, b) for a, b in bi_tags)

    for tag, count in freq.items():
        feature_vectors.update({tag: bin(count)})

    for tag, count in bi_freq.items():
        feature_vectors.update({tag: bin(count)})

    return feature_vectors

def bin(count):
    """
    Results in bins of  0, 1, 2, 3 >=
    :param count: [int] the bin label
    :return:
    """
    the_bin = None
    if count < 3:
        the_bin = count
    else:
        the_bin = 3

    return the_bin

def bin2(count):
    """
    Results in bins of  0, 1, 2, 3 >=
    :param count: [int] the bin label
    :return:
    """
    the_bin = None
    if count < 5:
        the_bin = count
    else:
        the_bin = 5

    return the_bin



def get_liwc_features(words):
    """
    Adds a simple LIWC derived feature

    :param words:
    :return:
    """
    # TODO: binning
    # FIXME: binning

    feature_vectors = {}
    text = " ".join(words)
    liwc_scores = word_category_counter.score_text(text)

    # All possible keys to the scores start on line 269
    # of the word_category_counter.py script
    negative_score = bin2(liwc_scores["Negative Emotion"])
    positive_score = bin2(liwc_scores["Positive Emotion"])
    feature_vectors["Negative Emotion"] = negative_score
    feature_vectors["Positive Emotion"] = positive_score

    if positive_score > negative_score:
        feature_vectors["liwc:positive"] = 1
    else:
        feature_vectors["liwc:negative"] = 1



    feature_vectors["Swear Words"] = bin2(liwc_scores["Swear Words"])
    feature_vectors["Anger"] = bin2(liwc_scores["Anger"])
    feature_vectors["Sadness"] = bin2(liwc_scores["Sadness"])
    feature_vectors["Inhibition"] = bin2(liwc_scores["Inhibition"])
    feature_vectors["Assent"] = bin2(liwc_scores["Assent"])#because 3 is included in negative


    return feature_vectors

def get_word_pos_liwc_features(word, pos):
    features_vectors = {}

    features_vectors.update(get_word_pos_features(word, pos))
    features_vectors.update(get_liwc_features(word))

    return features_vectors

def get_word_pos_features(word, pos):

    feature_vectors = {}

    feature_vectors.update(get_ngram_features(word))

    feature_vectors.update(get_pos_features(pos))
    return feature_vectors





FEATURE_SETS = {"word_pos_features", "word_features", "word_pos_liwc_features"}

def get_features_category_tuples(category_text_dict, feature_set):
    """

    You will might want to update the code here for the competition part.

    :param category_text_dict:
    :param feature_set:
    :return:
    """
    features_category_tuples = []
    all_texts = []

    assert feature_set in FEATURE_SETS, "unrecognized feature set:{}, Accepted values:{}".format(feature_set, FEATURE_SETS)


    counter = 0
    for category in category_text_dict:
        for text in category_text_dict[category]:

            words, tags = get_words_tags(text)
            #words2, tags2 = get_words_tags(text, False)# - I tried to do without normalizing
            feature_vectors = {}

            if feature_set == "word_features":
                feature_vectors = get_ngram_features(words)
            elif feature_set == "word_pos_features":
                feature_vectors = get_word_pos_features(words, tags) #I tried to do without normalizing
            elif feature_set == "word_pos_liwc_features":
                feature_vectors = get_word_pos_liwc_features(words, tags)#I tried to do without normalizing

            #if counter ==0:
            #print(feature_vectors)
            #counter+=1
            features_category_tuples.append((feature_vectors, category))
            all_texts.append(text)

    return features_category_tuples, all_texts


def write_features_category(features_category_tuples, outfile_name):
    """
    Save the feature values to file.

    :param features_category_tuples:
    :param outfile_name:
    :return:
    """
    with open(outfile_name, "w", encoding="utf-8") as fout:
        for (features, category) in features_category_tuples:
            fout.write("{0:<10s}\t{1}\n".format(category, features))


if __name__ == "__main__":
    
    h = "the fox is really cool"
    
    h_new = nltk.word_tokenize(h)
    
    print(h_new)
    
    paragraph = """Text classification requires assigning a category from a predefined set to each document of interest. For this assignment, you will build off of the previous assignment to model the reviews as a feature vector. You will then use these feature vector representations to make predictions about unlabeled (unknown rating) reviews. To do this, you will need to build and train a classifier."""
    
    k = get_words_tags(paragraph, True)
    print(k[0])
    print(k[1])

    print("Get ngram Features")

    print(get_ngram_features(k[0]))

    print(get_ngram_features(k[1]))
    
    
    pass

