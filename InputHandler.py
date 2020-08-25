##This Input handler will serve as a layer between the actual input and the
##resulting action in the game.

##Introducing new naming convention.
##All names that aren't classes or constants are lower case seperated by underscores
##An underscore before a name indicates a hidden or private variable.




#Buttons and properties:
drop_button = False
_drop_delay = 12
_drop_count = 0

def UpdateDrop(cur_val):
    global _drop_count
    global drop_button
    if (cur_val == 0):
        drop_button = False
        _drop_count = 0
    else:
        if (_drop_count == 0):
            drop_button = True
        else:
            drop_button = False
        _drop_count = (_drop_count+1) % _drop_delay
        

right_button = 0
_x_delay = 4
_x_offset = 13
_right_count = 0

def UpdateRight(cur_val):
    global _right_count
    global right_button
    if (cur_val == 0):
        right_button = 0
        _right_count = 0
    else:
        if (_right_count == 0 or _right_count == _x_offset):
            right_button = 1
        else:
            right_button = 0
        _right_count += 1
        if (_right_count > _x_offset):
            _right_count = _x_offset + (_right_count - _x_offset)%_x_delay

left_button = 0
_left_count = 0

def UpdateLeft(cur_val):
    global left_button
    global _left_count
    if (cur_val == 0):
        left_button = 0
        _left_count = 0
    else:
        if (_left_count == 0 or _left_count == _x_offset):
            left_button = 1
        else:
            left_button = 0
        _left_count += 1
        if (_left_count > _x_offset):
            _left_count = _x_offset + (_left_count - _x_offset)%_x_delay

down_button = 0
_down_delay = 6
_down_count = 0

def UpdateDown(cur_val):
    global down_button
    global _down_count
    if (cur_val == 0):
        down_button = 0
        _down_count = 0
    else:
        if (_down_count == 0):
            down_button = 1
        else:
            down_button = 0
        _down_count = (_down_count+1) % _down_delay

rotate_button = 0
_rotate_delay = 17
_rotate_count = 0

def UpdateRotate(cur_val):
    global rotate_button
    global _rotate_count
    if (cur_val == 0):
        rotate_button = 0
        _rotate_count = 0
    else:
        if (_rotate_count == 0):
            rotate_button = cur_val
        else:
            rotate_button = 0
        _rotate_count = (_rotate_count+1) % _rotate_delay

store_button = False

def UpdateStore(cur_val):
    global store_button
    store_button = cur_val


accept_button = False

def UpdateAccept(cur_val):
    global accept_button
    accept_button = cur_val

reject_button = False

def UpdateReject(cur_val):
    global reject_button
    reject_button = cur_val

pause_button = False
_pause_count = 0
_pause_delay = 10

def UpdatePause(cur_val):
    global pause_button
    global _pause_count
    if (cur_val == 0):
        pause_button = False
        _pause_count = 0
    else:
        if (_pause_count == 0):
            pause_button = True
        else:
            pause_button = False
        _pause_count = (_pause_count+1) % _pause_delay
        
#Does not need delay ass it cannot be repeated.

updates = [UpdateLeft, UpdateRight, UpdateRotate, UpdateDown, UpdateDrop, UpdateAccept, UpdateStore, UpdatePause, UpdateReject]

def update():
    #moveRight
    for i in range(len(userInput)):
        updates[i](userInput[i])


        
        




