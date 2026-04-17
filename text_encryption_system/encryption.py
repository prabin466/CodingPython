import string

# Helper function (unchanged)
def shift_char(c, shift):
    if c.islower():
        base = ord('a')
        return chr((ord(c) - base + shift) % 26 + base)
    elif c.isupper():
        base = ord('A')
        return chr((ord(c) - base + shift) % 26 + base)
    else:
        return c


# NEW: Clean, invertible encryption
def encrypt_char(c, shift1, shift2):
    if c.islower():
        shift = shift1 * shift2                     # same rule for ALL lowercase
        return shift_char(c, shift)

    elif c.isupper():
        shift = shift2 ** 2                         # same rule for ALL uppercase
        return shift_char(c, shift)

    return c


def encrypt_text(text, shift1, shift2):
    return "".join(encrypt_char(c, shift1, shift2) for c in text)


def encrypt_file(input_file, output_file, shift1, shift2):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()

        encrypted = encrypt_text(text, shift1, shift2)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(encrypted)

        print("Encryption completed successfully.")

    except FileNotFoundError:
        print("Input file not found.")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    input_file = "raw_text.txt"
    output_file = "encrypted_text.txt"

    try:
        shift1 = int(input("Enter shift1: "))
        shift2 = int(input("Enter shift2: "))
        encrypt_file(input_file, output_file, shift1, shift2)
    except ValueError:
        print("Please enter valid integer values for shifts.")
