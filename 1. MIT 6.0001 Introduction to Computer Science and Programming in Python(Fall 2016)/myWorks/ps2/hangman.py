# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    for secret_char in secret_word.lower():
        if not secret_char in letters_guessed:
            return False  
        
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    presented_str = ""
    
    for secret_char in secret_word.lower():
        if secret_char in letters_guessed:
            presented_str += secret_char
        else:
            presented_str += "_ "
    
    return presented_str



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    presented_str = ""
    
    for char in string.ascii_lowercase:
        if char not in letters_guessed:
            presented_str += char
    
    return presented_str
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # initialze hello
    lives = 12
    user_inputs = []
    warnings = 3
    valid_input = get_available_letters(user_inputs) + get_available_letters(user_inputs).upper()
    print("Welcome to the game Hangman")
#    print("Quit the game by inserting \"break\"")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    print("you have %d warnings left" %(warnings))
    
   # main loop
    while lives > 0 and not is_word_guessed(secret_word, user_inputs):
        # starts
        print("--------------------")
        if warnings <0:
            warnings = 0
        print("You have %d guesses left." %(lives))
        print("Available letters: %s" %(get_available_letters(user_inputs)))
        
        # inputs
        lives -= 1
        user_input = input("Please guess a letter: ")       
        if user_input == "break":
            return
        
        if user_input in valid_input and len(user_input) > 0:
            if user_input not in user_inputs:
                user_inputs.append(user_input.lower())
            elif user_input in user_inputs:
                if warnings > 0 :
                    warnings -= 1
                    print("Oops! You've already guessed that letter. You now have %d warnings: %s" %(warnings, get_guessed_word(secret_word, user_inputs)))
                    continue
                elif warnings <= 0:
                    print("Oops! You've already guessed that letter. You have no warning left so you lose one guess %s:" %(get_guessed_word(secret_word, user_inputs)))
                    continue
        else:
            if warnings > 0:
                warnings -= 1
                print("Oops! That is not a valid letter. You have %d warnings left: %s" %(warnings, get_guessed_word(secret_word, user_inputs)))
                continue
            elif warnings <= 0:
                print("Oops! That is not a valid letter. You have no warning left so you lose one guess %s:" %(get_guessed_word(secret_word, user_inputs)))
                continue
            
        # check
        if user_input in secret_word:
            lives += 1
            print("Good_guess: %s" %(get_guessed_word(secret_word, user_inputs)))
        else:
            if user_input.lower() in "aeiou":
                lives -= 1
            print("Oops! That letter is not in my word: %s" %(get_guessed_word(secret_word, user_inputs)))
            

         
    if is_word_guessed(secret_word, user_inputs):
        print("--------------------")
        score = lives * len(set(list(secret_word)))
        print("Congratulation, you won! \nYour total score for this game is: %d" %(score))
        return True
    else:
        print("Sorry,you ran put of guesses. The word was %s. " %(secret_word))
        return False
        

        
            
    



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    my_word = "".join(my_word.split())
    if len(my_word) != len(other_word):
        return False
    else:
        for i in range(len(my_word)):
            if my_word[i] == "_":
                continue
            elif my_word[i] != other_word[i]:
                return False
    
    return True

