import sys
from bs4 import BeautifulSoup
import requests

def main():
    if len(sys.argv) != 2:
        print "input error."
        sys.exit(0)

    recipeURL = str(sys.argv[1])

    r  = requests.get(recipeURL)

    data = r.text

    soup = BeautifulSoup(data, "html.parser")

    ingredientsHTML = soup.findAll("section", { "class" : "recipe-ingredients" })
    print ingredientsHTML

    directionsHTML = soup.findAll("section", { "class" : "recipe-directions" })
    print directionsHTML

    footnotesHTML = soup.findAll("section", { "class" : "recipe-footnotes" })
    print footnotesHTML

if __name__ == "__main__":
    main()
