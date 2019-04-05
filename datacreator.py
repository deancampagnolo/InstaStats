
from bs4 import BeautifulSoup
import requests
import string
import subprocess
import instagram_scraper


def main():
    COMPUTE_NUMBER = 499
    skip = [55, 70 , 120, 121,122,123,124,125,126, 127, 128, 129, 163, 195, 198, 233, 234, 235, 242, 304, 305, 306, 375, 376, 377, 386, 476, 477, 478, 479, 486]

    #main function
    n = "https://socialblade.com/instagram/top/500/followers"


    page = requests.get(n)
    print(page.status_code)

    soup = BeautifulSoup(page.content, 'html.parser')

    a_list = (soup.find_all('a'))
    i = 0
    listofnames = []
    for item in a_list:
        i +=1
        if i >= 130 and i <= 629:
            Name = (a_list[i].get_text())
            #print(Name)
            url = (a_list[i].get('href'))
            #print(url)
            username = (url.split("/",4)[-1])
            #print(username)
            #print()
            listofnames.append(username)

    length = len(listofnames)
    #print(length)
    for i in range(length):
        #print((length-1)-i)
        if ((length-1) - i) in skip:
            del listofnames[((length-1) - i)]

    print(len(listofnames))
    #print("hhhhh")
    b = []
    for number in range(len(listofnames)):
        b.append(14)

    actlistofnames = []
    for x, y in zip(listofnames, b):
        actlistofnames.extend([x] * y)

    print(len(actlistofnames))

    listofwebsites = []
    for i in listofnames:
        m = "https://socialblade.com/instagram/user/" + i
        listofwebsites.append(m)
    listofdates = []
    listofpercentchange = []
    listofnumberofuploads = []

    z = 0
    #print(listofwebsites)
    for i in listofwebsites:
        #print(i)
        #print(z)
        z+=1
    #print(len(listofwebsites))
    z=0
    for i in range(len(listofnames)):

        the_dates, the_percent_change, number_of_uploads = Get_Dates(listofwebsites[i])
       #print(number_of_uploads)
        #print("NUMBBY")
        print(i)
        listofdates.append(the_dates)
        listofpercentchange.append(the_percent_change)
        listofnumberofuploads.append(number_of_uploads)
        #print(z)
        z+=1
    #print("fuck yeah!")
    actuallistofdates = []
    actuallistofpercentchange = []
   # print(listofdates)
    for item in listofdates:
        for date in item:
            actuallistofdates.append(date)

    for item in listofpercentchange:
        for percent in item:
            actuallistofpercentchange.append(percent)
    #print(actuallistofdates)





    compiledlist = []
    for i in range((len(listofnames)*14)-14):
        print(i)
        indivlist = []
        indivlist.append(actlistofnames[i])
        indivlist.append(actuallistofdates[i])
        indivlist.append(actuallistofpercentchange[i])
        compiledlist.append(indivlist)

    return compiledlist #FIXME delete this later if you want to download more photos
    prefix_instagram = "https://ingram.life/u/"
    #chromedriver = r"chromedriver.exe"
    #browser = webdriver.Chrome(chromedriver)
    #browser.get(prefix_instagram+"therock")

    prefix = "instagram-scraper "
    my_username = " -u dean_campo -p DeanCole1 --maximum "
    naming_convention = " -t image -T {date} --retry-forever -d ./photos/"


    for i in range(len(listofnames)):

        command = prefix + listofnames[i] +my_username+str(listofnumberofuploads[i])+naming_convention+listofnames[i] #listofnumberofuploads[i]
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    counter = 0
    big_counter = 0
    for data in compiledlist:

        if counter == 13:
            instagram_name = listofnames[big_counter]









def Get_Dates(website):
    listofdates = []
    page = requests.get(website)

    soup = BeautifulSoup(page.content, 'html.parser')

    listofdates = []
    listofpercentchange = []
    # print(soup.prettify())
    dateblob = soup.find_all('div', attrs={
        'style': 'width: 880px; background: #fff; padding: 0px; color:#444; font-size: 10pt;'})
    e = 0
    legitchildren = []

    number_of_uploads= 0
    for item in dateblob[0].children:
        if e % 2 == 1:
            legitchildren.append(item)
        e = e + 1
        # print("\n")
    for item in range(14):
        #print(item)
        #print(legitchildren[item].prettify())
        website = list(list(legitchildren[item].children)[1].children)[1]
        listofdates.append(website.text)
        zz = 0

        if item == 0:
            listofpercentchange.append("0")
        else:
            change = list(list(legitchildren[item].children)[3].children)[1].text[1:].translate(str.maketrans('','',string.punctuation))#skips first character which is '+'
            followers = list(list(legitchildren[item].children)[3].children)[3].text.translate(str.maketrans('','',string.punctuation))
            listofpercentchange.append(str(float(change)/float(followers)))

        uploads =list(list(legitchildren[item].children)[7].children)[1].text
        #print(uploads)
        if uploads[0] == '+':
            number_of_uploads += int(uploads[1:].translate(str.maketrans('','',string.punctuation)))
        #print(legitchildren[item])
        #print("chi")

    return listofdates,listofpercentchange, number_of_uploads

if __name__ == "__main__":
    #Get_Dates("https://socialblade.com/instagram/user/therock")
    main()