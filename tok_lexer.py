
def lexer(input_str):
    #? Take the input string and turn it into a series of tokens
    tokens = [[""]]
    for char in input_str:
        # For each character, check it against punctuation
        if char.isalnum():
            tokens[-1][-1] += char
        elif char == " ":
            tokens[-1].append("")
        else:
            tokens.append([])
    
    # Remove blank strings from sentences
    tokens = [[token for token in sentence if token != ""] for sentence in tokens]
    # Remove blank sentences
    tokens = [sentence for sentence in tokens if sentence != []]
    
    return tokens

#print(lexer("toki a! mi jan Le a."))