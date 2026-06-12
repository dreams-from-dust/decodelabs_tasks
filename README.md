# Cybersecrity Internship Projects

# 1. Password Strength Checker

A secure, educational, and interactive tool designed to evaluate password strength based on industry-standard security criteria.

## Overview
This tool helps users understand the fundamental principles of password security. It evaluates passwords in real-time against four key metrics:
* Length (minimum 8 characters)
* Uppercase characters
* Numerical digits
* Special characters

## Features
* **Real-time feedback**: Instant visual feedback as the user types.
* **Security Criteria**: Clear breakdown of met vs. unmet security rules.
* **Interactive UI**: Engaging "Cyber-SOC" inspired design with smooth transitions.
* **Educational Content**: Includes detailed explanations of why specific rules (like length or symbol usage) are critical to preventing brute-force and dictionary attacks.

## How it works
The backend logic uses Python with `re` (Regular Expressions) to validate inputs. It is built to be "Pythonic," using efficient `any()` generators rather than manual loops for optimal performance.

## Getting Started
1. Ensure you have Python installed.
2. Run the application: `python password_checker.py`
3. Access the tool at `http://localhost:8001` in your browser.

# 2. Caesar Cipher - Encrypt & Decrypt

A visual and interactive implementation of the classic Caesar Cipher, designed to teach the fundamentals of symmetric encryption.

## Overview
This tool allows users to encrypt and decrypt messages by shifting letters by a user-defined key. It serves as an educational bridge between simple character manipulation and the complex mathematical models used in modern cryptography.

## Features
* **Dual-Mode**: Toggle between Encryption and Decryption seamlessly.
* **Visual Walkthrough**: An interactive A-Z alphabet row that highlights the specific shift mapping for the selected character.
* **Mathematical Transparency**: Displays the exact formula `(x + n) mod 26` used for every character transformation.
* **Educational Context**: Includes sections on why Caesar ciphers are vulnerable (brute-force, frequency analysis) and how they lead to modern standards like AES.

## How it works
The cipher logic mimics the traditional Caesar shift using Python’s `ord()` and `chr()` functions to perform arithmetic on character codes. It uses modular arithmetic (`% 26`) to ensure the alphabet "wraps around" correctly.

## Getting Started
1. Ensure you have Python installed.
2. Run the application: `python ceasor-cypher.py`
3. Access the tool at `http://localhost:8002` in your browser.
