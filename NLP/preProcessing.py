from NLP.imports import *


nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)


def expandContractions(text):
    sentence = ""
    words = re.split(" |:|;", text)
    for i in range(len(words)):
        if words[i].casefold() in CONTRACTION_MAP:
            words[i] = CONTRACTION_MAP[words[i].casefold()]
        sentence = sentence+" "+words[i]
    return sentence


def textReplacer(text):
    screenDict = {}
    inputDict = {}
    elementText = r"\{.*?\}"
    inputText = r"\'.*?\'"
    i = 0
    txtSize = len(text)
    for match in re.finditer(elementText, text):

        start, end = match.span()
        start = start - (txtSize - len(text))
        end = end - (txtSize - len(text))
        screenDict["text_"+str(i)] = text[start+1:end-1]
        text = text.replace(text[start:end], "text_"+str(i))
        i += 1
    i = 0
    txtSize = len(text)
    for match in re.finditer(inputText, text):
        start, end = match.span()
        start = start - (txtSize - len(text))
        end = end - (txtSize - len(text))
        inputDict["input_" + str(i)] = text[start+1:end-1]
        text = text.replace(text[start:end], "input_"+str(i))
        i += 1
    return text, screenDict, inputDict


def createOrdinalDict():
    p = inflect.engine()
    ordinalDict = {}
    for i in range(1, 100):
        word_form = p.number_to_words(i)
        ordinal_word = p.ordinal(word_form)
        # ordinal_number = p.ordinal(i)
        ordinalDict[ordinal_word] = i
    return ordinalDict


def replaceWord(text, original, replacement):  # replace every left by east
    txtSize = len(text)
    for match in re.finditer(original, text):
        start, end = match.span()
        start = start - (txtSize - len(text))
        end = end - (txtSize - len(text))
        text = text.replace(text[start:end], replacement)
    return text


def replaceDirections(text):
    next_to = r"next[\s|_|-]*?to"
    left = r"left"
    text = replaceWord(text, next_to, "beside")
    text = replaceWord(text, left, "east")
    return text


def replaceElements(text):
    expressions = [r"radio[\s|_|-]*?button", r"text[\s|_|-]+?box", r"check[\s|_|-]+?box", r"combo[\s|_|-]+?box",
                   r"spin[\s|_|-]+?box", "arrow", r"sub[\s|_|-]+?menu", r"scroll[\s|_|-]+?bar", r"progress[\s|_|-]+?bar",
                   r"tab[\s|-]*?bar", r"icon[\s|_|-]*?button",  r"\bbar\b", r"\bicon\b",
                   r"text[\s|_|-]+?area", r"drop[\s|_|-]*?down(([\s|_|-]*?menu)|([\s|_|-]*?list))?"]
    replacements = ["radio", "textbox", "checkbox", "combobox", "spinbox", "button", "submenu", "scrollbar",
                    "progressbar", "tab_bar", "icon", "scrollbar", "icon", "textarea",
                    "dropdown"]
    for i in range(len(expressions)):
        text = replaceWord(text, expressions[i], replacements[i])
    return text


def replaceOrdinalNumbers(text):
    p = inflect.engine()
    expression= r"\b[0-9][\s|_|-]*?((st)|(nd)|(th)|(rd))\b"
    txtSize = len(text)
    for match in re.finditer(expression, text):
        start, end = match.span()
        start = start - (txtSize - len(text))
        end = end - (txtSize - len(text))
        number=text[start:end-2]
        number = number.replace("-", "")
        number = number.replace("_", "")
        word_form = p.number_to_words(int(number))
        replacement= p.ordinal(word_form)
        text = text.replace(text[start:end], replacement)
    return text

def resolvePronouns():
    pass


def removeDET():  # which is , that is , etc...,
    pass



'''x = "click on the text box"
print(type(textReplacer(x)))'''


def preProcess(text):
    ordinal_dict = createOrdinalDict()
    text = replaceDirections(text)
    text = replaceElements(text)
    text = replaceOrdinalNumbers(text)
    text, screen_dict, input_dict = textReplacer(text)
    return text, ordinal_dict, screen_dict, input_dict
