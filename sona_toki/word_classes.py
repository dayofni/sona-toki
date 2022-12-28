
class Phrase:
    def __init__(self, token, tag):
        self.head = (token, tag)
        self.adjectives = []
        self.types = ["generic"]
        self.number = None
        self.ordinal = False
        
        self.values = [(token, tag)]
        
        if tag == "question_token":
            self.types.append("question")
        
        if len(self.types) > 1 and "generic" in self.types:
            self.types.remove("generic")
    
    def set_number(self, number):
        self.number = number.value
        self.ordinal = number.ordinal

    def add(self, token, tag):
        if tag == "preverb":
            self.types.append("verb")
        elif tag == "question_token":
            self.types.append("question")
        
        if len(self.types) > 1 and "generic" in self.types:
            self.types.remove("generic")
        
        self.values.append((token, tag))
        self.adjectives.append((token, tag))
    
    def __repr__(self, mode="type"):
        return f"Phrase({self.values}, number={self.number}, ordinal={self.ordinal}, ordinal={self.ordinal})"
    
    def __hash__(self):
        #* I don't know how to do this well, so excuse my horrible code
        struct = [self.head, self.number, self.ordinal] + self.adjectives + self.types
        return hash(tuple(struct))

class Number:
    def __init__(self, token, ordinal=False):
        self.value = 0
        self.ordinal = ordinal
        self.tokens = [(token, "number_token")]
        self.add(token)
    
    def add(self, token):
        values = {
            "wan": 1,
            "tu": 2,
            "luka": 5,
            "mute": 20,
            "ale": 100,
            "ali": 100,
            "nanpa": 0
        }
        self.value += values[token]
        self.tokens.append((token, "number_token"))
        #print(self.value, self.ordinal)
    
    def __repr__(self):
        return f"Number({self.value}, ordinal={self.ordinal})"
    
    def __hash__(self):
        #* I don't know how to do this well, so excuse my horrible code
        struct = [self.value, self.ordinal] + self.tokens
        return hash(tuple(struct))

class YNQuestion:
    def __init__(self, phrase):
        self.head = phrase.head
        self.adjectives = phrase.adjectives
        self.values = phrase.values
    
    def __repr__(self):
        values = [self.head] + self.adjectives
        return f"YNQuestion({values})"

class Object:
    def __init__(self, phrase, ignore_li=False):
        self.head = phrase.head
        self.adjectives = phrase.adjectives
        self.types = phrase.types
        self.number = phrase.number
        self.ignore_li = ignore_li
        self.ordinal = phrase.ordinal
        self.values = phrase.values
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"Object({values}, number={self.number})"
    
    def __hash__(self):
        #* I don't know how to do this well, so excuse my horrible code
        struct = [self.head, self.number, self.ignore_li, self.ordinal] + self.adjectives + self.types
        return hash(tuple(struct))

class Predicate:
    def __init__(self, phrase):
        if type(phrase) == Phrase:
            self.head = phrase.head
            self.adjectives = phrase.adjectives
            self.types = phrase.types
            self.number = phrase.number
            self.ordinal = phrase.ordinal
            self.values = phrase.values
        elif type(phrase) == YNQuestion:
            self.head = phrase.head
            self.adjectives = phrase.adjectives
            self.types = ["YNQuestion"]
            self.number = None
            self.ordinal = False
            self.values = phrase.values
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"Predicate({values}, number={self.number}, ordinal={self.ordinal}, types={self.types})"
    
    def __hash__(self):
        #* I don't know how to do this well, so excuse my horrible code
        struct = [self.head, self.number, self.ordinal] + self.adjectives + self.types
        return hash(tuple(struct))

class ContextPhrase:
    def __init__(self, tokens):
        self.tokens = tokens
    
    def __repr__(self):
        return f"ContextPhrase({self.tokens})"
    
    def __hash__(self):
        return hash(tuple(self.tokens))

#! Subclasses

class Subject(Object):
    def __init__(self, phrase, ignore_li=False):
        super().__init__(phrase, ignore_li=ignore_li)
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"Subject({values}, number={self.number}, ordinal={self.ordinal}, ignore_li={self.ignore_li})"

class Option(Predicate):
    def __init__(self, phrase):
        super().__init__(phrase)
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"Option({values}, number={self.number}, ordinal={self.ordinal}, types={self.types})"

class Verb(Predicate):
    def __init__(self, phrase):
        super().__init__(phrase)
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"Verb({values}, number={self.number}, ordinal={self.ordinal}, types={self.types})"

class ImpPredicate(Predicate):
    def __init__(self, phrase):
        super().__init__(phrase)
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"ImpPredicate({values}, number={self.number}, ordinal={self.ordinal}, types={self.types})"

class ImpVerb(Predicate):
    def __init__(self, phrase):
        super().__init__(phrase)
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"ImpVerb({values}, number={self.number}, ordinal={self.ordinal}, types={self.types})"

class DirectObject(Object):
    def __init__(self, phrase):
        super().__init__(phrase)
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"DirectObject({values}, number={self.number}, ordinal={self.ordinal}, types={self.types})"

class IndirectObject(Object):
    def __init__(self, phrase):
        super().__init__(phrase)
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"IndirectObject({values}, number={self.number}, ordinal={self.ordinal}, types={self.types})"

class AddSubject(Object):
    def __init__(self, phrase):
        super().__init__(phrase)
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"AddSubject({values}, number={self.number}, ordinal={self.ordinal}, types={self.types})"

class Means(Object):
    def __init__(self, phrase):
        super().__init__(phrase)
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"Means({values}, number={self.number}, ordinal={self.ordinal}, types={self.types})"

class Location(Object):
    def __init__(self, phrase):
        super().__init__(phrase)
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"Location({values}, number={self.number}, ordinal={self.ordinal}, types={self.types})"

class Similar(Object):
    def __init__(self, phrase):
        super().__init__(phrase)
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"Similar({values}, number={self.number}, ordinal={self.ordinal}, types={self.types})"

class Cause(Object):
    def __init__(self, phrase):
        super().__init__(phrase)
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"Cause({values}, number={self.number}, ordinal={self.ordinal}, types={self.types})"

class Interjection(Object):
    def __init__(self, phrase):
        super().__init__(phrase)
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"Interjection({values})"

class Modifier(Object):
    def __init__(self, phrase):
        super().__init__(phrase)
    
    def __repr__(self):
        values = [i[0] for i in [self.head] + self.adjectives]
        return f"Modifier({values}, number={self.number}, ordinal={self.ordinal}, types={self.types})"

class Vocative(ContextPhrase):
    def __init__(self, tokens):
        super().__init__(tokens)
    
    def __repr__(self):
        return f"Vocative({self.tokens})"