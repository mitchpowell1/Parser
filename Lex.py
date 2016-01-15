"""
Written in Python 3.4

Performs lexical analysis based on a grammar corresponding with the following transition table:

+------------+------------+------------+----------+------------+-------+-------+
|   State    |   letter   |   digit    | operator |     =      | space | other |
+------------+------------+------------+----------+------------+-------+-------+
| start      | identifier | number     | operator | assignment | start | error |
| identifier | identifier | identifier | operator | assignment | start | error |
| number     | error      | number     | operator | assignment | start | error |
| operator   | identifier | number     | error    | assignment | start | error |
| assignment | identifier | number     | operator | error      | start | error |
| error      | error      | error      | error    | error      | error | error |
+------------+------------+------------+----------+------------+-------+-------+

Represented as a 2D array,

The states correspond to row values as follows:
0 = Start
1 = Identifier
2 = Number
3 = Operator
4 = Assignment
5 = Error   <-- This is a sink state, should the program reach this state it will stop parsing the input

Potential input types correspond with column values and are:
0 = letter
1 = digit
2 = operator
3 = '='
4 = space
5 = other <-- Always produces an error

"""


import string


__author__ = "Mitch Powell"
__course__ = "Dr. Narayan, CSC 434: Programming Languages"
__date__ = "1/14/2016"


"""
initialize_vars() function just initializes the global variables that the rest of the program
uses.
"""


def initialize_vars():
    global state
    global delta_table
    global operator
    global letter
    global digit
    global input_types

    state = 0                                                                      # Initialized to start state.
    delta_table = [[1, 2, 3, 4, 0, 5],                                             # Defines table transitions for
                   [1, 1, 3, 4, 0, 5],                                             # each state.
                   [5, 2, 3, 4, 0, 5],
                   [1, 2, 5, 4, 0, 5],
                   [1, 2, 3, 5, 0, 5],
                   [5, 5, 5, 5, 5, 5]]
    operator = ['+', '-', '*', '/']                                                # Global operator list
    letter = list(string.ascii_lowercase)                                          # Global letter list
    digit = list(string.digits)                                                    # Global digit list
    input_types = [letter, digit, operator, ['='], [' ']]                          # list of different input types


"""
get_state_names() function takes a numerical input and returns the name of the state that corresponds
with said parameter. (Correlates with the table at the top)
"""


def get_state_names(state_code):
    state_names = ['start', 'identifier', 'number', 'operator', 'assignment', 'error']
    return state_names[state_code]


"""
read_input() function simply reads a text file
"""


def read_input(filename):
    global input_file
    input_file = open(filename, 'r')


"""
state_transition() function evaluates whether or not a state transition happens,
and returns a string with the appropriate tokenization.
"""


def state_transition(newstate):
    global state
    token = ''
    if delta_table[state][newstate] != state:                # If the character leads to a transition to a new state
        if state != 0:                                       # and the initial state isn't "Start"
            token = get_state_names(state) + " "             # append the tokenization of the string
    state = delta_table[state][newstate]                     # to include the state we just transitioned from
    return token


"""
parse_input() reads through all of the lines in the input file and
passes them to the parse_line() function, and prints the returned tokenization
"""


def parse_input():
    global state
    for line in input_file:
        if line[-1] == '\n':                                  # Removes any newline characters to avoid parsing errors
            line = line[:-1]
        state = 0                                             # Resets to start state before each line (important)
        print(line + " tokenizes as " + parse_line(line))


"""
The parse_line() function takes a string, splits it into all of its component characters,
checks each character against the different input sets for membership. Once a character
is verified as a member of a particular class of input, a corresponding numerical value is passed to
the state_transition() function to check if the character dictates a change in state
"""


def parse_line(line):
    global state
    line_tokenization = ""
    split_line = list(line)                                             # Split line into characters
    for character in split_line:
        valid_input = False                                             # assumes character is invalid initially
        for choice in range(len(input_types)):
            if character in input_types[choice]:
                valid_input = True                                      # if a character can be matched to a type,
                line_tokenization += state_transition(choice)           # pass it to the state_transition() function
                break
        if not valid_input:                                             # if a character doesn't fit any categories
            if state > 0:                                               # and the state is not the start state
                line_tokenization += get_state_names(state)+" "         # print out the state the analyzer was in
            state = 5                                                   # and declare an error
            break
    line_tokenization += get_state_names(state)                         # adds the completion state to the end of the
    return line_tokenization                                            # tokenization string


"""
The main() function calls all of the required functions and ensures that the data input file is closed.

If you wish to use the lexical analyzer on a different file, it should be changed in the read_input()
function call here.
"""


def main():
    initialize_vars()
    read_input("sample_data")                                           # modify this to change input file
    parse_input()
    input_file.close()


main()
