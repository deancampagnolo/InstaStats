import nltk, io, os

def detect_logos(path):
    """Detects logos in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo.description)

def detect_landmarks(path):
    """Detects landmarks in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('Latitude {}'.format(lat_lng.latitude))
            print('Longitude {}'.format(lat_lng.longitude))

def detect_labels(path):
    """Detects labels in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)

def detect_properties(path):
    """Detects image properties in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print('Properties:')

    for color in props.dominant_colors.colors:
        print('fraction: {}'.format(color.pixel_fraction))
        print('\tr: {}'.format(color.color.red))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))


def main():
    #Instagram name, date, percentage change, number of posts, pictures on that day, caption.
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\momok\Desktop\LAHacks2019\My First Project-1a0343ad2ed1.json"

    detect_logos(r"C:\Users\momok\Desktop\LAHacks2019\mickey.jpg")
    #detect_landmarks(r"C:\Users\momok\Desktop\LAHacks2019\obamaxlincoln.jpg")
    #detect_labels("C:\\Users\\momok\\Desktop\\LAHacks2019\\obama.jpg")
    #detect_properties("C:\\Users\\momok\\Desktop\\LAHacks2019\\obama.jpg")

    example1 = ["@bob", "5-7", 1, 2, "#pictures", "lmao look at my cat"]
    example2 = ["@flora", "3-2", 2, 3, "#pictures", "fuck cats amirite?"]


    the_data = []

    print("hello world")

if __name__ == "__main__":
    main()