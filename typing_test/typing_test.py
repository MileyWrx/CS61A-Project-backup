""" Typing Test implementation """

from utils import *
from ucb import main

# BEGIN Q1-5
"*** YOUR CODE HERE ***"
#Q1
def modify(str):
    """ Modify the string by :
        1. removing the empty lines
        2. removing ' ' in the beginning or ending of each string 
    """
    modified_lst = "".join(str.split("\n"))
    modified_lst = str.strip()
    return modified_lst

def lines_from_file(path):
    """ Read the conytent fron the file path and return a modified list
    """
    with open(path,'r') as file:
        file_list = []
        lines = file.readlines()
        for str in lines:
            file_list.append(modify(str))
        return file_list
     
def new_sample(path, i):
    """return the content in the i-th line of the file
    """
    with open(path,'r') as file:
        str = file.readlines()[i]
        return modify(str)

#Q2
def analyze(sample_paragraph, typed_string, start_time, end_time):
    """ Calculate the speed of typing (words per min) and the accuracy percentage:
        (number of right words / index)
    """
    out = []
    splited_sp = sample_paragraph.split()
    splited_ty = typed_string.split()
    out.append(len(typed_string) / 5 * 60 / (end_time - start_time))
    test_len = 0
    if len(splited_sp) <= len(splited_ty):
        test_len = len(splited_sp)
    else:
        test_len = len(splited_ty)
    index = 0
    num_of_yes = 0
    while index < test_len:
        if splited_sp[index] == splited_ty[index]:
            num_of_yes += 1
        index += 1
    if test_len == 0:
        test_len = 1
    out.append(num_of_yes / test_len * 100)
    return out

#Q3
def pig_latin(str):
    """ Translate the user input to pig latin by adding postfix according to
        vowel or consonant letters in the beginning
    """
    vowel = ['a', 'e', 'i', 'o', 'u']
    lst = []
    index = 0
    pig_pre = ""
    for letter in str:
        if letter in vowel:
            while (index < len(str)):
                lst += [str[index]]
                index += 1
            break
        else:
            pig_pre += letter
        index += 1
    if str[0] in vowel:
        translated_str = "".join(lst) + pig_pre + "way"
    else:
        translated_str = "".join(lst) + pig_pre + "ay"
    return translated_str

#Q4
def autocorrect(user_input, words_list, score_function):
    """ Return the number of differences between user input and word in words_list
    """
    if user_input in words_list:
        return user_input
    smallest = 10
    out = user_input
    for word in words_list:
        if score_function(word, user_input) < smallest:
            smallest = score_function(word, user_input)
            out = word
    return out

# Q5
def swap_score(w1, w2):
    """ Return the number of characters we need to substitute to change w1 to w2
    """
    list1, list2 = list(w1), list(w2)
    if list1 == [] or list2 == []:
        return 0
    if list1[0] == list2[0]:
        return swap_score(list1[1:], list2[1:]) + 0
    else:
        return swap_score(list1[1:], list2[1:]) + 1
            
# END Q1-5

# Q6
def score_function(word1, word2):
    """A score_function that computes the edit distance between word1 and word2.
    """
    if len(word1) == 0: 
        return len(word2) - len(word1)
    elif len(word2) == 0:
        return len(word1) - len(word2)
    elif word1[0] == word2[0]: 
        return score_function(word1[1:], word2[1:])
    
    else:
        add_char = score_function(word1, word2[1:]) + 1
        remove_char = score_function(word1[1:], word2) + 1
        substitute_char = score_function(word1[1:], word2[1:]) + 1 
        return min(add_char, remove_char, substitute_char)

KEY_DISTANCES = get_key_distances()
WORD_DATABASE = {}

#Q7
def score_function_accurate(word1, word2):
    """ Take the distance between two swapped letters into consideration,
        calculate and output a more accurate score
    """
    lst_word1, lst_word2 = list(word1), list(word2)
    pre_word1= lst_word1[:]
    for letter in pre_word1:
        if letter in lst_word2:
            lst_word2.remove(letter)
            lst_word1.remove(letter)
    diff_list = sum([lst_word1, lst_word2], [])

    if diff_list[0]:
        str1 = diff_list[0]
    else:
        return score_function(word1, word2)

    if len(diff_list) == 2:
        str2 = diff_list[1]
    else:
        return score_function(word1, word2)
    return KEY_DISTANCES[str1, str2]*4

# Q8
def score_function_final(word1, word2):
    """ An optimization which makes the code run more quickly
    """
    tuple1, tuple2 = (word1, word2), (word2, word1)
    if len(word1) == 0:
        if tuple1 in WORD_DATABASE:
            return WORD_DATABASE[tuple1]
        elif tuple2 in WORD_DATABASE:
            return WORD_DATABASE[tuple2]
        else:
            WORD_DATABASE.update({tuple1: len(word2) - len(word1), tuple2: len(word2) - len(word1)})
            return len(word2) - len(word1)
    elif len(word2) == 0:
        if tuple1 in WORD_DATABASE:
            return WORD_DATABASE[tuple1]
        elif tuple2 in WORD_DATABASE:
            return WORD_DATABASE[tuple2]
        else:
            WORD_DATABASE.update({tuple1: len(word1) - len(word2), tuple2: len(word1) - len(word2)})
        return len(word1) - len(word2)
    elif word1[0] == word2[0]:
        return score_function_final(word1[1:], word2[1:])

    else:
        if tuple1 in WORD_DATABASE:
            return WORD_DATABASE[tuple1]
        elif tuple2 in WORD_DATABASE:
            return WORD_DATABASE[tuple2]
        else:
            add_char = score_function_final(word1, word2[1:]) + 1
            remove_char = score_function_final(word1[1:], word2) + 1
            substitute_char = score_function_final(word1[1:], word2[1:]) + KEY_DISTANCES[word1[0], word2[0]]
            out = min(add_char, remove_char, substitute_char)
            WORD_DATABASE.update({tuple1: out, tuple2: out})
    return out