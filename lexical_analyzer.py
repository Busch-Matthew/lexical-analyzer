def main():
    data = getInput()
    itterate(data)
    output()
    checkErrors()
    return

#-------------------------------------------------------------------------------
# lexeme Table Goes Here

#-------------------| L| D| _| S|  | O| !| .| n|--------------------------------------
state_table = [     [ 2, 4, 2, 6, 1, 7,10, 6, 1], #1 -- entry point
                    [ 2, 2, 2, 3, 3, 3, 3, 3, 3], #2 -- looking for an identifier
                    [ 1, 1, 1, 1, 1, 1, 1, 1, 1], #3 -- terminating an identifier -- WAITS TO MOVE
                    [ 5, 4, 5, 5, 5, 5, 5, 8, 1], #4 -- looking for a number or a float
                    [ 1, 1, 1, 1, 1, 1, 1, 1, 1], #5 -- terminating a number -- WAITS TO MOVE
                    [ 1, 1, 1, 1, 1, 1, 1, 1, 1], #6 -- terminating a separator -- DOES NOT WAIT
                    [ 1, 1, 1, 1, 1, 1, 1, 1, 1], #7 -- terminating an operator -- DOES NOT WAIT
                    [ 9, 8, 9, 9, 9, 9, 9, 9, 9], #8 -- looking for a floatint point number
                    [ 1, 1, 1, 1, 1, 1, 1, 1, 1], #9 -- terminating a floating point number -- WAITS TO MOVE
                    [10,10,10,10,10,10,11,10,11], #10 - looking for a comment
                    [ 1 ,1, 1, 1, 1, 1, 1, 1, 1]  #11 - terminating a comment -- DOES NOT WAIT
                                                    ]
exit_states = [ -1, 3, 5, 6, 7, 9, 11]

#-------------------------------------------------------------------------------
# keywords
#-------------------------------------------------------------------------------
keywords = ['int', 'float', 'bool', 'true', 'false', 'if', 'else', 'then',
            'endif', 'while', 'whileend', 'do', 'doend', 'for', 'forend',
            'input', 'output', 'and', 'or', 'not']

separators = ['(' , ')' , '{', '}', "'",'[', ']', ',', ':', ';']

operators = ['*', '+', '-', '=', '/', '>', '<', '%']

#-------------------------------------------------------------------------------
# iterate through lines
#-------------------------------------------------------------------------------
def itterate(data):
    for foo in range(0,len(data)):
        print(f'parsing line {foo+1}\n')
        parse(data[foo] + ' ', foo + 1)

#-------------------------------------------------------------------------------
# itterate through characters of lines
#-------------------------------------------------------------------------------
error_list = []

def parse(data, current_line):
    front = 0
    current_state = 1
    next_state = 1
    tail = 0
    itteration = 1
    while tail < len(data):
        print(f'itteration #{itteration}')
        print(f'current state: {current_state}')
        foo = data[tail]
        print(f'checking for input: {foo}')
        current_state = nextState(current_state, foo)
        print(f'resulting state: {current_state}')
        if current_state in exit_states:
            if current_state == -1:
                error_list.append(f'Error reading line {current_line}, col {itteration}')
                print(f'error handling input: {foo}')
                print('------------------')
                break
            elif current_state in [6, 7, 11]:
                print (f'adding to list: {(data[front:tail] + foo).strip()}')
                move_forward = addToList((data[front:tail] + foo).strip() ,current_state)
            else:
                print (f'adding to list: {data[front:tail].strip()}')
                move_forward = addToList(data[front:tail].strip(),current_state)
            current_state = 1
            if move_forward:
                tail += 1
                front = tail
            else:
                front = tail
        else:
            tail += 1

        itteration +=1
        print('------------------')
    return

#-------------------------------------------------------------------------------
# get next state
#-------------------------------------------------------------------------------
def nextState(current_state, foo):
    input_value = 0
    if foo.isalpha():
        input_value = 1
    elif foo.isdigit():
        input_value = 2
    elif foo in ['_', '$']:
        input_value = 3
    elif foo in separators:
        input_value = 4
    elif foo in [' ', '\t']:
        input_value = 5
    elif foo in operators:
        input_value = 6
    elif foo == '!':
        input_value = 7
    elif foo == '.':
        input_value = 8
    elif foo == '\n':
        input_value = 9
    else:
        return -1

    state = state_table[current_state - 1][input_value - 1]
    return state

#-------------------------------------------------------------------------------
# push to completion table
#-------------------------------------------------------------------------------
result = []

def addToList(lexeme, exit_state):
    token = ''
    if exit_state == 3:
        if lexeme in keywords:
            token = 'keyword'
        else:
            token = 'identifier'
        result.append([lexeme, token])
        return False
    elif exit_state == 5:
        token = 'integer'
        result.append([lexeme, token])
        return False
    elif exit_state == 6:
        token = 'separator'
        result.append([lexeme, token])
        return True
    elif exit_state == 7:
        token = 'operator'
        result.append([lexeme,token])
        return True
    elif exit_state == 9:
        token = 'floating point'
        result.append([lexeme,token])
        return False
    elif exit_state == 11:
        token = 'comment'
        result.append([lexeme, token])
        return True
    return False

#-------------------------------------------------------------------------------
# input function
#-------------------------------------------------------------------------------
def getInput():
    input_file = open("input.txt", "r")
    data = input_file.readlines()
    input_file.close()
    return data

#-------------------------------------------------------------------------------
# output funtion
#-------------------------------------------------------------------------------
def output():
    output_file = open("output.txt","w")
    output_file.write('            Tokens     |    Lexemes \n')
    for foo in range(0,len(result)):
        output_file.write('%18s     =     %s \n' % (result[foo][1], result[foo][0]))
    output_file.close()
    return

#-------------------------------------------------------------------------------
# outputing error_list if there were any
#-------------------------------------------------------------------------------
def checkErrors():
    if error_list != []:
        for foo in range(0,len(error_list)):
            print(error_list[foo])
    else:
        print('No errors were detected!')

#-------------------------------------------------------------------------------
# calling the main fucntion
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

#-------------------------------------------------------------------------------
# end of program
#-------------------------------------------------------------------------------
