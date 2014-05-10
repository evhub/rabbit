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

Finally, Rabbit takes whitespace insensitivity to the extreme. Whitespace is only used in line continuations, strings, and seperating arguments to interpreter commands. In every other area, all whitespace is deleted, meaning that whitespace can be used liberally in almost any situation, including the seperation of digits or parts of variable names.

### Levels of Evaluation

Every line of Rabbit code goes through at least four different stages in its evaluation. Each stage will use its own symbols in the debug output, and will deal with different types of commands or operations.

#### 1. Text (run)

The first stage is text evaluation. This is the only stage that is sometimes exempted: if working in a command-line interpreter (cmd.py, for example), this stage will be skipped, since it only has to do with evaluating multiple lines, but if working in an IDE (ride.py, for example) or running a file, the input will always go through this stage.

The only thing done at this stage is line continuations. These are done by placing any amount of whitespace at the start of a line--doing so will automatically append that line to the one that came before it. This allows all of Rabbit's different control features to be spread out accross multiple lines in an easily readable, straightforward fashion.

Text evaluation does not generate debug output.

#### 2. Interpreter (cmd)

The second stage is interpreter command resolution. This stage can vary based on the interpreter, but the commands below should always be expected to work, and will be evaluated at this stage.

This stage mostly works in command-line syntax (spaces as argument seperators), but certain symbol operators (=, :=, ~~) are also evaluated at this step. The most important of these commands are:
```
x = 1             # This will set the variable x to the yet-to-be-evaluated value 1
x := x            # This will set the variable x to the result of evaluating x
f(x) = x          # This is the preferable notation for creating functions
a = 1 ~~ b = 2    # The ~~ operator is used to seperate top-level commands
del x             # This will delete the variable x
debug             # This will start debug mode
```

##### Debug Output
```
: ON            # Shows that debug output has been turned on
: a = 1         # Sets a to 1
: f = \x\x      # Sets f to \x\x (same thing as setting f(x) to x)
< g >           # Deletes g
```

#### 3. Command (calc)

##### Debug Output
```
>>> x+1 <--------   # The arrows after the command indicate that it's top-level
>>> f(x) | source   # Begins evaluating a command (source denotes who ordered the evaluation)
| f`0`              # Shows the result of parentheses evaluation (everything inside a paren becomes `number`)
2 <<< x+1           # Shown the result when a command has finished evaluating
```

#### 4. Equation (bool)

##### Debug Output
```
=>> >;1+1;2       # Begins evaluating an equation (turns it into prefix notation and seperates with semicolons)
0 <<= >;1+1;2     # Shows the result when an equation has finished evaluating
```

#### 5. Expression (eval)

##### Debug Output
```
=> 1+1      # Begins evaluating an expression
2 <= 1+1    # Shows the result when an expression has finished evaluating
```

#### 6. Term (call)

##### Debug Output
```
-> 1              # Begins evaluating a term
1 <- 1 | source   # Shows the result when a term has finished evaluating (source denotes who did the evaluation)
```
