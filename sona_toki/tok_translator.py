
from sona_toki.word_classes import *

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
    
    for t, token in enumerate(parse):
        if type(token) in phrases:
            penalty += len([token.head] + token.adjectives) * 5
            # Penalise for uncertain numbers very lightly
            if token.number:
                if token.number % 5 == 0 and not token.ordinal: # ale/ali, mute, luka
                    penalty += 10
                elif not token.ordinal:
                    penalty += 5
            
        elif type(token) == ContextPhrase:
            penalty += rank_parse(token.tokens)
        
        elif type(token) == Interjection:
            penalty += 2
    return penalty

def translate_phrase():
    ...