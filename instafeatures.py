


def get_date_features(date):
    return {date:1}

def get_number_of_posts_features(number):
    return {number:1}

def get_picture_features(pic_feat_string):#TODO bin this
    feature_vectors = {}
    list_of_pic_feat = pic_feat_string.split("|")
    for attribute in list_of_pic_feat:
        feature_vectors.update({attribute:1})
    return feature_vectors

def get_features(category_text_dict):
    print("start of get_features")
    features_category_tuples = []
    all_texts = []
    #print(category_text_dict)


    counter = 0
    for category in category_text_dict:
        print(category)
        for person in category_text_dict[category]:
            print(person)

            #words2, tags2 = get_words_tags(text, False)# - I tried to do without normalizing
            feature_vectors = {}

            feature_vectors.update(get_date_features(person[1]))
            feature_vectors.update(get_number_of_posts_features(person[3]))
            feature_vectors.update(get_picture_features(person[4]))


            #if counter ==0:
            #print(feature_vectors)
            #counter+=1
            features_category_tuples.append((feature_vectors, category))
            #all_texts.append(text)
    print("end of get_features")
    print(features_category_tuples)
    return features_category_tuples#, all_texts

def main():
    print("you probably running the wrong function buddy.")

if __name__ == "__main__":
    main()
