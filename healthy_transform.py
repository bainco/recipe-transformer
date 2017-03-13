from measure_standardizer import *

MEATS = ['pork', 'chicken', 'beef', 'turkey', 'steak']
BAKE_FAT_REPLACE = ['butter', 'lard', 'shortening']
PASTA_TYPES = ['spaghetti', 'linguini', 'macaroni', 'farfalle', 'penne', 'orzo', 'ravioli', 'fettucine',
    'rigatoni', 'tortellini', 'rotini', 'lasagna', 'manicotti']

def transform_healthy(ingredients, directions, primary_methods):

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
            if 'sugar' in ingredients[i]['name']:
                ingredients[i]['quant'] = float(ingredients[i]['quant']) / 2
                ingredients.append({"name" : 'allspice', "quant" : 2, "preparation": "", "measurement" : "teaspoon", "description" : ""})
                ingredients.append({"name" : 'vanilla extract', "quant" : 1, "preparation": "", "measurement" : "teaspoon", "description" : ""})
                directions = updateDirections(directions, "sugar", "allspice", False)
                directions = updateDirections(directions, "sugar", "allspice", False)

        # process applesauce replacements
        if replacement_amount:
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
        if 'pasta' in ingredients[i]['name']:
            directions = updateDirections(directions, ingredients[i]['name'], "whole-wheat " + ingredients[i]['name'], True)
            ingredients[i]['name'] = "whole-wheat " + ingredients[i]['name']

        # halve any uses of cheese
        if 'cheese' in ingredients[i]['name']:
            ingredients[i]['quant'] = float(ingredients[i]['quant']) / 2

        # Replace rice with brown rice
        if ('rice' in ingredients[i]['name']) and ('brown' not in ingredients[i]['name']):
            directions = updateDirections(directions, ingredients[i]['name'], "whole-wheat " + ingredients[i]['name'], True)
            ingredients[i]['name'] = 'brown rice'

        # Replace milk with fat-free
        if ('milk' in ingredients[i]['name']) and ('skim' not in ingredients[i]['name']):
            directions = updateDirections(directions, ingredients[i]['name'], "skim milk", True)
            ingredients[i]['name'] = 'skim milk'

        # trim fat from meats
        if any(ck in ingredients[i]['name'] for ck in MEATS):
            ingredients[i]['name'] += " (with fat trimmed)"

        # skinless for all chicken
        if ('chicken' in ingredients[i]['name']) and ('skinless' not in ingredients[i]['name']):
            ingredients[i]['name'] += " (skinless)"

    return (ingredients, directions)

def updateDirections(directions, old_ingredient, new_ingredient, remove):
    for i in range(len(directions)):
        for j in range(len(directions[i].ingredients)):
            if directions[i].ingredients[j] == old_ingredient:
                directions[i].ingredients.add(new_ingredient)
                if remove:
                    directions[i].ingredients.remove(directions[i].step.ingredients[j])
                    directions[i].text.replace(old_ingredient, new_ingredient)
                else:
                    directions[i].text.replace(old_ingredient, (old_ingredient + " and " + new_ingredient))

    return directions
