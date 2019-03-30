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
    for item in a_list:
        print(item)
        print()
        print(i)
        i +=1




if __name__ == "__main__":
    main()