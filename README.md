Game: Sudoku
Extra constraints: The twin value strategy and the diagonal unit strategy
Search type: Breadth Deepth Search
Inspiration: Peter Norvig, Udacity


Q: How do we use constraint propagation to solve the naked twins problem? 

A: Constraint propogation is the use of the valid assumptions (unless we're approximating then the assumptions are mostly valid) to narrow our search space when searching along a given search tree.

The propogation can be applied to our Sudoku solver. It can be applied by adding functionality to our puzzle solver funvtion. With another function that eliminates values, it gives our code another chance to keep implementing the while loop until the loop reaches completion.

Naked twins is the idea that if 2 possible outcomes are occupied by 2 boxes in the same unit on a Sudoku puzzle, then only those 2 boxes can contain those values, because there are no other possibilities. So this means that you can throw out any matching values that are included in the twins, but not in their constituents across their respective units. This way we can narrow our search. By implementing this function, puzzle solver has a less populated search grid. A less populated search grid means there are less possible tries and tree branches for our breadth depth search to search along. This is the definition of constrained propogation.


Q: How do we use constraint propagation to solve the diagonal sudoku problem?  

A: This is much like the answer to the naked twins except we're constraining across our definition of the entire search space. Making the diagonals part of our units means that there is a lower number of total possibilities in the entire game of Sudoku. This is because there are more rules in place that constrains the possible numbers that are possible in every space. A good anaology for this would be Go and Chess. Chess has more rules than Go. Chess is more constrained than Go because the pieces have a smaller board and rules for how the pieces can move. Chess is easier to search and therefor less computationally heavy when searching for the possibile outcomes. Whereas go has a simpler rule structure and a larger board. 