"""
The purpose of this document is to show  how to solve a 'recursive'-type problem
more intuitively.  The basic formula, as described in the readme, is to have
a todo list that you are popping items on and off of, and then transferring
them to a done list.  The solution to this problem though is simple than the
case of the elements, because the "item1" and "processing data" are the same
(Although I suppose I could have solved the elements problem this way too, just
maintaining a list of elements and continuing to cut the string until the last
item in the list is also an element symbol).

The problem solved here is given a keypad, i.e.:

123
456
789
 0 

what are the possible numbers you can dial using the moves of a chess knight?
"""


# from each position, where can you go?
knight_moves = [[4,6],[6,8],[9,7],[4,8],[3,9,0],[],[1,7,0],[2,6],[1,3],[2,4]]

# initialize the todo list. Here, the data structure is a list of lists.  E.g.
# one entry may be [1,6,7,2], which is an incomplete number that will need either
# a 7 or 9 thrown back on the list
todo=[[1],[2],[3],[4],[6],[7],[8],[9]]

# initialize the list of finished candidates.  We will make these just a continuous
# 7-digit integer.
done=[]

# while you still have todo items...
while len(todo)>0:

    # ...pop an item off the todo list
    workon = todo.pop()

    # there are two to three possible moves you can make. for each one:
    for move in knight_moves[workon[-1]]:

        # what's the full list with that move included?
        full_list = [*workon,move]

        # append to the appropriate list.  If it's done make it just one
        # string instead of a list of integers, then convert that to an int
        if len(workon)==6:
            done.append(int(''.join([str(i) for i in full_list])))
        else:
            todo.append(full_list)

# tidy up
done.sort()
print(done)

