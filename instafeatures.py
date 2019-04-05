import webcolors


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name



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

def get_color_features(the_string):
    feature_vectors = {}
    list_of_color = the_string.split("!")
    super_list_of_color = list_of_color[0].split("|")
    #print(super_list_of_color)
    if super_list_of_color == ['']:
        return

    #print(super_list_of_color[1])

    #print(int(super_list_of_color[1][:-2]))
    actual_name, closest_name = get_colour_name((int(super_list_of_color[1][:-2]),int(super_list_of_color[2][:-2]),int(super_list_of_color[3][:-2])))
    #print(closest_name)
    return {closest_name:1}

def get_color_features2(the_string):
    feature_vectors = {}
    list_of_color = the_string.split("!")
    if len(list_of_color) <2:
        return
    super_list_of_color = list_of_color[1].split("|")
    #print(super_list_of_color)
    if super_list_of_color == ['']:
        return


    #print(super_list_of_color[1])

    #print(int(super_list_of_color[1][:-2]))
    actual_name, closest_name = get_colour_name((int(super_list_of_color[1][:-2]),int(super_list_of_color[2][:-2]),int(super_list_of_color[3][:-2])))
    #print(closest_name)
    return {closest_name:1}

def get_features(category_text_dict):
    print("start of get_features")
    features_category_tuples = []
    all_texts = []
    #print(category_text_dict)


    counter = 0
    for category in category_text_dict:
        #print(category)
        for person in category_text_dict[category]:
            #print(person)

            #words2, tags2 = get_words_tags(text, False)# - I tried to do without normalizing
            feature_vectors = {}

            feature_vectors.update(get_date_features(person[1]))
            if get_color_features(person[4]) is not None:
                feature_vectors.update(get_color_features(person[4]))

            #if get_color_features2(person[4]) is not None:
            #    feature_vectors.update(get_color_features2(person[4]))
            feature_vectors.update(get_picture_features(person[3]))
            #get_color_features(person[4])


            #if counter ==0:
            #print(feature_vectors)
            #counter+=1
            features_category_tuples.append((feature_vectors, category))
            #all_texts.append(text)
    print("end of get_features")
    #print(features_category_tuples)
    return features_category_tuples#, all_texts

def main():
    print("you probably running the wrong function buddy.")

if __name__ == "__main__":
    main()
