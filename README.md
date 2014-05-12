Rabbit
======

Rabbit (PythonPlus) is a compilation of functions, classes, and variables that extend basic Python functionality.
See the \_\_doc\_\_ string in \_\_init\_\_.py for more information.

### Using Rabbit in Python

Using Rabbit in a Python program is fairly simple. Most Rabbit Python programs begin with a line that looks something like one of these (the latter is preferred but the former is more common):
```
from rabbit.all import *
import rabbit.all as rabbit
```

From there, what you want to do depends on what you're using rabbit for. If you're not sure what rabbit can do, use the \_\_doc\_\_ string in \_\_init\_\_.py to find a module that looks interesting and then look over the functions that are in it.

Some very common one-liners for initiating basic rabbit features are:
```
mathbase().start()  # Starts up the RabbitLang interpreter
editor().start()    # Starts up the RabbitLang editor
```

## RabbitLang

RabbitLang, or more commonly just Rabbit, is one of the Rabbit module's core features. RabbitLang is a functional, dynamically typed, interpreted language written in Python. RabbitLang borrows heavily from both Python and Haskel, but is very different from both languages. The tutorial below should give you a basic idea of how to write code in RabbitLang using the provided tools.

#### Core features
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

Finally, Rabbit takes whitespace insensitivity to the extreme. Whitespace is only used in line continuations, strings, and seperating arguments to interpreter commands. In every other area, all whitespace is deleted, meaning that whitespace can be used liberally in almost any situation, including the seperation of digits or parts of variable names.

For more information, read the docstrings in eval.py.

### Levels of Evaluation

Every line of RabbitLang code goes through at least four different stages in its evaluation. Each stage will use its own symbols in the debug output, and will deal with different types of commands or operations.

#### 1. Text (run)

The first stage is text processing. This is the only stage that is sometimes exempted: if working in a command-line interpreter (cmd.py, for example), this stage will be skipped, since it only has to do with evaluating multiple lines, but if working in an IDE (ride.py, for example) or running a file, the input will always go through this stage.

The only thing done at this stage is line continuations. These are done by placing any amount of whitespace at the start of a line--doing so will automatically append that line to the one that came before it. This allows all of Rabbit's different control features to be spread out accross multiple lines in an easily readable, straightforward fashion.

Text evaluation does not generate debug output.

#### 2. Interpreter (cmd)

The second stage is interpreter command resolution. This stage can vary based on the interpreter, but the commands below should always be expected to work, and will be evaluated at this stage.

This stage mostly works in command-line syntax (spaces as argument seperators), but certain symbol operators are also evaluated at this stage. The most common and important commands and operators evaluated are:
```
f(x) # a comment  # The # operator will tell the interpreter to ignore everything after it
x = 1             # Sets the variable x to the yet-to-be-evaluated value 1
x := x            # Sets the variable x to the result of evaluating x
f(x) = x          # The preferable notation for creating functions
a = 1 ;; b = 2    # The ;; operator is used to seperate top-level commands
del x             # Deletes the variable x
debug             # Toggles debug mode
get               # Shows all set variables
```

##### Debug Output
```
: ON            # Shows that debug output has been turned on
: a = 1         # Sets a to 1
: f = \x\x      # Sets f to \x\x (same thing as setting f(x) to x)
< g >           # Deletes g
```

#### 3. Command (calc)

The third stage is top-level operator evaluation. This stage, and all following stages, don't (usually) vary based on the interpreter, since the functions that carry them out are located in the evaluator class (eval.evaluator) instead of in the interpreter class (cmd.mathbase).

All different types of paretheses as well as conditionals are evaluated at this stage. In order, the different operators evaluated are:
```
"hello, world"  # Strings (after this step whitespace is eliminated)
{ x = 1 }       # Classes
[1, 2, 3]       # Matrix rows
(x+2)*2         # Parentheses
f(x); g(x)      # Conditionals
f(x) @ x>=0     # Conditions
```

