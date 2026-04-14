# Helper function for shifting with wrap-around
def shift_char(c, shift):
    if c.islower():
        base = ord('a')
        return chr((ord(c) - base + shift) % 26 + base)
    elif c.isupper():
        base = ord('A')
        return chr((ord(c) - base + shift) % 26 + base)
    else:
        return c


def decrypt_text(text, shift1, shift2):
    result = ""

    for c in text:
        # LOWERCASE
        if c.islower():
            # Reverse rule for a-m
            candidate = shift_char(c, -(shift1 * shift2))
            if 'a' <= candidate <= 'm':
                result += candidate
            else:
                # Reverse rule for n-z
                result += shift_char(c, (shift1 + shift2))

        # UPPERCASE
        elif c.isupper():
            # Reverse rule for A-M
            candidate = shift_char(c, shift1)
            if 'A' <= candidate <= 'M':
                result += candidate
            else:
                # Reverse rule for N-Z
                result += shift_char(c, -(shift2 ** 2))

        # OTHER CHARACTERS (unchanged)
        else:
            result += c

    return result


def decrypt_file(input_file, output_file, shift1, shift2):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            encrypted_text = f.read()

        decrypted_text = decrypt_text(encrypted_text, shift1, shift2)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(decrypted_text)

        print("Decryption completed successfully.")

    except FileNotFoundError:
        print("Encrypted file not found.")
    except Exception as e:
        print("Error:", e)





# MAIN
if __name__ == "__main__":
    encrypted_file = "encrypted_text.txt"
    decrypted_file = "decrypted_text.txt"
    original_file = "raw_text.txt"

    try:
        shift1 = int(input("Enter shift1: "))
        shift2 = int(input("Enter shift2: "))

        decrypt_file(encrypted_file, decrypted_file, shift1, shift2)

    except ValueError:
        print("Please enter valid integers.")
