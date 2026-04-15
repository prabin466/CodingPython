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


# MAIN
if __name__ == "__main__":
    original_file = "raw_text.txt"
    decrypted_file = "decrypted_text.txt"

    verify_files(original_file, decrypted_file)