##### Debug Output
```
>>> x+1 <--------   # The arrows after the command indicate that it's top-level
>>> f(x) | source   # Begins evaluating a command (source denotes who ordered the evaluation)
| f`0`              # Shows the result of parentheses evaluation (everything inside a paren becomes `number`)
2 <<< x+1           # Shown the result when a command has finished evaluating
```

#### 4. Equation (bool)

The fourth stage is boolean operator evaluation. The output of this stage will depend on whether it is being fed to an at clause. If it is, non-booleans will be made into booleans. If it isn't, booleans will be made into integers.

All different logical, equality, and inequality operators are evaluated at this stage. The stage itself is seperated into two phases. In the first phase, the logical operators are evaluated, and in the second, the equality and inequality operators are evaluated. In order, the different operators evaluaed are:
```
x < -1 | x > 1        # Logical or
0 <= x & x < 10       # Logical and
x >= 2 | x => 2       # Greater than or equal to (both symbol orders are accepted)
x <= 5 | x =< 5       # Less than or equal to (both symbol orders are accepted)
x > 3                 # Greater than
x < 4                 # Less than
x != [ ] & x <> [ ]   # Not equal to (both symbols are accepted)
x ?= 1 & x = 1        # Equal to (the question mark is optional)
```

In order, the 

##### Debug Output
```
=>> >;1+1;2       # Begins evaluating an equation (turns it into prefix notation and seperates with semicolons)
0 <<= >;1+1;2     # Shows the result when an equation has finished evaluating
```

#### 5. Expression (eval)

The fifth stage is high-level operator evaluation.

High-precedence mathematical and functional operators are evaluated at this stage. In order, the different operators evaluated are:
```
x~x^2~1,2,3   # List looping
1,2 .. 3,4    # Concatenation
1,2,3,4       # Lists
1+2-3         # Addition and subtraction
6 % 3         # Modulo
3*4/5         # Multiplication and division
```

##### Debug Output
```
=> 1+1      # Begins evaluating an expression
2 <= 1+1    # Shows the result when an expression has finished evaluating
```

#### 6. Term (call)

The sixth stage is low-level operator evaluation. Unlike stages 3-5, but like stage 2, instead of each expression going through every operator function, only the first term operator function to be able to handle the expression will be used. Often, however, it will then loop back up and perform another term evaluation.

There is a standard order for term operator function evaluation, but in rare cases the interpreter may change the order of or add in additional term operator functions. All interpreters in this module are consistent with the standard order. In standard order, the different term functions and their operators are:
```
x | var         # Evaluates variables
  | none        # Evaluates empty strings
- | neg         # Performs negation
/ | reciproc    # Performs division
^ | exp         # Performs exponentiation
\ | lambda      # Creates in-line functions
! | fact        # Performs factorial
: | colon       # Performs function calls
` | paren       # Evaluates all forms of parentheses
. | method      # Evaluates methods and functions of functions
1 | normal      # Evaluates numbers
```

##### Debug Output
```
-> 1              # Begins evaluating a term
1 <- 1 | source   # Shows the result when a term has finished evaluating (source denotes who did the evaluation)
```
### Sample Programs

#### Hello World
```
print("Hello, world!")    # The convential method, print is a built-in function just for this purpose
show "Hello, world!"      # A common interpreter command, show will print its argument in a text box
```

#### Boolean Functions
```
bool(x) = \true @ x; \false
not(x) = \false @ x; \true
and(x,y) = \true @ x&y; \false
nand(x,y) = \false @ x&y; \true
or(x,y) = \true @ x|y; \false
nor(x,y) = \false @ x|y; \true
xor(x,y) = \true @ bool:x != bool:y; \false
xnor(x,y) = \false @ bool:x != bool:y; \true
```

#### Basic Math
```
f'(x) = (D:\f):x
sec(x) = 1/cos:x
csc(x) = 1/sin:x
cot(x) = 1/tan:x
asec(x) = acos:(1/x)
acsc(x) = asin:(1/x)
acot(x) = atan:(1/x)
cis(x) = cos(x)+i*sin(x)
```
