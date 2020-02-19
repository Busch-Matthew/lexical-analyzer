def main():

    data = getInput()


    parse(data + ' ')

    output()

    #print(result)
    return






#-------------------------------------------------------------------------------
# lexeme Table Goes Here

#-------------------| L| D| _| S|  | O| !| .|--------------------------------------
state_table = [     [ 2, 4, 2, 6, 1, 7,10, 6], #1 -- entry point
                    [ 2, 2, 2, 3, 3, 3, 3, 3], #2 -- looking for an identifier
                    [ 1, 1, 1, 1, 1, 1, 1, 1], #3 -- terminating an identifier -- DOES NOT WAIT
                    [ 5, 4, 5, 5, 5, 5, 5, 8], #4 -- looking for a number or a float
                    [ 1, 1, 1, 1, 1, 1, 1, 1], #5 -- terminating a number -- DOES NOT WAIT
                    [ 1, 1, 1, 1, 1, 1, 1, 1], #6 -- terminating a seperator -- WAITS TO MOVE
                    [ 1, 1, 1, 1, 1, 1, 1, 1], #7 -- terminating an operator -- WAITS TO MOVE
                    [ 9, 8, 9, 9, 9, 9, 9, 9], #8 -- looking for a floatint point number
                    [ 1, 1, 1, 1, 1, 1, 1, 1], #9 -- terminating a floating point number -- DOES NOT WAIT
                    [10,10,10,10,10,10,11,10], #10 - looking for a comment
                    [1,1,1,1,1,1,1,1,1,1,1,1]  #11 - terminating a comment -- DOES NOT WAIT
                                                ]
exit_states = [ -1, 3, 5, 6, 7, 9, 11]

#-------------------------------------------------------------------------------
# keywords
#-------------------------------------------------------------------------------
keywords = ['int', 'float', 'bool', 'true', 'false', 'if', 'else', 'then',
            'endif', 'while', 'whileend', 'do', 'doend', 'for', 'forend',
            'input', 'output', 'and', 'or', 'not']

seperators = ['(' , ')' , '{', '}', "'",'[', ']', ',', ':', ';']

operators = ['*', '+', '-', '=', '/', '>', '<', '%']

#-------------------------------------------------------------------------------
# itterate through input
#-------------------------------------------------------------------------------
def parse(data):
    print(data)
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
            if current_state in [6, 7, 11]:
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
    elif foo == '_':
        input_value = 3
    elif foo in seperators:
        input_value = 4
    elif foo == ' ':
        input_value = 5
    elif foo in operators:
        input_value = 6
    elif foo == '!':
        input_value = 7
    elif foo == '.':
        input_value = 8
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
        token = 'seperator'
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
    parsable_string = input()
    return parsable_string




#-------------------------------------------------------------------------------
# output funtion
#-------------------------------------------------------------------------------
def output():
    output_file = open("output.txt","w+")
    output_file.write('            Tokens     |    Lexemes \n')
    for foo in range(0,len(result)):
        output_file.write('%18s     =     %s \n' % (result[foo][1], result[foo][0]))

    return

#-------------------------------------------------------------------------------
# calling the main fucntion
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

#-------------------------------------------------------------------------------
# end of program
#-------------------------------------------------------------------------------
