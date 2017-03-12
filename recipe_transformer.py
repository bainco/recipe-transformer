import sys
from bs4 import BeautifulSoup
import requests
from step import *
from ingredients import *

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

    ##GET THE REVIEW SENTIMENT
    review_sentiment = get_review_sentiment(soup)
    print round(review_sentiment[0], 1), "percent of users reviewed it positively"
    print round(review_sentiment[1], 1), "percent of users reviewed it neutrally"
    print round(review_sentiment[2], 1), "percent of users reviewed it negatively\n"

    ##GET THE NUMBER OF SERVINGS
    num_servings = get_num_servings(soup)
    print "Number of servings: " + num_servings

    ##GET NUTRITION INFO
    print "Nutritional information per serving:"
    nutrition = soup.findAll("div", { "class" : "recipe-nutrition__form" })[0]
    calories = get_nutrition_info(soup, nutrition, "calories")
    print "\tCalories: " + calories[0] + calories[1] + " (" + calories[2] + ")"
    fat = get_nutrition_info(soup, nutrition, "fatContent")
    print "\tFat: " + fat[0] + fat[1] + " (" + fat[2] + ")"
    carbs = get_nutrition_info(soup, nutrition, "carbohydrateContent")
    print "\tCarbs: " + carbs[0] + carbs[1] + " (" + carbs[2] + ")"
    protein = get_nutrition_info(soup, nutrition, "proteinContent")
    print "\tProtein: " + protein[0] + protein[1] + " (" + protein[2] + ")"
    cholesterol = get_nutrition_info(soup, nutrition, "cholesterolContent")
    print "\tCholesterol: " + cholesterol[0] + cholesterol[1] + " (" + cholesterol[2] + ")"
    sodium = get_nutrition_info(soup, nutrition, "sodiumContent")
    print "\tSodium: " + sodium[0] + sodium[1] + " (" + sodium[2] + ")\n"

    ##GET THE INGREDIENTS
    ingredients = get_ingredients(soup)
    for i in ingredients:
        print "Name:", i['name']
        print "    Quantity:", i['quant']
        print "    Measurement:", i['measurement']
        print "    Preparation:", i['preparation']
        print "    Description:", i['description']


    steps, prepTime, cookTime, readyTime = get_directions(soup)

    print ""
    print "Prep Time:", prepTime, "minutes"
    print "Cook Time:", cookTime, "minutes"
    print "Ready Time:", readyTime, "minutes"
    print ""

    # print "Directions:"
    i = 0
    processedSteps = []
    tool_list = ""
    primary_methods = ""
    other_methods = ""
    # for step in steps:
    for i in range(0, len(steps)):
        # print "Step", (str(i) + ".")
        # print step, "\n"
        [processed_step, tool_list, primary_methods, other_methods] = processDirection(steps[i], i, ingredients, tool_list, primary_methods, other_methods) 
        processedSteps.append(processed_step)
        i += 1
    
    print "Tools:", str(tool_list[2:]), "\n"
    print "Primary Methods:", primary_methods[2:]
    print "Other Methods:", other_methods[2:], "\n"
    print "Directions"
    for pstep in processedSteps:
        print str(pstep)

    # footnotesHTML = soup.findAll("section", { "class" : "recipe-footnotes" })
    # print footnotesHTML
    return 0

def get_directions(theSoup):
    ##GET THE DIRECTIONS
    times = theSoup.findAll("span", { "class": "prepTime__item--time" })
    prepTime = times[0].contents[0]
    cookTime = times[1].contents[0]
    if len(times) > 3:
        readyTime = (int(times[2].contents[0])*60) + int(times[3].contents[0])
    else:
        readyTime = int(times[2].contents[0])

    stepsHTML = theSoup.findAll("span", { "class" : "recipe-directions__list--item" })
    steps = []
    for span in stepsHTML:
        if span.contents:
            steps.append(span.contents[0])

    return steps, prepTime, cookTime, readyTime


def get_title_and_descript(soup):
    title = soup.findAll("h1", { "class" : "recipe-summary__h1" })[0].string
    descript = soup.findAll("div", { "class" : "submitter__description" })[0].contents[0]
    descript = descript[3:len(descript) - 4]

    return [title, descript]

def get_num_servings(soup):
    num_servings = soup.findAll("meta", { "id" : "metaRecipeServings" })[0]['content']
    return num_servings

def get_nutrition_info(soup, nutrition, itemprop):
    info_header = nutrition.findAll("li", { "itemprop" : itemprop })[0].parent
    info = info_header.findAll("li", { "itemprop" : itemprop })[0].contents[0].string
    info_unit = info_header.findAll("li", { "itemprop" : itemprop })[0].contents[1].string
    info_percent = info_header.findAll("li", { "class" : "nutrientLine__item--percent"})[0].string
    return [info, info_unit, info_percent]

def get_review_sentiment(soup):
    review_header = soup.findAll("section", { "id" : "reviews"})[0].ol
    total = int(review_header.contents[1].h4.string.split(" ")[0])
    love = int(review_header.findAll("div", { "data-ratingstars" : "5" })[0].parent["title"].split(" ")[0])
    like = int(review_header.findAll("div", { "data-ratingstars" : "4" })[0].parent["title"].split(" ")[0])
    ok = int(review_header.findAll("div", { "data-ratingstars" : "3" })[0].parent["title"].split(" ")[0])
    noLike = int(review_header.findAll("div", { "data-ratingstars" : "2" })[0].parent["title"].split(" ")[0])
    cantEat = int(review_header.findAll("div", { "data-ratingstars" : "1" })[0].parent["title"].split(" ")[0])
    total_positive = love + like
    total_neutral = ok
    total_negative = noLike + cantEat
    return [100*total_positive/float(total), 100*total_neutral/float(total), 100*total_negative/float(total)]

if __name__ == "__main__":
    # recipe_url = raw_input("Please enter the URL of the recipe:")
    test_r1 = 'http://allrecipes.com/recipe/15268/cajun-dirty-rice/?internalSource=staff%20pick&referringId=192&referringContentType=recipe%20hub&clickId=cardslot%205'
    test_r2 = 'http://allrecipes.com/recipe/87845/manicotti-italian-casserole/?internalSource=popular&referringContentType=home%20page&clickId=cardslot%207'
    main(test_r2)
