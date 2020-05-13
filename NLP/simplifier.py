from preProcessing import *


verbs = ["VERB","AUX"]
conjucts = ["ADJ", "ADV", "NOUN", "PROPN", "xcomp", "PRON"]
objects = ["pobj", "dobj"]
subjects = ["nsubj","csubj","npasssubj"]


def splitConj(text):
    sentences = []
    sent1 = []
    sent2 = []
    for word in text:
        if word.tag_ == "CC":
            parent = [p for p in word.ancestors][0]   # usually the root verb
            conj = [r for r in parent.rights if r.dep_ == "conj"]  # conjunction
            # fSubject = [l for l in parent.lefts if l.dep_ in subjects]
            dobject = [o for o in parent.rights if o.dep_ == "dobj"]
            prep = [o for o in parent.rights if o.dep_ == "prep"]
            pobject = []
            if len(prep) > 0:
                pobject = [p for p in prep[0].rights if len(prep) > 0]
            if len(conj) > 0 and conj[0].tag_ == parent.tag_ and parent.pos_ in verbs and parent.dep_ != "csubj":
                secSubject = [s for s in conj[0].lefts if s.dep_ in subjects]
                if len(secSubject) > 0 or (len(dobject) > 0 or (len(prep) > 0 and pobject[0].dep_ == "pobj")):  # 2 separate sentences
                    sent1 = text[0:word.i]
                    sent2 = text[word.i+1:]

                else:  # check if the first sentence has a subject
                    sent1 = str(text[0:word.i])+" "+str(text[min(conj[0].i + 1, len(text)):])
                    sent2 = str(text[0:parent.i])+" "+str(text[conj[0].i:])
            elif len(conj) == 0:
                sent1 = text[0:word.i]
                sent2 = text[word.i + 1:]

            else:
                sent1 = str(text[0:word.i]) + " " + str(text[min(conj[0].i + 1, len(text)):])
                sent2 = str(text[0:parent.i]) + " " + str(text[conj[0].i:])

    sentences.append(sent1)
    sentences.append(sent2)
    return sentences
# x = expandContractions()


sentence_nlp = nlp("click on a button then on the menu then on an arrow")


dependency_pattern = '{left}<---{word}[{w_type}]--->{right}\n--------'
for token in sentence_nlp:
    print(dependency_pattern.format(word=token.orth_,
                                   w_type=token.dep_,
                                   left=[t.orth_
                                            for t
                                            in token.lefts],
                                   right=[t.orth_
                                             for t
                                             in token.rights]))


spacy_pos_tagged = [(word, word.lemma_, word.tag_, word.pos_, word.dep_,word.ent_type_) for word in sentence_nlp]
print(spacy_pos_tagged)

print(splitConj(sentence_nlp))









