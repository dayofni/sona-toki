
import json
from sona_toki.word_classes import *

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
    

def translate_variable_base(n, bases):
    #? Translates a number from base 10 to a number in a base with variable amounts for each 
    digits = []
    if n == 0:
        return [0 for i in bases] # Otherwise would return []
    
    while n > 0:
        for d in bases:
            r = int(n%d) # Find remainder
            n = (n-r)/d  # Find next result
            digits.append(r)
    return digits

def product(seq):
    #? Find the product of an iterable
    n = 1
    for i in seq:
        n *= i
    return n

def find_permutations(syl_pos):
    #? Finds all possible permutations of a set of independent options
    perms = []
    syl_no = [len(i) for i in syl_pos]
    for perm in range(product(syl_no)):
        a = translate_variable_base(perm, syl_no)
        perms.append([syl_pos[i][index] for i, index in enumerate(a)])
    return perms

def generate_interpretations(tokens):
    #! Step 1: take all of the tokens and find what it could apply to
    tags = []
    for token in tokens:
        if token not in word_tags.keys() and token[0].isupper():
            tags.append(["proper_adjective"])
        elif token not in word_tags.keys():
            tags.append(["unknown"])
        else:
            tags.append(word_tags[token])
    
    #! Step 2: generate all possible permutations
    permutations = find_permutations(tags)
    return permutations

