def main():

    data = getInput()
    parse(data + ' ')


    print(result)
    return 0






#-------------------------------------------------------------------------------
# lexeme Table Goes Here
#--------------------L|D|_|(|)| |;|---------------------------------------------
state_table = [     [2,4,2,6,6,1,6], #1 -- entry point
                    [2,2,2,3,3,3,3], #2 -- looking for an identifier
                    [1,1,1,1,1,1,1], #3 -- terminating an identifier -- BACKS UP
                    [5,4,5,5,5,5,5], #4 -- looking for a number
                    [1,1,1,1,1,1,1], #5 -- terminating a number -- BACKS UP
                    [1,1,1,1,1,1,1]  #6 -- terminating a seperator
                                        ]
exit_states = [3,5,6]


#-------------------------------------------------------------------------------
# keywords
#-------------------------------------------------------------------------------

keywords = ['int', 'float', 'bool', 'true', 'false', 'if', 'else', 'then',
            'endif', 'while', 'whileend', 'do', 'doend', 'for', 'forend',
            'input', 'output', 'and', 'or', 'not']

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
            if current_state in [6]:
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
    elif foo == '=':
        input_value = 3
    elif foo == '(':
        input_value = 4
    elif foo == ')':
        input_value = 5
    elif foo == ' ':
        input_value = 6
    elif foo == ';':
        input_value = 7
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
        
    return

#-------------------------------------------------------------------------------
# input Function
#-------------------------------------------------------------------------------
def getInput():
    parsable_string = input()
    return parsable_string

#-------------------------------------------------------------------------------
# calling the main fucntion
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

#-------------------------------------------------------------------------------
# end of program
#-------------------------------------------------------------------------------
