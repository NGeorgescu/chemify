
=======
Chemify
=======

Python Library that is aimed at writing phrases in chemical element symbols

What do you mean?
-----------------
Consider my  name, 'Nicholas Georgescu'. It can be written as the chemical symbols 'Ni' 'C' 'Ho' 'La' 'S', 'Ge' 'O' 'Rg' 'Es' 'Cu', i.e. nickel, carbon, holmium, lanthanum, sulfur... germanium, oxygen, roentgenium, einsteinium, copper. This library lets you do that for literally any piece of text.

Ok... why?
----------
**Real Answer:** I always liked that you could spell my full name out of chemical elements ever since the induction of roentgenium in 2004 (My middle name doesn't work though; it's my greatest shame). It was a game I would play in high school when in the car on roadtrips looking at street names, etc.

**Smarter Answer:** This actually is non-trivial to implement because chemical symbols can be either one or two letter in length.  Suppose a string starts with 'Nar'.  Now there is no element 'R', but there is 'N', 'Na', and 'Ar', as well as other elements that start with R like 'Rg', 'Ru', 'Rh', etc.  So, should this be chunked as 'N, Ar', or 'Na, R..'? If the next letter is an 'C', the former only works.  If the next letter is a 'G', the latter only works.  If the next letter is a 'U', either works, but maybe you run into problems with later letters.  This gets messy quickly.  Hence it's really a test of implementation.  If you understand how to solve this problem you can solve other similar problems that people think of as recursive (like the google interview 'Knight Dialer' problem) rather easily without actually needing to use recursion.

Implementation
--------------
The way to solve this is using a recursive-descent algorithm using a while loop.  The basic structure of this loop is:

::

    todo = [[item1, processing_data],[item2, processing_data], ... ]
    done = []
    while len(todo)>0:
        item_to_workon = todo.pop()

        for each_branch in branches:
            stuff.do()
            data.process()

            if end_condition.met()
                done.append(processing_data)
            else
                todo.append([stuff, processing_data])

    return done

That is, pop an item off the todo list, process the node, and put the resulting nodes back on the todo list (unless the end condition is met in which case it's done).  Then return the done list when your todo list is empty.

So it starts with the first letter, tries one or two element combinations, and, if it succeeds in finding a match, puts the `item` (remaining characters) back on the todo list along with `processing data`, i.e. the list of elements.  If it runs out of possible paths through the rest of the word and you haven't hit the end of the word, that means that you can't spell it with the given elements.

This implementation, I hope you'll agree, is a lot cleaner and understandable than using recursion.  It's also less computationally intensive because you don't need to redefine a new variable space with its own scope at every node (i.e. every function call), thereby using less resources.

Getting the library
-------------------
To get the library, `pip install chemify`.


Using the library
-----------------
The library contains two functions, `chemify` and `chemify_words`. The first is targeted at single words or lists of words, the latter is a rather quick way to run through a phrase keeping the words separate (i.e. the last letter of a word won't be combined with the first letter of the next).

An example is:

::

  >>> from chemify import chemify
  >>> chemify('georgescu')
  ['[Ge][O][Rg][Es][Cu]', '[Ge][O][Rg][Es][C][U]']

  >>> chemify('georgescu',shortest=True)`
  '[Ge][O][Rg][Es][Cu]'

or:

::

  >>> from chemify import chemify_words
  >>> chemify_words('In case of fire, use stairs.')
  '[In] [Ca][Se] [O][F] [F][I][Re] [U][Se] [S][Ta][Ir][S]'

but:

::

  >>> chemify_words('In case of fire, do not use elevator')
   "do" failed to convert
   "not" failed to convert
   "elevator" failed to convert

Look at the function help for more input/output options, output upon success or failure to convert, custom elements, etc.

Misc
----

Email nsgeorgescu@gmail.com with issues and questions or open an issue at https://github.com/NGeorgescu/chemify or if you think there's some functionality that would be cool to add.

Thanks and Enjoy!




