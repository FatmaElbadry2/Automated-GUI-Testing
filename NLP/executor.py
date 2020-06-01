from actionMatcher import *
from objectMatcher import *

text_dict = {}
input_dict = {}

# don't forget the keypress


def execute(sentence, elements):
    pos = getSentenceStructure(sentence, elements)
    target_obj = None
    if pos.target_element is not None:
        target_obj, tx_range, ty_range, t_input, direction = objectFinder(pos.target_element, elements, text_dict,
                                                                      input_dict)
        if t_input is not None:
            pos.input = t_input
        if direction is not None:
            pos.direction = direction
    if pos.source_element is not None:
        source_obj, sx_range, sy_range, t_input, direction = objectFinder(pos.source_element, elements, text_dict,
                                                                      input_dict)

    actionMapper(pos.action, [target_obj.x_center, target_obj.y_center], t_input=pos.input, quantity=pos.quantity,
                 direction=pos.direction)

