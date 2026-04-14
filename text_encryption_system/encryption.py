import string

# Helper function to shift characters with wrap-around
def shift_char(c, shift):
    if c.islower():
        base = ord('a')
        return chr((ord(c) - base + shift) % 26 + base)
    elif c.isupper():
        base = ord('A')
        return chr((ord(c) - base + shift) % 26 + base)
    else:
        return c


def encrypt_text(text, shift1, shift2):
    encrypted = ""

    for c in text:
        # LOWERCASE
        if c.islower():
            if 'a' <= c <= 'm':
                shift = shift1 * shift2
                encrypted += shift_char(c, shift)
            else:  # n-z
                shift = -(shift1 + shift2)
                encrypted += shift_char(c, shift)

        # UPPERCASE
        elif c.isupper():
            if 'A' <= c <= 'M':
                shift = -shift1
                encrypted += shift_char(c, shift)
            else:  # N-Z
                shift = shift2 ** 2
                encrypted += shift_char(c, shift)

        # OTHER CHARACTERS
        else:
            encrypted += c

    return encrypted


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


# MAIN EXECUTION
if __name__ == "__main__":
    input_file = "raw_text.txt"
    output_file = "encrypted_text.txt"

    try:
        shift1 = int(input("Enter shift1: "))
        shift2 = int(input("Enter shift2: "))

        encrypt_file(input_file, output_file, shift1, shift2)

    except ValueError:
        print(" Please enter valid integer values for shifts.")
