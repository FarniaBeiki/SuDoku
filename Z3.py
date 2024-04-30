from z3 import *

# build a matrix 9*9 with each cell type is int
X = [ [ Int("x_%s_%s" % (i+1, j+1)) for j in range(9) ] for i in range(9) ]


# set the rule of that each cell must be a value between 1 until 9
cells_c  = [ And(1 <= X[i][j], X[i][j] <= 9) for i in range(9) for j in range(9) ]

# use Distinct function to set the rule of that each row of matrix(table) must have an unique vlaue
rows_c   = [ Distinct(X[i]) for i in range(9) ]

# use Distinct function to set the rule of that each column of matrix(table) must have an unique vlaue
cols_c   = [ Distinct([ X[i][j] for i in range(9) ]) for j in range(9) ]

# use Distinct function to set the rule of that every 3*3 matrix cells must have an unique vlaue
sq_c     = [ Distinct([ X[3*i0 + i][3*j0 + j]     for i in range(3) for j in range(3) ])  for i0 in range(3) for j0 in range(3) ]

# now every rules turn to a code and we must combine all rules
sudoku_c = cells_c + rows_c + cols_c + sq_c

# use instance object to show our sudoku table , 0 cells consider as empty cell
instance = ((0,0,0,0,6,1,0,0,2),
            (0,7,0,0,0,0,0,6,0),
            (9,2,0,0,0,0,0,0,0),
            (0,0,4,5,2,0,9,0,0),
            (0,8,2,1,0,4,6,3,0),
            (0,0,3,0,7,6,1,0,0),
            (0,0,0,0,0,0,0,9,8),
            (0,3,0,0,0,0,0,4,0),
            (6,0,0,3,8,0,0,0,0))

# we use 0 as empty now we must turn 0 filed to true and not zero filed to false to z3 understand
instance_c = [ If(instance[i][j] == 0, 
        True, 
        X[i][j] == instance[i][j]) 
    for i in range(9) for j in range(9) ]

s = Solver()                                           
s.add(sudoku_c + instance_c)                            
if s.check() == sat:                                    
    m = s.model()                                       
    r = [ [ m.evaluate(X[i][j]) for j in range(9) ]     
          for i in range(9) ]
    print_matrix(r)                                    
else:
    print("failed to solve")   