from NLP.imports import *


nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)
print(spacy.explain("RB"))


def expandContractions(text):
    sentence = ""
    words = re.split(" |:|;", text)
    for i in range(len(words)):
        if words[i].casefold() in CONTRACTION_MAP:
            words[i] = CONTRACTION_MAP[words[i].casefold()]
        sentence = sentence+" "+words[i]
    return sentence


# x = expandContractions("")
# print(x)
#sentence_nlp = nlp("he is funny and she is cool")


# print(sentence_nlp[2:8])
# print([t.orth_ for t in sentence_nlp[5].ancestors][0])
# print([t.i for t in sentence_nlp[1].rights])


def preProcess(text):
    text = sent_tokenize(text)
    text = expandContractions(text)
    return text
