import selenium
from bs4 import BeautifulSoup
import requests


def main():
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
            print(Name)
            url = (a_list[i].get('href'))
            print(url)
            username = (url.split("/",4)[-1])
            print(username)
            print()
            listofnames.append(username)

    listofwebsites = []
    for i in listofnames:
        m = "https://socialblade.com/instagram/user/" + i
        listofwebsites.append(m)
    print(listofwebsites)

    h = "https://socialblade.com/instagram/user/therock"
#for i in range(len(listofwebsites)):
#listofwebsites[i] instead of h
    page = requests.get(h)
    print(page.status_code)





    compiledlist = []
    for i in range(len(listofnames)):
        indivlist = []
        indivlist.append(listofnames[i])
        indivlist.append("date")
        indivlist.append("percentchange")
        indivlist.append("hotposts")
        indivlist.append("pics")
        indivlist.append("captions")
        compiledlist.append(indivlist)


    print(listofnames)
    print(compiledlist)









if __name__ == "__main__":
    main()