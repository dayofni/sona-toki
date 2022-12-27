# sona-toki
**A suite of rule-based tools designed to assist in parsing and understanding toki pona text, written in Python.**

#### Q&A
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

#### tok_lexer.py
The toki pona lexer used in this project. Consisting of about one function of 20 lines of actual code, it works ever so slighly differently to the `str.split()` method given to us by Vanilla Python (TM). 
> ##### tok_parser.lexer(input_str)
>Takes an input string and returns a series of tokens, grouped by sentence.
>**Example usage:**
>```py
> sentences = lexer("o awen! o awen!")
> for i in sentences:
>    print(i) # -> [["o", "awen"], ["o", "awen"]]```

<TODO: more documentation>
