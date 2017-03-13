from measure_standardizer import *

MEATS = ['pork', 'chicken', 'beef', 'turkey', 'steak']
BAKE_FAT_REPLACE = ['butter', 'lard', 'shortening']
PASTA_TYPES = ['spaghetti', 'linguini', 'macaroni', 'farfalle', 'penne', 'orzo', 'ravioli', 'fettucine',
    'rigatoni', 'tortellini', 'rotini', 'lasagna', 'manacotti']

def healhty_transform(ingredients, directions):
    #TODO: HOW DO WE DEAL WITH UPDATING DIRECTIONS?
    if "bake" in primary_methods:
        replacement_amount = []
        for i in range(len(ingredients)):
            # # If baking, replace 1/2 of the amount of any BAKE_FAT_REPLACE with applesauce
            for item in BAKE_FAT_REPLACE:
                if item in ingredients[i]['name']:
                    ingredients[i]['quant'] = float(ingredients[i]['quant']) / 2
                    replacement_amount.append((ingredients[i]['quant'], ingredients[i]['measurement']))
                    directions = updateDirections(directions, item, "applesauce")

            # If sugar, replace 1/2 with 1tsp of allspice and 1tsp of Vanilla Extract
            if 'sugar' in ingredient[i]['name']:
                ingredients[i]['quant'] = float(ingredients[i]['quant']) / 2
                ingredients.append({"name" : 'allspice', "quant" : 2, "preparation": "", "measurement" : "teaspoon", "description" : ""})
                ingredients.append({"name" : 'vanilla extract', "quant" : 1, "preparation": "", "measurement" : "teaspoon", "description" : ""})
                directions = updateDirections(directions, "sugar", "allspice")
                directions = updateDirections(directions, "sugar", "allspice")

        # process applesauce replacements
        actual_amount = 0
        for quant, measurement in replacement_amount:
            actual_amount += standardize_measurement(quant, measurement)
        ingredients.append({"name" : 'applesauce', "quant" : actual_amount, "preparation": "", "measurement" : "oz", "description" : ""})

    # Remove most salt (or 1/3) if NOT BAKING
    else:
        for i in range(len(ingredients)):
            if 'salt' in ingredients[i]['name']:
                ingredients[i]['quant'] = float(ingredients[i]['quant']) / 3

    for i in range(len(ingredients)):
        # replace pasta with whole-wheat pasta
        if ingredients[i]['name'] in PASTA_TYPES:
            updateDirections(directions, ingredients[i]['name'], "whole-wheat " + ingredients[i]['name'])
            ingredients[i]['name'] = "whole-wheat " + ingredients[i]['name']

        # halve any uses of cheese
        if 'cheese' in ingredients[i]['name']:
            ingredients[i]['quant'] = float(ingredients[i]['quant']) / 2

        # Replace rice with brown rice
        if ('rice' in ingredients[i]['name']) and ('brown' not in ingredients[i]['name']):
            directions = updateDirections(directions, ingredients[i]['name'], "whole-wheat " + ingredients[i]['name'])
            ingredients[i]['name'] = 'brown rice'

        # Replace milk with fat-free
        if ('milk' in ingredients[i]['name']) and ('skim' not in ingredients[i]['name']):
            directions = updateDirections(directions, ingredients[i]['name'], "skim milk")
            ingredients[i]['name'] = 'skim milk'

        # trim fat from meats
        if any(ck in ingredient[i]['name'] for ck in MEATS):
            ingredients[i]['name'] += " (with fat trimmed)"

        # skinless for all chicken
        if ('chicken' in ingredients[i]['name']) and ('skinless' not in ingredients[i]['name']):
            ingredients[i]['name'] += " (skinless)"

    return (ingredients, directions)

def updateDirections(directions, old_ingredient, new_ingredient, remove):
    for i in range(len(directions)):
        for j in range(len(directions[i].step.ingredients)):
            if directions[i].step.ingredients[j] == old_ingredient:
                directions[i].step.ingredients.add(new_ingredient)
                if remove:
                    directions[i].step.ingredients.remove(directions[i].step.ingredients[j])
                    directions[i].step.text.replace(old_ingredient, new_ingredient)
                else:
                    directions[i].step.text.replace(old_ingredient, (old_ingredient + " and " + new_ingredient))

    return directions
