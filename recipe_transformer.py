import sys
from bs4 import BeautifulSoup
import requests

def main(recipeURL):

    r  = requests.get(recipeURL)

    data = r.text

    soup = BeautifulSoup(data, "html.parser")

    ##GET TITLE AND DESCRIPTION
    title = soup.findAll("h1", { "class" : "recipe-summary__h1" })[0].string
    print "Name: ", title
    descript = soup.findAll("div", { "class" : "submitter__description" })[0].contents[0]
    print "Description: ", descript
    ##GET THE INGREDIENTS
    ingredientsHTML = soup.findAll("li", { "class" : "checkList__line" })
    ingredientsList = []
    for i in range(0, len(ingredientsHTML)):
        ingredientsList.append(ingredientsHTML[i].findAll("span", { "class" : "recipe-ingred_txt"}))
    final_ing_list = []
    for i in range(0, len(ingredientsList)):
        final_ing_list.append(ingredientsList[i][0].string)

    types_of_measurement_list = ['teaspoon', 'cup', 'pound', 'dash', 'pinch',  'pint', 'quart', 'gallon', 'oz', 'oz.', 'liter', 'gram', 'ml', 'ounce', 'stick']
    ing_list = []
    for i in range(0, len(final_ing_list)):
        split_ing = final_ing_list[0].split()
        split_ind = 0
        for j in range(0, len(split_ing)):
            if any(keyword in split_ing[j] for keyword in types_of_measurement_list):
                split_ind = j
        ing_quant = split_ing[0:split_ind + 1]
        ing_quant = ' '.join(ing_quant)
        ing_value = split_ing[split_ind + 1:]
        ing_value = ' '.join(ing_value)
        ing_list.append([ing_quant, ing_value])

    print "Ingredients List: ", str(ing_list)

    #directionsHTML = soup.findAll("section", { "class" : "recipe-directions" })
    #print directionsHTML

    #footnotesHTML = soup.findAll("section", { "class" : "recipe-footnotes" })
    #print footnotesHTML

if __name__ == "__main__":
    recipe_url = raw_input("Please enter the URL of the recipe:")
    main(recipe_url)
