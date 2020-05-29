from imports import *
from enum import Enum


def matchText(eText, uText,thresh):
    levRatio = fuzz.partial_ratio(eText.lower(), uText.lower())
    if levRatio >= thresh:
        return True, levRatio
    return False, levRatio


def getObjectRange(x_center, y_center, width, height):
    x_min = x_center - (width / 2)
    x_max = x_center + (width / 2)
    y_min = y_center - (height / 2)
    y_max = y_center + (height / 2)
    return x_min, x_max, y_min, y_max


def in_range(x_range, y_range, objs):
    in_obj = []
    for obj in objs:
        in_x = False
        in_y = False
        x_min, x_max, y_min, y_max = getObjectRange(obj.x_center, obj.y_center, obj.width, obj.height)
        for x in x_range:
            if x_min >= x[0] and x_max <= x[1]:
                in_x = True
                break
        for y in y_range:
            if y_min >= y[0] and y_max <= y[1]:
                in_y = True
                break
        if in_x and in_y:
            in_obj.append(obj)
    return in_obj


def colorComparator(shade,elems):
    colors = np.array([e.hex for e in elems])
    lightest = max(colors)
    darkest = min(colors)
    if shade == "light":
        return colors[colors == lightest]
    else:
        return colors[colors == darkest]


# it only processes one split sentence


def is_inside(range1, range2):
    intersection = []
    min_in_range = False
    max_in_range = False
    if range1[0] <= range2[0] <= range1[1]:
        min_in_range = True
    if range1[0] <= range2[1] <= range1[1]:
        max_in_range = True
    if min_in_range and max_in_range:
        intersection = [range2[0], range2[1]]
    elif min_in_range:
        intersection = [range2[0], range1[1]]
    elif max_in_range:
        intersection = [range1[0], range2[1]]
    return intersection


def Intersection(x_range1, x_range2, y_range1, y_range2):
    intersections_x = []
    for x1 in x_range1:
        for x2 in x_range2:
            intersection_x = is_inside(x1, x2)
            if len(intersection_x) == 0:
                intersection_x = is_inside(x2, x1)
            if len(intersection_x) > 0:
                intersections_x.append(intersection_x)
    if len(intersections_x) == 0:
        return None, None
    intersections_y = []
    for y1 in y_range1:
        for y2 in y_range2:
            intersection_y = is_inside(y1, y2)
            if len(intersection_y) == 0:
                intersection_y = is_inside(y2, y1)
            if len(intersection_y) > 0:
                intersections_y.append(intersection_y)
    if len(intersections_y) == 0:
        return None, None
    return intersections_x, intersections_y


def nearestElement(elements, center):
    dist_min = m.sqrt(pow(elements[0].x_center-center[0], 2) + pow(elements[0].y_center-center[1], 2))
    nearest = elements[0]
    for element in elements[1:]:
        dist = m.sqrt(pow(element.x_center-center[0], 2) + pow(element.y_center-center[1], 2))
        if dist < dist_min:
            dist_min = dist
            nearest = element
    return nearest


inside = ["in", "on", "inside", "into", "of", "towards", "to", "for", "from", "middle"]
below = ["below", "under", "beneath", "bottom", "down"]
above = ["over", "above", "top", "up"]
beside = ["next", "beside"]


def directionOfIncrease(x, y):
    if all(p == x[0] for p in x):
        direction = "vertical"

    elif all(p == y[0] for p in y):
        direction = "horizontal"

    else:
        def line(x, a, b):
            return (a * x) + b
        param, param_cov = curve_fit(line, x, y)
        angle = m.degrees(param[0])
        if 40 <= abs(angle) <= 50:
            if angle < 0:
                direction = "vertical"
            else:
                direction = "horizontal"
        elif abs(angle) > 50:
            direction = "vertical"
        else:
            direction = "horizontal"
    return direction


def ordinalSorter(value, objs, direction=None):
    sorted_obj = objs
    if type(objs) is np.ndarray:
        sorted_obj = sorted_obj.tolist()
    if direction in below:
        sorted_obj.sort(key=operator.attrgetter('y_center'), reverse=True)
    elif direction in above:
        sorted_obj.sort(key=operator.attrgetter('y_center'))
    elif direction in ["left", "east"]:
        sorted_obj.sort(key=operator.attrgetter('x_center'))
    elif direction in ["right", "west"]:
        sorted_obj.sort(key=operator.attrgetter('x_center'), reverse=True)
    elif direction is None:
        x_points = [p.x_center for p in objs]
        y_points = [p.y_center for p in objs]
        direction = directionOfIncrease(x_points, y_points)
        if direction == "vertical":
            sorted_obj.sort(key=operator.attrgetter('y_center'))
        else:
            sorted_obj.sort(key=operator.attrgetter('x_center'))
    return [sorted_obj[value - 1]], sorted_obj


def prepMatcher(x_min, x_max, y_min, y_max, wx_min, wx_max, wy_min, wy_max, prep):
    # it can return a multi range but it can only take single range as an input
    if prep in inside:
        return [[x_min, x_max]], [[y_min, y_max]]
    elif prep in below:
        return [[wx_min, wx_max]], [[y_max, wy_max]]
    elif prep in above:
        return [[wx_min, wx_max]], [[wy_min, y_min]]
    elif prep in beside:
        return [[wx_min, x_min], [x_max, wx_max]], [[wy_min, wy_max]]
    elif prep == "out":
        return [[wx_min, x_min], [x_max, wx_max]], [[wy_min, y_min], [y_max, wy_max]]
    elif prep in ["left", "east"]:
        return [[wx_min, x_min]],  [[wy_min, wy_max]]
    elif prep in ["right", "west"]:
        return [[x_max, wx_max]], [[wy_min, wy_max]]
    return [[wx_min, wx_max]], [[wy_min, wy_max]]


class Errors(Enum):  # type of errors
    object_not_found = 0
    empty_range = 1
    invalid_key = 2
    no_error = 3







