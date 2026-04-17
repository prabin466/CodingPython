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

# decrypt like encrypt
def build_decrypt_dictionaries(shift1, shift2):
    lower_decrypt = {}
    upper_decrypt = {}

    for ch in lowercase_letters:
        encrypted_char = encrypt_char(ch, shift1, shift2)
        lower_decrypt[encrypted_char] = ch

    for ch in uppercase_letters:
        encrypted_char = encrypt_char(ch, shift1, shift2)
        upper_decrypt[encrypted_char] = ch

    return lower_decrypt, upper_decrypt

def decrypt_char(ch, lower_decrypt, upper_decrypt):
    if ch in lower_decrypt:
        return lower_decrypt[ch]
    elif ch in upper_decrypt:
        return upper_decrypt[ch]
    else:
        return ch

def decrypt_file(shift1, shift2):
    with open("encrypted_text.txt", "r", encoding="utf-8") as file:
        encrypted_text = file.read()

    lower_decrypt, upper_decrypt = build_decrypt_dictionaries(shift1, shift2)

    decrypted_text = ""

    for ch in encrypted_text:
        decrypted_text += decrypt_char(ch, lower_decrypt, upper_decrypt)

    with open("decrypted_text.txt", "w", encoding="utf-8") as file:
        file.write(decrypted_text)

    return decrypted_text
#verify

def verify_decryption():
    with open("raw_text.txt", "r", encoding="utf-8") as file:
        original_text = file.read()

    with open("decrypted_text.txt", "r", encoding="utf-8") as file:
        decrypted_text = file.read()

    if original_text == decrypted_text:
        print("Decryption was successful.")
    else:
        print("Decryption failed.")


def main():
    try:
        shift1 = int(input("Enter shift1: "))
        shift2 = int(input("Enter shift2: "))
    except ValueError:
        print("Please enter integer values only.")
        return

    encrypt_file(shift1, shift2)
    print("Encryption completed. Output saved to encrypted_text.txt")

    decrypt_file(shift1, shift2)
    print("Decryption completed. Output saved to decrypted_text.txt")

    verify_decryption()


main()


