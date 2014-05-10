Rabbit
======

Rabbit (PythonPlus) is a compilation of functions, classes, and variables that extend basic Python functionality.
See the \_\_doc\_\_ string in \_\_init\_\_.py for more information. Keep reading below for a tutorial of how to use the rabbit language.

## RabbitLang

RabbitLang, or more commonly just Rabbit, is one of the Rabbit module's core features. RabbitLang is a functional, dynamically typed, interpreted language written in Python. RabbitLang borrows heavily from both Python and Haskel, but is very different from both languages. The tutorial below should give you a basic idea of how to write code in RabbitLang using the provided tools.

Core features:
* Dynamic typing
* Dynamic scoping
* Object-oriented
* Functional
* Not whitespace sensitive
* Good for complex math
* Extendable with Python

### Language Basics

The largest difference between Rabbit and any other programming language is that each line of code is isolated. If I define a function in Python, for example, I will usually then enter multiple lines of code that define what that function does. Each line of code inside the function is not isolated: it's part of the function. In Rabbit, you cannot use multiple lines (not to be interpreted as actual single lines--almost all lines of code in rabbit will use continuations) to define the function--instead, you use RabbitLang's different integrated control features to define all the logic in the function in one fell swoop.

Beyond that, Rabbit uses very few special words in favor of mostly using special symbols. This serves to limit the core language features to the keyboard symbols, making it very clear what is a core language feature and what is not.

Finally, Rabbit takes whitespace insensitivity to the extreme. Whitespace is only used in seperating arguments to interpreter commands and line continuations. In every other areas, all whitespace is deleted, meaning that whitespace can be used liberally in almost any situation, including the seperation of digits or parts of variable names.
