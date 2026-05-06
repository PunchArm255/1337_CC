def is_palindrome(s: list):
    str = [c.lower() for c in s if c.isalnum()]

    return str == str[::-1]

# print(is_palindrome("Able was I ere I saw Elba"))