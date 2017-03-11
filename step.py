import re
import nltk
TOOLS = ["pan", "skillet", ]
PRIMARY_METHODS = ['saute', 'mix', 'heat', 'bake', 'whip', 'roast', 'grill', 'boil', 'broil', 'poach', 'fry']



def processDirection(text, ingredients):
    sentences = text.split(".")

    stepIngredients = set()
    stepTime = 0
    [p_methods, o_methods] = get_methods(text)
    for sentence in sentences:
        substep = sentence.strip().lower()
        for ingredient in ingredients:
            for word in ingredient['name'].split(" "):
                if word in substep:
                    stepIngredients.add(ingredient['name'])


        match = re.search('(\d+) minutes', substep)
        if match != None:
            stepTime += int(match.group(1))

        match = re.search('(\d+) hours', substep)
        if match != None:
            stepTime += int(match.group(1)) * 60

    stepTools = []
    stepMethod = ""
    stepTimeStr = str(stepTime) + " minutes"

    return Step(text, stepIngredients, stepTimeStr, stepTools, p_methods, o_methods)

def get_methods(text):
    text = text.strip().lower()
    text = "I " + text
    text_tokens = nltk.word_tokenize(text)
    text_pos_tagged = nltk.pos_tag(text_tokens)
    print "TEXT:", text
    print "TAGGED:", str(text_pos_tagged)

    all_methods = []
    for i in range(0, len(text_pos_tagged)):
            curr_token = text_pos_tagged[i]
            if "VB" in curr_token[1]:
                all_methods.append(curr_token[0])

    print "ALL METHODS:", str(all_methods)

    return [" ", " "]
        # CHECK FOR INGREDIENTS BY COMPARING TO INGREDIENTS LISTYL



class Step:
    def __str__(self):
        result = ""
        result += "text: " + str(self.text) + '\n'
        result += "ingredients: " + str(self.ingredients) + "\n"
        result += "time: " + str(self.time) + "\n"
        result += "tools: " + str(self.tools) + "\n"
        result += "Cooking method: " + str(self.method) + "\n"
        result += "Other methods: " + str(self.other_methods) + "\n"
        return result

    def __init__(self, text, ingredients, time, tools, method, other_methods):
        self.text = text
        self.ingredients = ingredients
        self.time = time
        self.tools = tools
        self.method = method
        self.other_methods = other_methods
