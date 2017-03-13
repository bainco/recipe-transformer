from flask import Flask
from flask import render_template
from recipe_transformer import *

app = Flask(__name__)

@app.route("/")
def hello():
    [title, descript, ingredients, prepTime, cookTime, readyTime, tool_list, primary_methods, other_methods, processedSteps] = parse_recipe('')
    
    tl = tool_list.split(",")
    return render_template('index.html', recipe_url = "has url", title = title, description = descript, ingredients = ingredients, prepTime = prepTime, cookTime = cookTime, readyTime = readyTime, tool_list = tl)

@app.route("/<recipe_url>")
def p_recipe(recipe_url):
    print "RECIPE: ", recipe_url
    [title, descript, ingredients, prepTime, cookTime, readyTime, tool_list, primary_methods, other_methods, processedSteps] = parse_recipe(recipe_url)

    print "ING:", str(ingredients)
    return render_template('index.html', recipe_url = recipe_url)


if __name__ == "__main__":
    app.run()
