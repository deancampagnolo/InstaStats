import nltk, io, os, csv
from google.cloud import vision

def detect_logos(client, image):

    response = client.logo_detection(image=image)
    logos = response.logo_annotations

    return logos

def detect_landmarks(client, image):
    """Detects landmarks in the file."""

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    if len(landmarks)>0:
        return "landmark"
    #for landmark in landmarks:
        #print(landmark.description)
        #for location in landmark.locations:
         #   lat_lng = location.lat_lng
          #  print('Latitude {}'.format(lat_lng.latitude))
           # print('Longitude {}'.format(lat_lng.longitude))

def detect_labels(client, image):
    """Detects labels in the file."""


    response = client.label_detection(image=image)
    labels = response.label_annotations

    return labels

def detect_properties(client, image):


    response = client.image_properties(image=image)
    props = response.image_properties_annotation

    for color in props.dominant_colors.colors:
        print('fraction: {}'.format(color.pixel_fraction))
        print('\tr: {}'.format(color.color.red))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))

#def build_features():#FIXME look at restaurant p1 for more

def write_csv(the_list, name):
    with open(name, "w", newline="") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(the_list)
    csvFile.close()

def photo_fill(data):
    path = "PictureData/"+data[0]+"/"+data[1]+"/"
    mega_string = ""


    list_of_pictures = list(os.walk(path))[0][2]

    mega_list = []
    for picture in list_of_pictures:
        path2 = path+picture
        client = vision.ImageAnnotatorClient()

        with io.open(path2, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        labels = detect_labels(client, image)
        print(labels)
        #properties = detect_properties(path + picture)
        landmarks = detect_landmarks( client, image)
        print(landmarks)
        #logos = detect_logos(path+picture)
        #print(logos)
        if labels is not None:
            mega_list.extend(labels)

        #mega_list.extend(properties)
        if landmarks is not None:
            mega_string += landmarks+"|"
        #if logos is not None:
            #mega_list.extend(logos)

        labels = []
        properties = []
        landmarks = []
        logos = []
    print(mega_list)
    for i in mega_list:
        mega_string+=i.description+"|"
    data.append(mega_string)

    #for

    #detect_list = detect_labels(r"PictureData/bob/2019-05-07/Smash Cole.png")
def main():
    #Instagram name, date, percentage change, number of postson that day, pictures on that day, caption.
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\momok\Desktop\LAHacks2019\My First Project-1a0343ad2ed1.json"

    #detect_logos(r"C:\Users\momok\Desktop\LAHacks2019\mickey.jpg")
    #detect_landmarks(r"C:\Users\momok\Desktop\LAHacks2019\obamaxlincoln.jpg")
    #print(detect_labels("C:\\Users\\momok\\Desktop\\LAHacks2019\\obamaxlincoln.jpg"))
    #detect_properties("C:\\Users\\momok\\Desktop\\LAHacks2019\\obama.jpg")

    example1 = ['bob', '2019-05-07', '1', '2']#, '#pictures1|herp', 'lmao look at my cat']
    example2 = ['flora', '2019-03-05', '2', '3']#, '#pictures2|herp', 'fuck cats amirite?']
    example3 = ['gary', '2019-05-07', '.5', '1']#, '#pictures3|herp', 'dogz suk']
    example4 = ['biannca', '2019-05-07', '3', '4']#, '#pictures2|heyp', 'dogz r so kool']
    example5 = ['bob', '2019-05-07', '1', '2']#, '#pictures1|herp', 'lmao look at my cat']
    example6 = ['flora', '2019-05-07', '2', '3']#, '#pictures2|herp', 'fuck cats amirite?']
    example7 = ['gary', '2019-05-07', '.5', '1']#, '#pictures2|herp', 'dogz suk']
    example8 = ['biannca', '2019-05-07', '3', '4']#, '#pictures2|heyp', 'dogz r so kool']

    example_list = [example1,example2,example3,example4,example5,example6,example7,example8]

    xample1 = ['boob', '2019-05-07', '1', '2']#, '#pictures7|herp', 'lmao look at my cat']
    xample2 = ['floora', '2019-05-07', '.5', '3']#, '#pictures2|herp', 'fuck cats amirite?']
    xample3 = ['gaary', '2019-05-07', '.5', '1']#, '#pictures3|herp', 'dogz suk']
    xample4 = ['biiannca', '2019-05-07', '.5', '4']#, '#pictures2|heyp', 'dogz r so kool']
    xample5 = ['booob', '2019-05-07', '1', '2']#, '#pictures1|herp', 'lmao look at my cat']
    xample6 = ['flooora', '2019-05-07', '2', '3']#, '#pictures2|herp', 'fuck cats amirite?']
    xample7 = ['gaaary', '2019-05-07', '.5', '1']#, '#pictures2|herp', 'dogz suk']
    xample8 = ['biiiannca', '2019-05-07', '.5', '4']#, '#pictures2|heyp', 'dogz r so kool']

    xample_list = [xample1, xample2, xample3, xample4, xample5, xample6, xample7, xample8]
    print(example_list)
    write_csv(example_list, "insta_data.csv")
    write_csv(xample_list, "insta_data2.csv")
    photo_fill(example_list[0])
    print(example_list)
    #for item in example_list:
     #   photo_fill(item)
if __name__ == "__main__":
    main()