def match_with_guesses(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    return: boolean. True if the guessed character in myword matches that charactor in other_word
            at exact same place and exact same time
    """
    def find(str, ch):
        for i, ltr in enumerate(str):
            if ltr == ch:
                yield i

    my_word = "".join(my_word.split())
    for char in my_word:
        if char == "_":
            continue
        elif my_word.count(char) != other_word.count(char):
            return False
        elif list(find(my_word, char)) != list(find(other_word, char)):
            return False
    
    return True

def non_letter(potential_letters):
    # return a string woth incorrect characters
    non_chars = ""
    for char in string.ascii_lowercase:
        if char not in potential_letters:
            non_chars += char
    
    return non_chars
        
        
def match_with_non_guesses(non_chars, other_word):
    """
    non-word: string with wrong characters
    other_word: string, regular English word
    return: boolean. True if no guessed character in non_word matches that charactor in other_word.
                     False otherwise
    """
    for char in non_chars:
        if char in other_word:
            return False
        
    return True

def show_possible_matches(my_word, available_letters):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    non_chars = non_letter(available_letters + my_word)
    
    matches_words = []
    for word in wordlist:
        if match_with_gaps(my_word, word) and match_with_guesses(my_word, word) and match_with_non_guesses(non_chars, word):
            matches_words.append(word)
    if len(matches_words) == 0:
        print("No matches found")
    else:
        print("Possible matches word are:\n%s" %(" ".join(matches_words)))
        print("Most appeared guessable character is %s" %(best_guess_bot(available_letters, matches_words)))
        
    return
    
    
def best_guess_bot(available_letters , words):
    """
    input: available letters, potential wordlist
    return : the most appeared available letter
    """
    char_count = []
    for char in available_letters:
        word_count = 0
        for word in words:
            if char in word:
                word_count += 1
        char_count.append(word_count)
        
    return available_letters[char_count.index(max(char_count))]
        


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
        # initialze hello
    lives = 6
    user_inputs = []
    warnings = 3
    valid_input = get_available_letters(user_inputs) + get_available_letters(user_inputs).upper()
    print("Welcome to the game Hangman")
#    print("Quit the game by inserting \"break\"")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    print("you have %d warnings left" %(warnings))
    
   # main loop
    while lives > 0 and not is_word_guessed(secret_word, user_inputs):
        # starts
        print("--------------------")
        if warnings <0:
            warnings = 0
        print("You have %d guesses left." %(lives))
        print("Available letters: %s" %(get_available_letters(user_inputs)), end = "")
        
        # inputs
        lives -= 1
        user_input = input("Please guess a letter: ")       
        if user_input == "break":
            return       
        elif user_input == "*":
            lives += 1
            show_possible_matches(get_guessed_word(secret_word, user_inputs), get_available_letters(user_inputs))
            continue
        elif user_input in valid_input and len(user_input) > 0:
            if user_input not in user_inputs:
                user_inputs.append(user_input.lower())
            elif user_input in user_inputs:
                if warnings > 0 :
                    warnings -= 1
                    print("Oops! You've already guessed that letter. You now have %d warnings: %s" %(warnings, get_guessed_word(secret_word, user_inputs)))
                    continue
                elif warnings <= 0:
                    print("Oops! You've already guessed that letter. You have no warning left so you lose one guess %s:" %(get_guessed_word(secret_word, user_inputs)))
                    continue
        else:
            if warnings > 0:
                warnings -= 1
                print("Oops! That is not a valid letter. You have %d warnings left: %s" %(warnings, get_guessed_word(secret_word, user_inputs)))
                continue
            elif warnings <= 0:
                print("Oops! That is not a valid letter. You have no warning left so you lose one guess %s:" %(get_guessed_word(secret_word, user_inputs)))
                continue
            
        # check
        if user_input in secret_word:
            lives += 1
            print("Good_guess: %s" %(get_guessed_word(secret_word, user_inputs)))
        else:
            if user_input.lower() in "aeiou":
                lives -= 1
            print("Oops! That letter is not in my word: %s" %(get_guessed_word(secret_word, user_inputs)))
            

         
    if is_word_guessed(secret_word, user_inputs):
        print("--------------------")
        score = lives * len(set(list(secret_word)))
        print("Congratulation, you won! \nYour total score for this game is: %d" %(score))
        return True
    else:
        print("Sorry,you ran put of guesses. The word was %s. " %(secret_word))
        return False
    pass



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
#    secret_word = choose_word(wordlist)
#    while len(secret_word) <= 8:
#        secret_word = choose_word(wordlist)
#    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
