# Creat lowercase and uppercase alphabet dictionary to match letters with their postionas
lowercase_letters = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]

uppercase_letters = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

lowercase_index = {}
uppercase_index = {}

for i in range(26):
    lowercase_index[lowercase_letters[i]] = i
    uppercase_index[uppercase_letters[i]] = i

# make a function for make letter forward
def shift_char_forward(ch, step, start):
    if start == 'a':    # the situationo for lowercase letter
        letters = lowercase_letters
        index_dict = lowercase_index
    else:    # for uppercase letter
        letters = uppercase_letters
        index_dict = uppercase_index

    current_index = index_dict[ch]    
    new_index = (current_index + step) % 26  # find the new position

    return letters[new_index]

# make a function for make letter backward like forward
def shift_char_backward(ch, step, start):
    if start == 'a':
        letters = lowercase_letters
        index_dict = lowercase_index
    else:
        letters = uppercase_letters
        index_dict = uppercase_index

    current_index = index_dict[ch]
    new_index = (current_index - step) % 26

    return letters[new_index]

# encrypt
def encrypt_char(ch, shift1, shift2):
    if 'a' <= ch <= 'm':    # for lowercase a to m
        step = shift1 * shift2
        return shift_char_forward(ch, step, 'a')

    elif 'n' <= ch <= 'z':    # for lowercase n to z
        step = shift1 + shift2
        return shift_char_backward(ch, step, 'a')

    elif 'A' <= ch <= 'M':    # for uppercase A to M
        step = shift1
        return shift_char_backward(ch, step, 'A')

    elif 'N' <= ch <= 'Z':    # for uppercase N to Z
        step = shift2 ** 2
        return shift_char_forward(ch, step, 'A')

    else:    # for other character,keep same
        return ch
# encrypt for the file
def encrypt_file(shift1, shift2):
    with open("raw_text.txt", "r", encoding="utf-8") as file:
        original_text = file.read()

    encrypted_text = ""

    for ch in original_text:
        encrypted_text += encrypt_char(ch, shift1, shift2)

    with open("encrypted_text.txt", "w", encoding="utf-8") as file:
        file.write(encrypted_text)

    return encrypted_text


