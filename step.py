import re
TOOLS = ["pan", "skillet", ]
METHODS = ['saute', 'mix', 'heat', 'bake', 'whip', 'roast', 'grill', 'boil', '']



def processDirection(text, ingredients):
    sentences = text.split(".")

    stepIngredients = set()
    for sentence in sentences:
        substep = sentence.strip().lower()
        for ingredient in ingredients:
            for word in ingredient['name'].split(" "):
                if word in substep:
                    stepIngredients.add(ingredient['name'])

        stepTime = 0
        match = re.search('(\d+) minutes', substep)
        if match:
            stepTime += int(match.group(1))
        match = re.search('(\d+) hours', substep)
        if match:
            stepTime += int(match.group(1)) * 60

    stepTools = []
    stepMethod = ""

    return Step(text, stepIngredients, stepTime, stepTools, stepMethod)


        # CHECK FOR INGREDIENTS BY COMPARING TO INGREDIENTS LISTYL



class Step:
    def __str__(self):
        result = ""
        result += "text: " + str(self.text) + '\n'
        result += "ingredients: " + str(self.ingredients) + "\n"
        result += "time: " + str(self.time) + "\n"
        result += "tools: " + str(self.tools) + "\n"
        result += "method: " + str(self.method) + "\n"
        return result

    def __init__(self, text, ingredients, time, tools, method):
        self.text = text
        self.ingredients = ingredients
        self.time = time
        self.tools = tools
        self.method = method
