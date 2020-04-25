from matplotlib import pyplot as plt
import argparse
import os

def ErrorDictionaryMatcher(error):
    pass
    #returns boolean

def CheckDialogBox(dialogbox):
    # depends on the struct formulation
    text = dialogbox[2]  # assume text is stored in the 3rd position of the info. array
    check = ErrorDictionaryMatcher(text)
    return check

def ErrorHandler(elements, sudden_shutdown_check, screen_capture):
    if sudden_shutdown_check==True:
        return 1
    else:
        for i in range(elements):
            if elements[i]=="dialogbox":
                error_check = CheckDialogBox(elements[i])
                if error_check==1:
                    return 1
        return error_check