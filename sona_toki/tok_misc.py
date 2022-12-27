
import json
from sona_toki.word_classes import *

with open("sona_toki/data/gloss.json") as f:
    gloss_data = json.loads(f.read())

gloss_classes = {
    Subject: "SUB",
    Predicate: "PRED",
    Verb: "VERB",
    ImpPredicate: "IMP.PRED",
    ImpVerb: "IMP.VERB",
    DirectObject: "OBJ",
    IndirectObject: "INDIRECT.OBJ",
    Modifier: "MOD",
    Option: "OR",
    Means: "MEANS",
    Location: "LOC",
    Similar: "SAME",
    Interjection: "INTJ",
    AddSubject: "SUB"
}

numerical = [
    Predicate,
    Subject,
    Option,
    Verb,
    ImpPredicate,
    ImpVerb,
    DirectObject,
    AddSubject,
    Means,
    Location,
    Similar,
    Cause,
    Modifier
]

has_types = [
    Predicate,
    Verb,
    ImpPredicate,
    ImpVerb
]


def gloss_parse(parse):
    gloss = []
    for token in parse:
        if type(token) in gloss_classes.keys():
            if type(token) in numerical and token.number != None:
                if token.ordinal:
                    gloss.append(["ORD.%s"%str(token.number)])
                else:
                    gloss.append([str(token.number)])
            else:
                gloss.append([])
            
            if type(token) in has_types and "YNQuestion" in token.types:
                gloss[-1].append("YNQ")
            
            gloss[-1].append(gloss_classes[type(token)])
            
            for word, _ in token.values:
                if word in gloss_data.keys():
                    gloss[-1].append(gloss_data[word])
                else:
                    gloss[-1].append(word)
        elif type(token) == ContextPhrase:
            gloss.append([f"CONTEXT-[{gloss_parse(token.tokens)}]"])
    #print(gloss)
    gloss = " ".join(["-".join(i) for i in gloss])
    return gloss

def find_syllables(token):
    syls = []
    current = token
    possible = sorted(([i for i in syllables if i in token]))[::-1]
    while current != "":
        for s, syl in enumerate(possible):
            if syl == current[:len(syl)]:
                syls.append(syl)
                current = current[len(syl):]
                break
        if s == len(syllables) - 1 and current != "":
            return []
    ret = []
    ignore = False
    for s, syl in enumerate(syls):
        if ignore:
            ignore = False
            continue
        
        if s != len(syls) - 1:
            forward = syls[s+1]
        else:
            forward = ""
        
        if forward == "n":
            ret.append(syl + "n")
            ignore = True
        else:
            ret.append(syl)
    return ret