class Parser:
    def __init__(self, tokens, tags):
        self.tokens = tokens
        self.tags = tags
        self.length = len(tokens)
        self.run()
    
    def run(self):
        self.parse_text()
        self.parse, self.errors = self.check_grammar()
    
    def parse_text(self):
        parse = {}
        prev_phrase = 0
        phrase_tokens = [
            "content_token",
            "question_token",
            "preverb"
        ]
        
        #? Step 1: determine phrases
        for t, (token, tag) in enumerate(zip(self.tokens, self.tags)):
            if tag in phrase_tokens:
                if t-1 >= 0 and self.tags[t-1] in phrase_tokens:
                    parse[list(parse.keys())[-1]].add(token, tag)
                else:
                    parse[t] = Phrase(token, tag)
            elif tag == "proper_adjective":
                if t-1 >= 0 and self.tags[t-1] in phrase_tokens:
                    parse[list(parse.keys())[-1]].add(token, tag)
            elif tag == "number_token" or tag == "ordinal_marker":
                if t-1 >= 0 and self.tags[t-1] in ["number_token", "ordinal_marker"]:
                    parse[list(parse.keys())[-1]].add(token)
                else:
                    if tag == "number_token":
                        parse[t] = Number(token)
                    else:
                        parse[t] = Number(token, ordinal=True)
                        #print(parse[t])
            else:
                parse[t] = tag
        
        #? Step 2: Apply numbers
        for pos, (i, item) in enumerate(list(parse.items())):
            if type(item) == Number and i - 1 >= 0:
                #print(item)
                back_index = list(parse.keys())[pos - 1]
                if type(parse[back_index]) == Phrase:
                    del parse[i]
                    
                    parse[back_index].set_number(item)
                else:
                    number = Phrase("nanpa", "number_token")
                    number.set_number(item)
                    parse[i] = number
            elif type(item) == Number:
                number = Phrase("nanpa", "number_token")
                number.set_number(item)
                parse[i] = number
        
        #? Step 3: determine y/n questions
        index = 0
        for pos, (i, item) in enumerate(list(parse.items())):
            if item == "yn_question_particle" and pos > 0 and pos < len(parse.items()) - 1:
                back, forward = list(parse.keys())[pos - 1], list(parse.keys())[pos + 1]
                if back >= 0 and forward < self.length:
                    if type(parse[back]) == Phrase and type(parse[forward]) == Phrase:
                        back_val, forward_val = parse[back], parse[forward]
                        if back_val.head[0] == forward_val.head[0]:
                            parse[i] = YNQuestion(forward_val)
                            del (parse[back], parse[forward])
        
        #? Step 4: Apply particles and prepositions
        
        parse_ret = {}
        deleted = []
        
        for _, (i, item) in enumerate(parse.items()):
            
            if i in deleted:
                continue
            
            pos_list = list({k:v for k, v in parse.items() if k not in deleted}.keys())
            pos = pos_list.index(i)
            
            if pos > 0:
                prev_pos = list(parse_ret.keys())[-1]
                prev = parse_ret[prev_pos] 
            else:
                prev = None
            
            if pos + 1 < len(pos_list):
                forward_pos = pos_list[pos + 1]
                forward = parse[forward_pos]
            else:
                forward = None
            
            #! Handle mi/sina ignore li exception
            
            if item == "ignore_li":
                
                parse_ret[i] = Subject(Phrase(self.tokens[i], item), ignore_li=True)
                
                #! Handle a predicate/verb following mi/sina
                if type(forward) in [Phrase, YNQuestion] or forward == "imp_pred_particle":
                    if "direct_object_particle" in self.tags:
                        parse_ret[forward_pos] = Verb(forward)
                    else:
                        parse_ret[forward_pos] = Predicate(forward)
                    if forward != "imp_pred_particle":
                        deleted.append(forward_pos) #? Look, the only other thing it could be is a pred. tag, and that's not grammatical 
            
            #! Predicates and verbs
            
            elif item == "predicate_particle" and forward != None and type(forward) in [Phrase, YNQuestion]:
                if "direct_object_particle" in self.tags or "indirect_object_particle" in self.tags:
                    parse_ret[i] = Verb(forward)
                else:
                    parse_ret[i] = Predicate(forward)
                deleted.append(forward_pos)
            
            elif item == "imp_pred_particle" and forward != None and type(forward) in [Phrase, YNQuestion]:
                if "direct_object_particle" in self.tags or "indirect_object_particle" in self.tags:
                    parse_ret[i] = ImpVerb(forward)
                else:
                    parse_ret[i] = ImpPredicate(forward)
                deleted.append(forward_pos)
            
            #! Handle objects
            
            elif item == "direct_object_particle" and type(forward) == Phrase:
                parse_ret[i] = DirectObject(forward)
                deleted.append(forward_pos)
            elif item == "indirect_object_particle" and type(forward) == Phrase:
                parse_ret[i] = IndirectObject(forward)
                deleted.append(forward_pos)
            
            elif item == "add_subject_particle" and type(forward) == Phrase:
                parse_ret[i] = AddSubject(forward)
                deleted.append(forward_pos)
            
            elif item == "option_particle" and forward != None and type(forward) == Phrase:
                parse_ret[i] = Option(forward)
                deleted.append(forward_pos)
            
            #! Prepositions and interjections
            
            elif item == "means_particle" and forward != None and type(forward) == Phrase:
                parse_ret[i] = Means(forward)
                deleted.append(forward_pos)
            elif item == "location_particle" and forward != None and type(forward) == Phrase:
                parse_ret[i] = Location(forward)
                deleted.append(forward_pos)
            elif item == "similarity_particle" and forward != None and type(forward) == Phrase:
                parse_ret[i] = Similar(forward)
                deleted.append(forward_pos)
            elif item == "causality_particle" and forward != None and type(forward) == Phrase:
                parse_ret[i] = Cause(forward)
                deleted.append(forward_pos)
            elif item == "modifier_particle" and forward != None and type(forward) == Phrase:
                parse_ret[i] = Modifier(forward)
                deleted.append(forward_pos)
            
            elif item == "interjection":
                parse_ret[i] = Interjection(Phrase(self.tokens[i], item))
                deleted.append(i)
            
            elif item == "vocative_particle" and type(prev) in [Phrase, Modifier, Subject, AddSubject]:
                tokens = []
                delete = []
                for k, v in list(parse_ret.items())[::-1]:
                    if type(v) not in [Phrase, Modifier, Subject, AddSubject]:
                        print(type(v))
                        break
                    elif i > index:
                        tokens.append(v)
                        delete.append(k)
                    else:
                        break
                parse_ret[i] = Vocative(tokens[::-1])
                for key in delete:
                    parse_ret.pop(key)
            
            #! Context phrases ---- NOT FINISHED ----
            
            elif item == "context_particle":
                tokens = []
                delete = []
                for k, v in list(parse_ret.items())[::-1]:
                    if type(v) == ContextPhrase:
                        break
                    elif i > index:
                        tokens.append(v)
                        delete.append(k)
                    else:
                        break
                parse_ret[i] = ContextPhrase(tokens[::-1])
                
                for key in delete:
                    parse_ret.pop(key)
            
            #! Failsafe
            
            elif type(item) == Phrase:
                parse_ret[i] = Subject(item)
            elif type(item) == Number:
                number = Phrase("nanpa", "number_token")
                number.set_number(item)
                parse_ret[i] = Subject(number)
            else:
                parse_ret[i] = item
        
        self.parse = [v for k, v in parse_ret.items()]
    
    def check_grammar(self, inp=None, context=False, voc=False):
        
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
            Modifier,
            Vocative
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
        
        
        for t, token in enumerate(inp):
            if t > 0:
                back = inp[t-1]
            else:
                back = None
            parse.append(token)
            
            if type(token) == Subject:
                #print(ignore_li, token.ignore_li)
                if "ignore_li" in word_tags[token.head[0]] and "li" in self.tokens:
                    fails.append("LI_NOT_IGNORED")
                if subject_passed:
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
                if voc:
                    fails.append("FULL_PHRASE_IN_VOCATIVE")
                if token.number != None and type(token) not in [Predicate, ImpPredicate]:
                    fails.append("NUMBERED_VERB")
                if type(token) in [ImpVerb, ImpPredicate]:
                    imperative = True
                elif not subject_passed:
                    fails.append("PREDICATE_BEFORE_SUBJECT")
                predicate_verb_passed = True
            elif type(token) in [DirectObject, IndirectObject, Means, Location, Similar, Cause]:
                if voc:
                    fails.append("FULL_PHRASE_IN_VOCATIVE")
                if not predicate_verb_passed:
                    fails.append("FINAL_WITHOUT_PREDICATE")
            elif type(token) == Interjection:
                if context and not subject_passed and len(inp) == 1:
                    fails.append("LONE_INTERJECTION_AS_CONTEXT")
            elif type(token) == Modifier:
                if type(back) in [Interjection, ContextPhrase, Vocative] or back == None:
                    fails.append("HANGING_PI_PHRASE")
                if token.adjectives == [] and not token.number:
                    fails.append("SOLE_WORD_PI_PHRASE")
            elif type(token) == ContextPhrase:
                if voc:
                    fails.append("FULL_PHRASE_IN_VOCATIVE")
                phrase_parse, phrase_fails = self.check_grammar(token.tokens, context=True)
                fails += phrase_fails
            elif type(token) == Vocative:
                phrase_parse, phrase_fails = self.check_grammar(token.tokens, context=True, voc=True)
                fails += phrase_fails
        if fails != []:
            parse = []
        return parse, fails

ERROR_CODES = {
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
    "HANGING_PI_PHRASE": 2,
    "LI_NOT_IGNORED": 2,
    "FULL_PHRASE_IN_VOCATIVE": 2
}