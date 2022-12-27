# sona-toki
**A suite of rule-based tools designed to assist in parsing and understanding toki pona text, written in Python.**

### Q&A
1. **How many people are working on this?**
Just one at the moment.

2. **Why are you making this?**
Because I can. And hey, I thought it might be fun.

3. **Why use rule-based techinques over ML?**
First, rule-based programs are easier to write. Second, they tend to be quite a bit faster. And third, I cannot for the life of me figure out how ML works.

4. **Use something other than Python, ewww**
Look, I really *did not* want to deal with memory errors and such while making this, performance be damned. If you want to fork this and use a different language, go ahead!

5. **Can I use this in my own project?**
(Read the license :3) Go right ahead, just provide appropriate credit in accordance with said license.

6. **How fast is it?**
*Probably not very fast at all.* I tried my best to make it go quick, but large texts will probably take a while to be parsed.

7. **What techniques did you use?**
I used the power of thinking outside a box because I really cannot understand the box. Proceed at your own risk.

8. **Did you know that there are no apostrophes in this entire README file?**
Yes, yes I did. :3

### tok_lexer.py
The toki pona lexer used in this project. Consisting of about one function of 20 lines of actual code, it works ever so slighly differently to the `str.split()` method given to us by Vanilla Python (TM). 
> ##### function tok_parser.lexer(input_str)
>Takes an input string and returns a series of tokens, grouped by sentence.
>**Example usage:**
>```python
> sentences = lexer("o awen! o awen!")
> for i in sentences:
>    print(i) # -> [["o", "awen"], ["o", "awen"]]
> ```

### tok_parser.py
The heart of like 90% of this project; this is the parser behind all of these tools and features. Also happens to be my favourite child. It takes in all of the tokens given to us from `tok_lexer.py` and spits out... multiple groups of tokens that ever so happen to conform to toki pona grammar, I guess?
> ##### function translate_variable_base(n, bases)
> Converts a number `n` from base-10 to a base defined by `bases`.
> **Example usage:**
> ``` python
> n = 11
> bases = [2, 3, 1, 3, 2]
> print(translate_variable_base(n, bases)) # -> [1, 2, 0, 1, 0]
> ```

> ##### function product(seq)
> Finds the product of a given iterable.
> **Example usage**
> ```python
> seq = [1, 2, 3, 4, 5, 6]
> print(product(seq)) # -> 720
> ```

> ##### function find_permutations(syl_pos)
> Finds all possible permutations of a given input.
> **Example usage:**
> ```python
> paths = [
>      ("a", "b"),
>      (1),
>      ("b", "a", "c")
> ]
> print(find_permutations(paths)) # -> [("a", 1, "b"), ..., ("b", 1, "c")] (6 items)
> ```

> ##### function generate_interpretations(tokens)
> Converts a series of tokens from `tok_lexer.py` into a series of possible grammatical permutations based on what functions that particular token can play.
> **Example usage:**
> ```python
> sentence = ["toki", "a"]
> print(generate_interpretations(sentence))
> # --> [['content_token', 'content_token'], ..., ['interjection', 'interjection']]
> ```

> ##### class Parser(tokens, tags)
> Generates a `Parser()` object. Takes in `tokens` (the words in the sentence) and `tags` (the parts of speech generated from `generate_interpretations()`)
> **Example usage:** see `example.py`

### word_classes.py
Wow, a sudden change from the naming convention, classy! This holds all of the different complex token classes mentioned in `tok_parser.py`. This is going to take forever to list...
### tok_translator.py
### tok_misc.py
### tok_spellcheck.py
### all.py
### base.py
