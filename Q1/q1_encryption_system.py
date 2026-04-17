# ========================================================
# HIT137 - Group Assignment 2 - Question 1
# Complete encryption/decryption/verification system
# ========================================================

import string

# Helper function (unchanged)
def shift_char_en(c, shift):
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
        return shift_char_en(c, shift)

    elif c.isupper():
        shift = shift2 ** 2                         # same rule for ALL uppercase
        return shift_char_en(c, shift)

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


# ====================== DECRYPTION ======================

# Helper function (unchanged)
def shift_char_de(c, shift):
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
        return shift_char_de(c, -shift)

    elif c.isupper():
        shift = shift2 ** 2
        return shift_char_de(c, -shift)
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



# ====================== VERIFICATION ======================

def verify_files(original_file, decrypted_file):
    try:
        with open(original_file, 'r', encoding='utf-8') as f1:
            original = f1.read()

        with open(decrypted_file, 'r', encoding='utf-8') as f2:
            decrypted = f2.read()

        if original == decrypted:
            print("Verification successful: Decryption is correct.")
            return True
        else:
            print("Verification failed: Files do NOT match.")
            return False

    except FileNotFoundError:
        print("One or both files not found.")
        return False
    except Exception as e:
        print("Error during verification:", e)
        return False



# ====================== MAIN PROGRAM ======================

if __name__ == "__main__":
    print("HIT137 - Group Assignment 2 - Question 1")
    print("=" * 55)

    # 1. Get shifts from user
    try:
        shift1 = int(input("\nEnter shift1: "))
        shift2 = int(input("Enter shift2: "))
    except ValueError:
        print("Please enter valid integer values for shifts.")
        exit()

    # 2. Encrypt
    encrypt_success = encrypt_file("raw_text.txt", "encrypted_text.txt", shift1, shift2)

    # 3. Decrypt
    decrypt_success = decrypt_file("encrypted_text.txt", "decrypted_text.txt", shift1, shift2)

    # 4. Verify
    print("\n" + "=" * 55)
    verify_files("raw_text.txt", "decrypted_text.txt")
