def sculptor(text: str):
    res = []
    is_lower = True

    for c in text:
        if c.isalpha():
            res.append(c.lower() if is_lower else c.upper())
            is_lower = not is_lower
        else:
            res.append(c)
    
    return "".join(res)

# print(sculptor("123abcDEF"))
