import re
import nltk
from nltk.chunk.regexp import *
TOOLS = ["pan", "skillet", "oven", "baking pan", "pot", "slotted spoon", "spoon", "dish", "knife", "collander", "baking sheet", "bowl", "whisk", "grater"]
PRIMARY_METHODS = ['saute', 'mix', 'heat', 'bake', 'whip', 'roast', 'grill', 'boil', 'broil', 'poach', 'fry', 'preheat']
CUTTING_KEYWORDS = ['cut', 'chop', 'slice', 'dice', 'julienne']

# regex_p = RegexpParser('''
#          NP: {<DT>? <JJ>* <NN>*}
#          P: {<IN>}
#          V: {<V.*>}
#          PP: {<P> <NP>}
#          VP: {<V> <NP|PP>*}
#          ''')

def processDirection(text, number, ingredients, tool_list, pm, om):
    sentences = text.split(".")

    stepIngredients = set()
    stepTime = 0
    all_methods = []
    stepTools = set()
    for sentence in sentences:
        substep = sentence.strip().lower()
        for ingredient in ingredients:
            for word in ingredient['name'].split(" "):
                if word in substep:
                    stepIngredients.add(ingredient['name'][:len(ingredient['name']) - 1])


        match = re.search('(\d+) minutes', substep)
        if match != None:
            stepTime += int(match.group(1))

        match = re.search('(\d+) hours', substep)
        if match != None:
            stepTime += int(match.group(1)) * 60

        [all_methods, stepTools] = get_methods(substep, all_methods, stepTools)

    stepMethod = ""
    stepTimeStr = str(stepTime) + " minutes"
    stepIngredients = list(stepIngredients)[1:]
    stepIngredientsStr = ""
    for i in stepIngredients:
        stepIngredientsStr = stepIngredientsStr + i + ", "
    stepIngredientsStr = stepIngredientsStr[:len(stepIngredientsStr) - 2]
    [p_methods, o_methods] = split_methods(all_methods)
    if p_methods != "":
        pm = pm + ", " + p_methods
    if o_methods != "":
        om = om + ", " + o_methods
    stepTools = list(stepTools)
    stepToolsStr = ""
    for s in stepTools:
        stepToolsStr += s + ", "
    stepToolsStr = stepToolsStr[:len(stepToolsStr) - 2]
    tool_list = tool_list + ", " + stepToolsStr

    return [Step(text, number, stepIngredientsStr, stepTimeStr, stepToolsStr, p_methods, o_methods), tool_list, pm, om]

def get_methods(text, all_methods, stepTools):
    text = text.strip().lower()
    text = "I " + text
    # print "TEXT: ", text
    text_tokens = nltk.word_tokenize(text)
    for t in text_tokens:
        if t in TOOLS:
            stepTools.add(t)
    text_pos_tagged = nltk.pos_tag(text_tokens)

    # print "T_TOKENS: ", text_pos_tagged

    for i in range(0, len(text_pos_tagged)):
            curr_token = text_pos_tagged[i]
            if ('VB' in curr_token[1]) and (curr_token[1] != 'VBD') and (curr_token[1] != 'VBN'):
                if len(curr_token[0]) > 2:
                    all_methods.append(curr_token[0])
            if curr_token[0] == 'brown' or curr_token[0] == 'drain':
                all_methods.append(curr_token[0])
    
    for m in all_methods:
        if 'drain' in m:
            stepTools.add('collander')
        if any(ck in m for ck in CUTTING_KEYWORDS):
            stepTools.add('knife')

    return [all_methods, stepTools]

def split_methods(methods):
    p_methods = "" #primary cooking methods
    o_methods = "" #secondary cooking methods

    for m in methods:
        if m in PRIMARY_METHODS:
            p_methods = p_methods + m + ", "
        else:
            o_methods = o_methods + m + ", "

    return [p_methods[:len(p_methods) - 2], o_methods[:len(o_methods) - 2]]
        # CHECK FOR INGREDIENTS BY COMPARING TO INGREDIENTS LISTYL


class Step:
    def __str__(self):
        result = ""
        result += "Step " + str(self.number) + ": " + str(self.text) + '\n'
        result += "    Ingredients: " + str(self.ingredients) + "\n"
        result += "    Time: " + str(self.time) + "\n"
        result += "    Tools: " + str(self.tools) + "\n"
        result += "    Cooking method(s): " + str(self.method) + "\n"
        # result += "    Other methods: " + str(self.other_methods) + "\n"
        return result

    def __init__(self, text, number, ingredients, time, tools, method, other_methods):
        self.text = text
        self.number = number + 1
        self.ingredients = ingredients
        self.time = time
        self.tools = tools
        # self.method = method + other_methods
        self.method = ""
        if method != "":
            self.method = method
        if other_methods != "":
            if self.method == "":
                self.method = other_methods
            else:
                self.method = self.method + ", " + other_methods

        # self.other_methods = other_methods
