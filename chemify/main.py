import re

def chemify(string,**kwargs):
    """
    chemify(string or list, failure="none", output="brackets")

    Descripton
    --------
    takes in a string, and outputs the chemical elements that you can 
    use to write that string, ignoring anything that isn't a plain letter
    (letters with diacritics of any kind will be ignored)
    
    If you input a list, it will run it (kwargs and all) on each individual
    items.  If you want words to be done separately, use chemify_words

    
    Options for failure
    --------
    
    - "none" (default): no exception, but returns nothing upon failure
    - "exception": raises exception for inclusion in a try/except block
    
    Options for output
    --------
    examples are for passing in my last name, capitalized

    - "brackets": Like "capitalize" but the elements are bracketed, e.g. ['[Ge][O][Rg][Es][Cu]', '[Ge][O][Rg][Es][C][U]']
    - "capitalize": List of possible capitalizations consistent with the elements, e.g. ['GeORgEsCu', 'GeORgEsCU']
    - "list": Lists of each possible lists of the chemical elements, e.g. [['Ge', 'O', 'Rg', 'Es', 'Cu'], ['Ge', 'O', 'Rg', 'Es', 'C', 'U']]
    - "pass": Just return the input string, e.g. 'Georgescu'
    
    shortest
    --------
    add "shortest==True": returns just one item: the shortest, rather than a whole list (affects "list" and "capitalize")

    
    fake_elements
    --------
    Add extra 'fake' elements to the list just to make a phrase work.
    Some choices that aren't too whacky are 'D' for Deuterium, 'Nt' for Neutron, 'P' for Protium, 'Tr' for Tritium, or other particles.
    Only works with 1- or 2- length items in the list.  Capitalization is not considered.
    
    e.g. chemify('johnathan',output='brackets',fake_elements=['J','An'],shortest=True)) yields [J][O][H][Na][Th][An]
    
    """
    
    if isinstance(string, list):
        return [chemify(i,**kwargs) for i in string]

    
    # This is a regex that just searches for capital and lowercase letters
    string = ''.join(re.findall("[A-Za-z]+",string))
    
    # If there are no capital or lowercase letters
    if len(string)==0:
        raise Exception('no usable characters provided')
    
    #Checking kwargs
    try: failure = kwargs['failure']
    except: failure = 'none'        
    try: output = kwargs['output']
    except: output = 'brackets'
             
    def string_to_chem(string):
        """
        This function takes in the regexed list of characters.  It starts with two
        lists, todo (items which still need to be processed), and done (strings which
        have already been completed.)
        
        The function pops an item off the todo list, and for each successful 'element
        step' forward in that string, pops the item back on the end of the list.  It's
        tricky because you can either have two-element steps (e.g. Na) or one (e.g. N).
        Sometimes what works one way won't work the other.  
        
        It's essentially recursive descent, written as a while loop. I.e. "while
        there are nodes left to traverse, traverse the node and put the resulting 
        nodes back on the left-to-traverse list" (rather than node returning 
        a test of the next level as in a recursive algorithm).
        
        If you run out of todo items before you get one that finished chunking,
        then raise an exception (i.e. "nothing on the todo list and no successes")
        
        Otherwise, return the lowercase list of possible element lists to make
        the string work
        """
        elements=['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 
          'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 
          'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 
          'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 
          'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 
          'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 
          'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 
          'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 
          'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 
          'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 
          'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
        
        if 'fake_elements' in kwargs:
            elements = [*elements, *kwargs['fake_elements']]

        #[[elem w/len(1) like H, O, F, etc.],[Elements with len 2, like Be, He, etc.]]
        elements_by_len = [[i.lower() for i in elements if len(i)==j] for j in [1,2]]
        
        # start the todo list, of with each item of structure:
        # [string_left_to_check, [element_list_already_chunked_out ]]
        todo = [[string.lower(),[]]]
        done = []
        while len(todo)>0:
            workon = todo.pop()
            workon_str = workon[0]
            workon_list = workon[1]
            for n,elem in enumerate(elements_by_len):
                check, remainder = workon_str[:n+1],workon_str[n+1:]
                if check in elem:
                    toadd=[remainder,[*workon_list,check]]
                    if len(remainder)==0:
                        done.append(toadd[1])
                    else:
                        todo.append(toadd)
        if len(done)>0:
            return done
        else:
            raise Exception("No Chemical Element Found")

    def getminlen(items):
        if not isinstance(items,list):
            return items
        else:
            lens = [len(i) for i in items]
            min_len = min(lens)
            for i in items:
                if len(i) == min_len:
                    return i

    
    #try to 
    try: 
        list_of_element_lists = string_to_chem(string)
    
    # this section handles failure
    except:
        if failure == 'none':
            return None
        elif failure == 'exception':
            raise Exception('No Elements Found')
        else:
            raise Exception('Exception: Bad failure option')
    
    else:
        if output == 'list':
            return_val=[[i.capitalize() for i in j]
                     for j in list_of_element_lists]
        elif output == 'capitalize':
            return_val=[''.join([i.capitalize() for i in j]) 
                     for j in list_of_element_lists]
        elif output == 'brackets':
            return_val=[''.join(['[{}]'.format(i.capitalize()) for i in j]) 
                     for j in list_of_element_lists]
        elif output == 'pass':
            return_val=string
        else:
            raise Exception('Exception: bad output option')

        if 'shortest' in kwargs:
            if kwargs['shortest']==True:
                return_val = getminlen(return_val)
        
        return return_val
        
        
def chemify_words(string,**kwargs):
    """
    chemify_words('string with spaces',fake_elements=[list])
    
    returns bracketed (shortest) word list linked by spaces
    
    e.g. chemify_words('In case of fire, use stairs.') returns:
     '[In] [Ca][Se] [O][F] [F][I][Re] [U][Se] [S][Ta][Ir][S]'    

    """
    try:
        fake = kwargs['fake_elements']
    except:
        fake = []
        
    return_val = []
    failed = False
    for i in re.findall('\\w+',string):
        try:
            i = chemify(i,output='brackets',failure='exception',fake_elements=fake,shortest=True)
        except:
            print('\"{}\" failed to convert'.format(i))
            failed = True
        else:
            return_val.append(i)
    if failed:
        return None
    else:
        return ' '.join(return_val)
        
        
        
        
        
        
        
        
        
        
