from preProcessing import *
from RL.Utils import *
from executor import *
import shortcuts as sh


# split conjunction

if __name__ == "__main__":

    app_path = "C:\\Program Files\\Elmer 8.4-Release\\bin"
    app_name = "ElmerGUI.exe"
    app_pid = OpenApp(app_path, app_name)

    text = "double click on the 5th icon button from the right"
    text, ordinal_dict, screen_dict, input_dict = preProcess(text)
    text = nlp(text)
    sentences = text.sents
    sentences = list(sentences)
    print(sentences)

    for i in range(len(sentences)):
        print(sentences[i])

        image, path = save_image(i, "NLP")

        elements = buildElements(path, i, [Width, Height], "NLP")
        print(elements)

        try:
            execute(sentences[i], elements, ordinal_dict)
        except ValueError as e:
            print(e)








