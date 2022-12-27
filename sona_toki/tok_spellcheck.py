
import json

from sona_toki.base import *

with open("sona_toki/data/parts_of_speech.json") as f:
    #! Let's do this *once*
    categories = json.loads(f.read())
    word_tags = {}
    for k, v in categories.items():
        for word in v:
            if word in word_tags.keys():
                word_tags[word].append(k)
            else:
                word_tags[word] = [k]

class SpellcheckParser(Parser):
    def __init__(self, tokens, tags):
        super().__init__(tokens, tags)
    
    def run(self):
        self.parse_text()
        #print(self.parse)
        self.parse, self.fails = self.check_grammar()
    
    def check_grammar(self, inp=None, context=False):
        
        if inp == None:
            inp = self.parse
        
        allowed_types = [
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
            Interjection,
            ContextPhrase,
            Modifier
        ]
        
        fails = []
        
        #! Find any incomplete parses
        
        if any([type(i) not in allowed_types for i in inp]):
            #! Look, it's a string. A particle's in the wrong spot. OTHERWISE WE HAVE A PROBLEM.
            if any([i == "unknown" not in allowed_types for i in inp]):
                fails.append("UNKNOWN_WORD")
            if any([type(i) not in allowed_types and i != "unknown" for i in inp]):
                fails.append("HANGING_PARTICLE")
            #return []
        
        if len(self.tokens) > 0 and self.tokens[0] in word_tags.keys():
            ignore_li = "ignore_li" in word_tags[self.tokens[0]]
            #print(ignore_li)
        elif len(self.tokens) <= 0:
            fails.append("LENGTH_ERROR")
            ignore_li = False
        else:
            fails.append("PREDICATE_BEFORE_SUBJECT")
            ignore_li = False
        
        
        parse = []
        
        subject_passed = False
        imperative = False
        predicate_verb_passed = False
        
        
        for token in inp:
            parse.append(token)
            if type(token) == Subject:
                #print(ignore_li, token.ignore_li)
                if "ignore_li" in word_tags[token.head[0]] and "li" in self.tokens:
                    fails.append("LI_NOT_IGNORED")
                if subject_passed or (ignore_li and not token.ignore_li):
                    fails.append("HANGING_PHRASE")
                elif token.number == 0 and token.ordinal:
                    fails.append("ZEROTH_ORDINAL")
                else:
                    subject_passed = True
            elif type(token) == AddSubject:
                if not subject_passed:
                    fails.append("EN_BEFORE_SUBJECT")
                elif predicate_verb_passed:
                    fails.append("EN_AFTER_PREDICATE")
            elif type(token) in [Verb, Predicate, ImpVerb, ImpPredicate]:
                if token.number != None and type(token) not in [Predicate, ImpPredicate]:
                    fails.append("NUMBERED_VERB")
                if type(token) in [ImpVerb, ImpPredicate]:
                    imperative = True
                elif not subject_passed:
                    fails.append("PREDICATE_BEFORE_SUBJECT")
                predicate_verb_passed = True
            elif type(token) in [DirectObject, IndirectObject, Means, Location, Similar, Cause]:
                if not predicate_verb_passed:
                    fails.append("FINAL_WITHOUT_PREDICATE")
            elif type(token) == Interjection:
                if context and not subject_passed and len(inp) == 1:
                    fails.append("LONE_INTERJECTION_AS_CONTEXT")
            elif type(token) == Modifier:
                if token.adjectives == [] and not token.number:
                    fails.append("SOLE_WORD_PI_PHRASE")
            elif type(token) == ContextPhrase:
                phrase_parse, phrase_fails = self.check_grammar(token.tokens, context=True)
                fails += phrase_fails
        if fails != []:
            parse = []
        return parse, fails

# Priority 0: Common errors
# Priority 1: Nitpicky grammar (x5)
# Priority 2: Actual errors (x10)

error_codes = {
    "UNKNOWN_WORD": 2,
    "HANGING_PARTICLE": 0,
    "LENGTH_ERROR": 2,
    "NO_SUBJECT": 2,
    "HANGING_PHRASE": 0,
    "ZEROTH_ORDINAL": 1,
    "EN_BEFORE_SUBJECT": 2,
    "EN_AFTER_PREDICATE": 2,
    "NUMBERED_VERB": 1,
    "PREDICATE_BEFORE_SUBJECT": 2,
    "FINAL_WITHOUT_PREDICATE": 2,
    "LONE_INTERJECTION_AS_CONTEXT": 2,
    "SOLE_WORD_PI_PHRASE": 1,
    "LI_NOT_IGNORED": 2
}

def spellcheck(string):
    sentences = lexer(string)
    #print(sentences)
    sentence_interps = {}
    for sentence in sentences:
        inters = generate_interpretations(sentence)
        allowed_inters = []
        fails = []
        for interp in inters:
            parser = SpellcheckParser(sentence, interp)
            if parser.parse != []:
                allowed_inters.append(parser.parse)
            fails += parser.fails
        if allowed_inters != []:
            wrongdoing = []
        else:
            wrongdoing = {}
            for f in fails:
                if f in wrongdoing.keys():
                    wrongdoing[f] += max(1, 1 * (5 * error_codes[f]))
                else:
                    wrongdoing[f] = max(1, 1 * (5 * error_codes[f]))
            wrongdoing = sorted(wrongdoing.keys(), key=wrongdoing.get)[::-1]
            
    return wrongdoing

spellcheck("nimi tokija li pona a")