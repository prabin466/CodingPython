# Text Encryption and Decryption System

## Overview

This project implements a text encryption and decryption system based on specific transformation rules. It reads input text from a file, applies encryption, then reverses the process through decryption, and finally verifies correctness.

---

## File Structure

* `encryption.py`
  Handles encryption of text from `raw_text.txt` and writes to `encrypted_text.txt`.

* `decryption.py`
  Decrypts `encrypted_text.txt` and writes the result to `decrypted_text.txt`.

* `verification.py`
  Compares `raw_text.txt` and `decrypted_text.txt` to verify correctness.

* `raw_text.txt`
  Original input text.

* `encrypted_text.txt`
  Encrypted output.

* `decrypted_text.txt`
  Decrypted output.

---

## Encryption Rules

### Lowercase Letters

* 'a' to 'm': shift forward by (shift1 × shift2)
* 'n' to 'z': shift backward by (shift1 + shift2)

### Uppercase Letters

* 'A' to 'M': shift backward by shift1
* 'N' to 'Z': shift forward by (shift2²)

### Other Characters

* Remain unchanged

---

## How to Run

### Step 1: Encrypt the Text

Run:
python q1_encryption_system.py

Enter values for:

* shift1
* shift2

---

## Expected Output

* `encrypted_text.txt` will contain encrypted content.
* `decrypted_text.txt` should match `raw_text.txt`.
* Verification will confirm whether decryption is correct.

---

## Notes

* Ensure the same shift values are used for both encryption and decryption.
* Files must be in the same directory.
* The system preserves spaces, punctuation, and non-alphabet characters.

---

## Author

Student Name: Mst Nowal Ahmed Jarin
Course: HIT137
Assignment: Assignment 2
