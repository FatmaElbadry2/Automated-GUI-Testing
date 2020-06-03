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


def resolvePronouns():
    pass


def removeDET():  # which is , that is , etc...,
    pass


def splitConditions():
    pass


def injectBy():
    pass

#x = "click on the {file} menu"
#print(textReplacer(x))


def preProcess(text):
    text = replaceDirections(text)
    text, text_dict, input_dict = textReplacer(text)

    text = expandContractions(text)
    return text
