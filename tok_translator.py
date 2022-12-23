
from word_classes import *

def rank_parse(parse):
    # Penalise for overzealous length
    penalty = len(parse) * 3  
    phrases = [
        YNQuestion,
        Predicate,
        Subject,
        Option,
        Verb,
        ImpPredicate,
        ImpVerb,
        DirectObject,
        IndirectObject,
        AddSubject,
        Means,
        Location,
        Similar,
        Cause,
        Modifier
    ]
    # Limit no. of items in each phrase
    
    for token in parse:
        if type(token) in phrases:
            penalty += len([token.head] + token.adjectives) * 5
            # Penalise for uncertain numbers very lightly
            if token.number:
                if token.number % 5 == 0: # ale/ali, mute, luka
                    penalty += 10
                elif not token.ordinal:
                    penalty += 5
        elif type(token) == ContextPhrase:
            penalty += rank_parse(token.tokens) 
    
    return penalty

def translate_phrase():
    ...