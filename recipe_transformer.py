import sys
from bs4 import BeautifulSoup
import requests

types_of_measurement_list = ['teaspoon', 'cup', 'pound', 'dash', 'pinch',  'pint', 'quart', 'gallon', ' oz', 'liter', 'gram', 'ml', 'ounce', 'stick', 'can', 'jar', 'lb', 'package']

def main(recipeURL):

    r  = requests.get(recipeURL)

    data = r.text

    soup = BeautifulSoup(data, "html.parser")

    ##GET TITLE AND DESCRIPTION
    [title, descript] = get_title_and_descript(soup)
    print "Title - ", title
    print "Description: ", descript
    print " "
    ##GET THE INGREDIENTS
    ingredients = get_ingredients(soup)
    for i in ingredients:
        print "Name:", i['name']
        print "    Quantity:", i['quant']
        print "    Measurement:", i['measurement']
        print "    Preparation:", i['preparation']
        print "    Description:", i['description']

    ##GET THE DIRECTIONS
    directionsHTML = soup.findAll("section", { "class" : "recipe-directions" })
    # print directionsHTML

    # footnotesHTML = soup.findAll("section", { "class" : "recipe-footnotes" })
    # print footnotesHTML
    return 0

def get_title_and_descript(soup):
    title = soup.findAll("h1", { "class" : "recipe-summary__h1" })[0].string
    descript = soup.findAll("div", { "class" : "submitter__description" })[0].contents[0]
    descript = descript[3:len(descript) - 4]

    return [title, descript]

def get_ingredients(soup):
    ingredientsHTML = soup.findAll("li", { "class" : "checkList__line" })
    ingredientsList = []
    for i in range(0, len(ingredientsHTML)):
        ingredientsList.append(ingredientsHTML[i].findAll("span", { "class" : "recipe-ingred_txt"}))
    final_ing_list = []
    for i in range(0, len(ingredientsList)):
        final_ing_list.append(ingredientsList[i][0].string)

    final_ing_list = final_ing_list[0: len(final_ing_list) - 3]
    ing_list = []
    print "Ingredients"
    for i in range(0, len(final_ing_list)):
        split_ing = final_ing_list[i].split()
        split_ind_quant_value = 0

        ing_name = 'None'
        ing_quantity = 'None'
        ing_measurement = 'None'
        ing_descript = 'None'
        ing_preparation = 'None'
        #split each ingredient into quant(amount), and value(everything else)
        for j in range(0, len(split_ing)):
            if any(keyword in split_ing[j] for keyword in types_of_measurement_list):
                split_ind_quant_value = j

        ing_quant = split_ing[0:split_ind_quant_value + 1]
        ing_value = split_ing[split_ind_quant_value + 1:]
        ing_quant = ' '.join(ing_quant)
        ing_value = ' '.join(ing_value)

        [ing_quantity, ing_measurement] = get_qm_from_quant(ing_quant)
        [ing_name, ing_descript, ing_preparation] = split_ing_value(ing_value)

        curr_ing = {"name" : ing_name, "quant" : ing_quantity, "preparation": ing_preparation, "measurement" : ing_measurement, "description" : ing_descript}
        ing_list.append(curr_ing)

    return ing_list

def get_qm_from_quant(quant):
    ing_quantity = 'None'
    ing_measurement = 'None'
    split_q = quant.split()
    # print "SPLIT Q", str(quant)
    q_ind = 0
    paren_start = -1
    paren_end = -1
    paren_start_types = ['(', '{', '[']
    paren_end_types = [')', '}', ']']
    for j in range(0, len(split_q)):
        if any(keyword in split_q[j] for keyword in paren_start_types):
            paren_start = j
        if any(keyword in split_q[j] for keyword in paren_end_types):
            paren_end = j
        if any(keyword in split_q[j] for keyword in types_of_measurement_list):
            q_ind = j
    if q_ind == 0:
        ing_quantity = " "
        ing_measurement = " "
        return [ing_quantity, ing_measurement]
    if paren_start != -1:
        ing_quantity = ' '.join(quant[0:paren_start])
        ing_measurement = quant[paren_start:]
    else:
        print "SPLIT Q", str(split_q), ", J:", str(q_ind)
        ing_quantity = ' '.join(split_q[0:q_ind])
        ing_measurement = ' '.join(split_q[q_ind:])
    return [ing_quantity, ing_measurement]

def split_ing_value(ing_value):
    ing_name = 'None'
    ing_descript = 'None'
    ing_preparation = 'None'

    split_ind_comma = ing_value.find(',')
    if split_ind_comma == -1:
        ing_name = ing_value
        ing_preparation = 'None'
    else:
        ing_name = ing_value[0: split_ind_comma + 1]
        ing_preparation = ing_value[split_ind_comma + 1 :]
    return [ing_name, ing_descript, ing_preparation]

if __name__ == "__main__":
    # recipe_url = raw_input("Please enter the URL of the recipe:")
    test_r1 = 'http://allrecipes.com/recipe/15268/cajun-dirty-rice/?internalSource=staff%20pick&referringId=192&referringContentType=recipe%20hub&clickId=cardslot%205'
    test_r2 = 'http://allrecipes.com/recipe/87845/manicotti-italian-casserole/?internalSource=popular&referringContentType=home%20page&clickId=cardslot%207'
    main(test_r2)
