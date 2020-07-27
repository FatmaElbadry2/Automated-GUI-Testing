from preProcessing import *
from RL.Utils import OpenApp
from global_imports import *
from executor import *
import shortcuts as sh
from elements_preprocessing import *

# split conjunction

if __name__ == "__main__":
    r.init(visual_automation=True, chrome_browser=False)
    app_path = "C:\\Program Files\\Elmer 8.4-Release\\bin"
    app_name = "ElmerGUI.exe"
    app_pid = OpenApp(app_path, app_name)

    text = "click on {material}. click on the icon on the left of the second green icon from the right. apply. click on the button on the left of {model}."

    text, ordinal_dict, screen_dict, input_dict = preProcess(text)
    text = nlp(text)
    sentences = text.sents
    sentences = list(sentences)
    print(sentences)

    for i in range(len(sentences)):
        print(sentences[i])

        image, path = save_image(i, "NLP")

        elements = buildElements(path, i, [Width, Height], "NLP")
        elements = getTextAndColor(elements,image)
        print(elements)

        try:
            execute(sentences[i], elements, ordinal_dict, screen_dict, input_dict)
        except ValueError as e:
            print(e)

    im=sh.ScreenShot()
    cv2.imwrite("C:\\Users\\ssalma\\Documents\\Dexter Projects\\Test NLP\\test1.png",im)
    r.close()
    os.kill(app_pid, 9)






