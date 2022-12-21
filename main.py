from tok_lexer import *
from tok_parser import *
from pprint import pprint

# Example use of tok_lexer and tok_parser.

def translate_string(string):
    sentences = lexer(string)
    #print(sentences)
    
    for sentence in sentences:
        print(" ".join(sentence), "\n----------------------------------------------------------\n")
        inters = generate_interpretations(sentence)
        allowed_inters = []
        for interp in inters:
            parser = Parser(sentence, interp)
            if parser.parse != []:
                allowed_inters.append(parser.parse)
        for interp in allowed_inters:
            pprint(interp)
            print()
    return allowed_inters

#translate_string("pana sona")
print()
translate_string("sina toki ala toki e toki pona? mi ken la mi ken pana e sona pi toki pona")
print()