from sona_toki.base import *
from pprint import pprint

def translate_string(string):
    sentences = lexer(string)
    #print(sentences)
    sentence_interps = []
    
    for sentence in sentences:
        print(" ".join(sentence), "\n----------------------------------------------------------\n")
        
        inters = generate_interpretations(sentence)
        allowed_inters = []
        errors = []
        
        for interp in inters:
            parser = Parser(sentence, interp)
            if parser.parse != []:
                allowed_inters.append(parser.parse)
            else:
                errors += parser.errors
        
        if allowed_inters != []:
            wrongdoing = []
            interpretations = set([tuple(i) for i in allowed_inters])
            interpretations = sorted(list(interpretations), key=rank_parse)
            for interp in interpretations[:5]:
                print(gloss_parse(interp))
                print(rank_parse(interp), "\n")
        else:
            wrongdoing = {}
            for e in errors:
                if e in wrongdoing.keys():
                    wrongdoing[e] += max(1, 1 * (5 * ERROR_CODES[e]))
                else:
                    wrongdoing[e] = max(1, 1 * (5 * ERROR_CODES[e]))
            wrongdoing = sorted(wrongdoing.keys(), key=wrongdoing.get)[::-1]
            print(wrongdoing)
        
        sentence_interps.append(allowed_inters)
    return sentence_interps

#translate_string("pana sona")
print()
translate_string("sina en ona o!")
print()