from actionMatcher import *
from objectMatcher import *



# don't forget the keypress
# ordinal_dict={}
# text_dict={}
# input_dict={}

def execute(sentence, elements,ordinal_dict,text_dict,input_dict):
    pos, action_type = getSentenceStructure(sentence, elements)
    x_center1, x_center2, y_center1, y_center2, target_obj, source_obj = None, None, None, None, None, None
    if pos.target_element is not None:
        target_obj, tx_range, ty_range, t_input, direction, return_type = objectFinder(pos.target_element, elements,
                                                                                       text_dict, input_dict,ordinal_dict,pos.target_index)
        print("whfgwf: ",direction)
        if t_input is not None:
            pos.input = t_input
        if direction is not None:
            pos.direction = direction
        if return_type == ReturnTypes.range:
            x_center1 = round((tx_range[0][0]+tx_range[0][1])/2)
            y_center1 = round((ty_range[0][0]+ty_range[0][1])/2)
        elif target_obj is not None:
            x_center1 = target_obj.x_center
            y_center1 = target_obj.y_center
    if pos.source_element is not None:
        #if pos.direction is not None and str(pos.action[-1]) == "scroll" and action_type == Actions.drag:
            # if pos.direction in ["up", "down", "top", "bottom"]:
            #     elements = [e for e in elements if e.text == "vertical" and e.type == "scrollbar"]
            # elif pos.direction in ["left", "right", "east", "west"]:
            #     elements = [e for e in elements if e.text == "horizontal" and e.type == "scrollbar"]
        source_obj, sx_range, sy_range, t_input, direction, return_type = objectFinder(pos.source_element, elements,
                                                                                       text_dict, input_dict,ordinal_dict,pos.source_index)
        if return_type == ReturnTypes.range:
            x_center2 = round((sx_range[0][0]+sx_range[0][1])/2)
            y_center2 = round((sy_range[0][0]+sy_range[0][1])/2)
        elif source_obj is not None:
            x_center2 = source_obj.x_center
            y_center2 = source_obj.y_center
    print(pos.direction)
    actionMapper(elements, pos.action, action_type, [x_center1, y_center1], [x_center2, y_center2], t_input=pos.input,
                 quantity=pos.quantity, direction=pos.direction)


# text = nlp("drag the dialogbox by 100 cm to the right")
# try:
#     execute(text, e9,ordinal_dict,text_dict,input_dict)
# except ValueError as e:
#     print(str(e))
