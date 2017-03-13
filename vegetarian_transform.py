from measure_standardizer import *
from healthy_transform import updateDirections

FORBIDDEN = ['beef stock',
             'chicken stock',
             'wild meat',
             'sour cream',
             'ice cream',
             'chicken nuggets',
             'pork', 
             'chicken', 
             'beef', 
             'turkey', 
             'steak', 
             'lamb', 
             'veal',  
             'venison', 
             'goose', 
             'duck', 
             'quail',
             'fish', 
             'shrimp', 
             'scallops', 
             'crab', 
             'lobster', 
             'clam',
             'milk',
             'yogurt',
             'cheese',
             'butter',
             'eggs',
             'honey',
             'yogurt',
             'mayonnaise',
             'gelatin',
             'hamburger',
             'chocolate',
             'pepperoni',
             'sausage']

REPLACEMENT = {'milk' : 'soymilk',
               'cheese' : 'vegan cheese',
               'eggs' : 'tofu',
               'butter' : 'vegan margarine',
               'yogurt' : 'soy yogurt',
               'sour cream' : 'plain soy yogurt',
               'mayonnaise' : 'vegan mayonnaise',
               'gelatin' : 'agar powder',
               'honey' : 'liquid FruitSource',
               'sugar' : 'unbleached cane sugar',
               'chocolate' : 'non-dairy chocolate',
               'ice cream' : 'fruit sorbet',
               'pork' : 'tofu', 
               'chicken' : 'tofu',
               'beef' : 'tofu',
               'turkey' : 'tofu',
               'steak' : 'tofu',
               'lamb' : 'tofu',
               'veal' : 'tofu',
               'wild meat' : 'tofu',
               'venison' : 'tofu',
               'goose' : 'tofu',
               'duck' : 'tofu',
               'quail' : 'tofu',
               'fish' : 'tofu',
               'shrimp' : 'tofu',
               'scallops' : 'tofu',
               'crab' : 'tofu',
               'lobster' : 'tofu',
               'clam' : 'tofu',
               'hamburger' : 'veggie burger',
               'chicken nuggets' : 'soy chicken nuggets',
               'pepperoni' : 'tofu',
               'sausage' : 'tofu'}

def vegan_transform(ingredients, directions):
    for i in range(len(ingredients)):
        for bad in FORBIDDEN:
            if bad in ingredients[i]['name']:
                if bad not in REPLACEMENT.keys():
                    directions = updateDirections(directions, ingredients[i]['name'], "(No suitable replacement) OMIT " + ingredients[i]['name'], True)
                    ingredients[i]['name'] = "(No suitable replacement) OMIT " + ingredients[i]['name']
                else:
                    directions = updateDirections(directions, ingredients[i]['name'], REPLACEMENT[bad], True)
                    ingredients[i]['name'] = REPLACEMENT[bad]
    return (ingredients,directions)