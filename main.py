from tok_lexer import *
from tok_parser import *
from tok_translator import *
from pprint import pprint

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
        interpretations = set([tuple(i) for i in allowed_inters])
        interpretations = sorted(list(interpretations), key=rank_parse)
        for interp in interpretations[:5]:
            pprint(interp)
            print(rank_parse(interp), "\n")
    return allowed_inters

#translate_string("pana sona")
print()
translate_string("sina toki ala toki kepeken toki pona a? ni la o toki pona!")
print()