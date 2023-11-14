"""
A utility module that provides quick access to useful and commonly needed functions
Initially developed for string manipulation and formatting

Author: Mark Proud <markwproud@protonmail.com
Date: April 2023
File: utilities.py
version: 1.0.0

Notes: A personal library of utilities that is continuously being developed and added to.
       Provides functions that frequently useful such as retrieving delimited substring
"""


# imports

def validate_number_in_string(test_str):
    """
    Improved testing for auditing for a numeric within a string
    prevents entries such as 5x, #4 and returns the stripped number
    Works with multi character digits such as '1#35', which would return '135'
    :param test_str:
    :return: string digit if found
    """
    number = []
    for i in test_str:

        if i.isdigit() and i != '':
            number.append(i)
        else:
            continue
    return ''.join(number)


def right_string(input_string: str, front_delim: str):
    """
    Captures everything in a string to the right of a passed in delimiter
    Can handle whitespace character
    if no delimiter is found or an empty string is passed as delimiter an empty string will be returned
    :param input_string:
    :param front_delim:
    :return: substring to the right of delimiter if found or empty string if not found
    """
    if not isinstance(input_string, str) or not isinstance(front_delim, str):
        return ''

    # Find the index of the delimiter in the input string
    # Returns -1 if not found
    delim_front_NDX = input_string.find(front_delim)

    # delimiter found and not an empty string
    if delim_front_NDX != -1 and len(front_delim) > 0:
        # calculate substring start
        substring_start = delim_front_NDX + len(front_delim)
        # Return all characters following the final character of the delimiter
        return input_string[substring_start:]
    else:
        # no delimiter found return empty string
        return ''


def mid_string(input_string, front_delim, back_delim):
    """
    Captures everything in a string between two delimiters
    Can handle whitespace characters
    If either delimiter is not found or an empty string is passed as a delimiter an empty string will be returned
    :param input_string: string to extract substring from
    :param front_delim: delimiter marking the beginning of the desired substring
    :param back_delim: delimiter marking the end of the desired substring
    :return: substring between the two delimiters if found, otherwise an empty string
    """
    # if not isinstance(input_string, str) or not isinstance(front_delim, str) or isinstance(back_delim, str):
    #     return ''
    # find the index of the front delimiter in the input string
    front_delim_index = input_string.find(front_delim)
    if front_delim_index == -1 or not front_delim:
        # front delimiter not found or an empty string was passed
        return ''

    # find the index of the back delimiter in the input string
    back_delim_index = input_string.find(back_delim, front_delim_index + len(front_delim))
    if back_delim_index == -1 or not back_delim:
        # back delimiter not found or an empty string was passed
        return ''

    # extract the substring between the two delimiters
    return input_string[front_delim_index + len(front_delim):back_delim_index]
