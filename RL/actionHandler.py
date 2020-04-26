
def ActionEncoder(label, ID):
    actions = []
    if(label=="button" or label=="icon-button" or label=="radio-button" or label=="combobox-opened" or label=="combobox-closed" or label=="menu" or label=="checkbox"):
        action = "0000" + ID
        actions.append(action)
    elif(label=="scrollbar" or label=="slider"):
        action = "0100" + ID
        actions.append(action)
    elif label=="link":
        action = "0010" + ID
        actions.append(action)
    elif label=="textbox":
        action = "0111" + ID
        actions.append(action)
        action = "1001" + ID
        actions.append(action)
        action = "1011" + ID
        actions.append(action)
        action = "1101" + ID
        actions.append(action)
        action = "1111" + ID
        actions.append(action)
    return actions

def DecimalToBinary(n):
    return bin(n).replace("0b", "")

def ActionDecoder(action_code):
    action_type = action_code[0:4]
    ID = action_code[4:]
    action= ""
    if action_type=="0000":
        action = "click"
    elif action_type=="0100":
        action = "slide"
    elif action_type=="0010":
        action = "double-click"
    elif action_type=="0111":
         action = "alphabet"
    elif action_type=="1001":
         action = "alphanumeric"
    elif action_type=="1011":
         action = "numbers"
    elif action_type=="1101":
         action = "long"
    elif action_type=="1111":
         action = "empty"
    return


def ActionSpace():
    action_space = []
    for i in range(1,801):
        binary_id = DecimalToBinary(i)
        difference = 11 - len(binary_id)
        for j in range(difference):
            binary_id = "0" + binary_id
        action = "0000" + binary_id
        action_space.append(action)
    for i in range(801,901):
        binary_id = DecimalToBinary(i)
        difference = 11 - len(binary_id)
        for j in range(difference):
            binary_id = "0" + binary_id
        action = "0010" + binary_id
        action_space.append(action)
    for i in range(901,1001):
        binary_id = DecimalToBinary(i)
        difference = 11 - len(binary_id)
        for j in range(difference):
            binary_id = "0" + binary_id
        action = "0100" + binary_id
        action_space.append(action)
    for i in range(1001,1201):
        binary_id = DecimalToBinary(i)
        difference = 11 - len(binary_id)
        for j in range(difference):
            binary_id = "0" + binary_id
        action = "0111" + binary_id
        action_space.append(action)
    for i in range(1201,1401):
        binary_id = DecimalToBinary(i)
        difference = 11 - len(binary_id)
        for j in range(difference):
            binary_id = "0" + binary_id
        action = "1001" + binary_id
        action_space.append(action)
    for i in range(1401,1601):
        binary_id = DecimalToBinary(i)
        difference = 11 - len(binary_id)
        for j in range(difference):
            binary_id = "0" + binary_id
        action = "1011" + binary_id
        action_space.append(action)
    for i in range(1601,1801):
        binary_id = DecimalToBinary(i)
        difference = 11 - len(binary_id)
        for j in range(difference):
            binary_id = "0" + binary_id
        action = "1101" + binary_id
        action_space.append(action)
    for i in range(1801,2001):
        binary_id = DecimalToBinary(i)
        difference = 11 - len(binary_id)
        for j in range(difference):
            binary_id = "0" + binary_id
        action = "1111" + binary_id
        action_space.append(action)
    return action_space
