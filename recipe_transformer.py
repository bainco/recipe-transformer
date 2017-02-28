import sys
from bs4 import BeautifulSoup
import requests

def main(recipeURL):

    r  = requests.get(recipeURL)

    data = r.text

    soup = BeautifulSoup(data, "html.parser")
    ingredientsHTML = soup.findAll("li", { "class" : "checkList__line" })
    #print "INGREDIENTS:", str(len(ingredientsHTML)), " , thing: ", str(ingredientsHTML[0].contents)

    ingredientsList = []
    for i in range(0, len(ingredientsHTML)):
    #    print ingredientsHTML[i]
        ingredientsList.append(ingredientsHTML[i].findAll("span", { "class" : "recipe-ingred_txt"}))
    #print "LIST: ", str(ingredientsList)
    final_ing_list = []
    for i in range(0, len(ingredientsList)):
        final_ing_list.append(ingredientsList[i][0].string)

    #print "FINAL LIST: ", str(final_ing_list)
    types_of_measurement_list = ['teaspoon', 'cup', 'pound', 'dash', 'pinch',  'pint', 'quart', 'gallon', 'oz', 'oz.', 'liter', 'gram', 'ml', 'ounce', 'stick']
    ing_dict = {}
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
