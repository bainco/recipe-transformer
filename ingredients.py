import sys
from bs4 import BeautifulSoup
import requests
import nltk


types_of_measurement_list = ['teaspoon', 'cup', 'pound', 'dash', 'pinch',  'pint', 'quart', 'gallon', ' oz', 'liter', 'gram', 'ml', 'ounce', 'stick', 'can', 'jar', 'lb', 'package']
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

        ing_quantity = validate_quant(ing_quantity)

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
        # print "SPLIT Q", str(split_q), ", J:", str(q_ind)
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

    [ing_name, ing_descript] = split_name(ing_name)
    return [ing_name, ing_descript, ing_preparation]

def split_name(nd):
    # print "ND:", nd
    nd = "This is " + nd + "."
    nd_tokens = nltk.word_tokenize(nd)
    nd_tagged = nltk.pos_tag(nd_tokens)
    # print "NAME DESCRIPT:", str(nd_tagged)
    name = ""
    description = ""
    print "TAGGED: ", str(nd_tagged)
    for i in range(2, len(nd_tagged) - 1):
        if "NN" in nd_tagged[i][1]:
            name = name + nd_tagged[i][0] + " "
        else:
            description = description + nd_tagged[i][0] + " "
    return [name, description]

def validate_quant(some_quant):
    if "/" in some_quant:
        
        position = some_quant.index("/")
        numerator = some_quant[position - 1]
        denominator = some_quant[position + 1]
        fraction = float(numerator) / float(denominator)
        print "FLOAT:", some_quant[:position - 1].strip()
        base = 0.0
        if some_quant[:position - 1] != '':
            base = float(some_quant[:position - 1].strip())
        return str(base + fraction)
        
    else:
        return some_quant
