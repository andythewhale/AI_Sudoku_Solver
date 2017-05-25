#Andy Miller

#This program solves any Sudoku puzzle.
#Included in the code are provisions to solve for diagonal sudokus.
#Hash out the rule to not use it.
#Change the sudoku grid to change your output.
#See the readme for conceptual information.

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

#Setting up our rows:
rows = 'ABCDEFGHI'
#setting up our cols:
cols = '123456789'

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

#So we make a cross function to iterate over all of our rows and cols to create our designations for each box:
def cross(a,b):
    crossed = []
    for i in a:
        for j in b:
            a = i+j
            crossed.append(a)
    return(crossed)
            
#So we make a vector that stores all of our box values:
boxes = cross(rows, cols)

#we aalso make a vector that stores all of our col units:
col_units = []
for j in cols:
    temp_col = cross(rows, j)
    col_units.append(temp_col)
    
#we make a vector that stores all of our row units with that:
row_units = []
for i in rows:
    temp_row = cross(i, cols)
    row_units.append(temp_row)
    
#We also need the units for the boxes:
box_units = []
box_row = ['ABC', 'DEF', 'GHI']
box_col = ['123', '456', '789']
for i in box_row:
    for j in box_col:
        temp_box = cross(i, j)
        box_units.append(temp_box)
    
#This is for the diagonal columns.
#This is my second submission and my reviewer gave me this code.
#My code before was a mess and did not use list comprehension.
#I will try to include list comprehension on future projects as it is best practice, thank you.
diagonal_1 = [a[0] + a[1] for a in zip(rows, cols)]
diagonal_2 = [a[0] + a[1] for a in zip(rows, cols[::-1])]
diagonal_units = [diagonal_1] + [diagonal_2]

#We need to add all of these units to the unitlist to have all of our units in one list:
unitlist = row_units + col_units + box_units + [diagonal_1] + [diagonal_2]

#This gives us a dictionary of all of our units for each box. 
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
#This gives us a dictionary of all of our peers for each box. This is insanely hard to follow
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)

#So we need a way to store out values in a grid.
#This code is not my own, I had never used a zip function before this moment. Let it be known that 
#I, Andy Miller, from this moment forward will be able to combine an equal list of keys and values
#with a zip function.
def grid_values(puzzle_string):
    #This function converts an incoming puzzle in string format and converts it to a dictionary.
    #The arguement is an 81 length string with numbers for defined values and periods for undefined.
    #It should return box label keys
    #It should return number value values.
    
    #so if there's a period we want to replace it with all the possible numbers. 
    values = []
    all_possible_numbers = '123456789'
    for c in puzzle_string:
        if c == '.':
            values.append(all_possible_numbers)
        else:
            values.append(c)
    #Let's make sure it's 81 in length:
    assert len(puzzle_string) == 81, "Input string must be 81 units in length"
    #Now we use a zip function to zip the stuff into a dictionary, I've never used zip, so this is fun.
    return dict(zip(boxes, values))

#Note to reviewer: I am using sublime and when copying over these silly arrows always take up my tab space.
#Is there a way to avoid this? I just don't like the way it looks.
def naked_twins(values):
#This function's job is to eliminate naked twins from a Sudoku puzzle.
#It will do this by iterating through each pair of boxes in a unit and
#checking for an equality in boxes that have 2 possible values.
#After that, this function eliminates these values from the other boxes
#within the Sudoku puzzle.

#This function takes in a dictionary as an arguement.
#This function releases a dictionary as an output.


    #For each unit in our unit list
    for unit in unitlist:
        #storage of unit twins and unit values
        unit_twins = []
        unit_values = []
        #For each box in our unit
        for box_a in unit:
            #For each box in our unit... again
            for box_b in unit:
                #Check if the value of this box is equivilent to the other for loop box
                if box_a != box_b and values[box_a] == values[box_b] and len(values[box_a]) == 2:
                    #If the values are equal then we have found a pair of twins.
                    #Because these are twins, we have to eliminate these values from all other boxes in this unit.
                    #But that's not the level that we're at in this for loop so we just save these values here.
                    #Add box_a to our unit list
                    unit_twins.append(box_a)
                    #Add box_b to our unit list
                    unit_twins.append(box_b)
                    #Add their value to our unit list
                    unit_values.append(values[box_a])

                    #Now we need to eliminate these values out of our boxes that are not the unit twins.
                    #So for each box in the unit
                    for box in unit:
                        #As long as the box is not a twin:
                        if box not in unit_twins:
                            #And for each value in unit values:
                            for big_number in unit_values:
                                for digit in big_number:
                                    #Replace the impossible values with nothing, eliminating it from existence in this box.
                                    #values[box] = values[box].replace(digit, '')
                                    values = assign_value(values, box, values[box].replace(digit,''))
    return values

