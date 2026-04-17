# Helper function (unchanged)
def shift_char(c, shift):
    if c.islower():
        base = ord('a')
        return chr((ord(c) - base + shift) % 26 + base)
    elif c.isupper():
        base = ord('A')
        return chr((ord(c) - base + shift) % 26 + base)
    return c


 
def decrypt_char(c, shift1, shift2):
    if c.islower():
        shift = shift1 * shift2
        return shift_char(c, -shift)

    elif c.isupper():
        shift = shift2 ** 2
        return shift_char(c, -shift)

    return c


def decrypt_text(text, shift1, shift2):
    return "".join(decrypt_char(c, shift1, shift2) for c in text)


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


if __name__ == "__main__":
    encrypted_file = "encrypted_text.txt"
    decrypted_file = "decrypted_text.txt"

    try:
        shift1 = int(input("Enter shift1: "))
        shift2 = int(input("Enter shift2: "))
        decrypt_file(encrypted_file, decrypted_file, shift1, shift2)
    except ValueError:
        print("Please enter valid integers.")
