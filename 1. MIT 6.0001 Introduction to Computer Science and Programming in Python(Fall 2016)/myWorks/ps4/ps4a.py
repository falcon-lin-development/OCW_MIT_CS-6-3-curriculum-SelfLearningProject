# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    assert isinstance(sequence, str), 'are you kidding me?'
    
    # base case:
    if len(sequence) == 1:
        return [sequence, ]
    
    # general case
    else:
        last_char = sequence[0]
        sequence = sequence[1:]
        tem_list = get_permutations(sequence)
        new_list = []
        for word in tem_list:
            for i in range(len(word)+1): # n+1 positions for length n word
                # insert the last_char into different positions of the str
                new_word = word[:i] + last_char + word[i:]
                new_list.append(new_word)
        else:
            new_list = list(set(new_list))
            return new_list
        
if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    
    first_input = 'abc'
    print('Input:', first_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(first_input))
    print()
    
    test_2 = 'kk'
    print('Input:', test_2)
    print('Expected Output:', ['kk', ])
    print('Actual Output:', get_permutations(test_2))
    print()
    
    test_3 = '12a'
    print('Input:', test_3)
    print('Expected Output:', ['12a', '21a', '2a1', '1a2', 'a12', 'a21'])
    print('Actual Output:', get_permutations(test_3))
    print()