#We need a function that rolls through our dictionary and eliminates stuff.
#The function needs to be the first iteration in our quest for solving the puzzle.
def eliminate(values):
    #This function eliminates the single values from the possible numbers in our values dictionary.
    #This is our first step in constraint propogation.
    #This function takes in the dictonary object as an arguement.
    #This function outputs another  dictionary function.
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            #values[peer] = values[peer].replace(digit,'')
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

#We also need a function that looks at the values in our units and determines:
#what is the only logical choice that fits into this scenario?
#It can work for all units
#It's possible that implementing for all units increases our search space way too much. But I want to try it.

def only_choice(values):
    #This function checks the units of an equation for boxes in a unit that only have one possible value.
    #This means that all other boxes are missing one of the digits from they're boxes.
    #So this function finds that digit and sets the respective box equal to that value.
    
    #This function takes in a sudoku puzzle dictionary as an input arguement.
    #This function outputs a dictionary in the exact same format, hopefully after solving some boxes.
    
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit
                values = assign_value(values, dplaces[0], digit)
    return values

#Note to reviewer: I am using sublime and when copying over these silly arrows always take up my tab space.
#Is there a way to avoid this? I just don't like the way it looks.



#So now we have 2 functions that narrow down our possible values. We can combine these functions
#We can just combine the functions into another function:
def reduce_puzzle(values):
    #This function will give us a function that place other functions within to apply constraint propogation
    #Constraint propogation just narrows the search space for a given search function.
    #Reduce puzzle will be included in the constraint propogation portion of a search function.
    
    #This function will take in a dictionary of values
    #This function will output a (hopefully) reduced version of that same dictionary.
    
    #Check if we're stalled:
    stalled = False
    #as long as we're not stalled, run:
    while not stalled:
        #check before for stalled:
        pre_stalled_check = len([box for box in values.keys() if len(values[box]) == 1])
        #apply our functions here:
        values = eliminate(values)
        values = naked_twins(values)
        values = eliminate(values)
        values = only_choice(values)
        values = eliminate(values)
        #check after for stalled
        post_stalled_check = len([box for box in values.keys() if len(values[box]) == 1])
        #Checking equality for stalling:
        stalled = pre_stalled_check == post_stalled_check
        #If we reduce stuff too much, then the functions don't make any sense, so we're going to eliminate that possibiltiy:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

        return values
    
#This is he hard part and understanding this is the main point of the entire project.
#This box is for the search function.
#This search function is going to follow the breadth - depth search idea where you go to end of a branch.
#You basically search all of the leaves of a tree first until you find a solution.
#So you go down a branch down a stem, to a leaf, don;'t get an answer? Search the next leaf.
#None of the leaves on this stem have the answer? search the next stem.
#None of the leaves in this stem in this branch have the answer? Search the next branch.


def search(values):
    #This function searches the possible outcomes of our Sudoku puzzle using breadth depth search.
    
    #This function will take in a dictionary of values
    #This function will output a (hopefully) solved Sudoku dictionary file.
    
    #So first thing is first, let's use constraint propogation on our values to reduce our searchs space:
    values = reduce_puzzle(values)
    #Just in case the CP function didn't output a faulty value:
    if values is False:
        return False
    #Check for solved:
    if all(len(values[i]) == 1 for i in boxes):
        return values
    #The best thing to do to further reduce the search is to choose the branches with the least possible outcomes
    #By searching them first we can fill in the Sudoku puzzle and possibly further reduce the search space.
    #We're basically guessing on the path that leads us to the highest probability of success.
    
    #Choose fewest guesses:
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    
    #Now we have a recursive step on our ideal or closest to our ideal base-case:
    for value in values[s]:
        #So we don't overwright.
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
        
def solve(grid):

    values = grid_values(grid)
    values = search(values)

    return values

    if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('Beep Boop')