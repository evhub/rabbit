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

From there, what you want to do depends on what you're using Rabbit for. If you're not sure what Rabbit can do, use the \_\_doc\_\_ string in \_\_init\_\_.py to find a module that looks interesting and then look over the functions that are in it.

Some very common one-liners for initiating basic rabbit features are:
```
mathbase().start()  # Starts up the RabbitLang interpreter
editor().start()    # Starts up the RabbitLang editor
```

## RabbitLang

RabbitLang, or more commonly just Rabbit, is one of the Rabbit module's core features. RabbitLang is a functional, dynamically typed, interpreted language written in Python. RabbitLang borrows heavily from both Python and Haskel, but is very different from both languages. The tutorial below should give you a basic idea of how to write code in RabbitLang using the provided tools.

#### Core Features
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

### Basic Tutorial

This tutorial will teach you all the basic syntax of RabbitLang as well as many of the basic concepts. Two things before we begin.

First, it should be understood that each code block that is not labeled as otherwise (such as debug output) will be valid Rabbit Code. In these code blocks, it will be common to use comments. Comments in Rabbit are anything after a pound symbol (#) on a line, and will be ignored.

Second, lines that don't start with setting a variable or function are just expressions. They can be placed anywhere, and if just placed on their own, will print the result.

#### Rabbits Do Math

Math in rabbit is very similar to in any other programming language. Rabbit's mathematical operators are fairly conventional:
```
1+1		# Addition (result = 2) (evaluated left to right, highest precedence)
3-5		# Subtraction (result = -2) (evaluated left to right, highest precedence)
2*3		# Multiplication (result = 6) (evaluated left to right, medium precedence)
1/2		# Division (result = 0.5) (evaluated left to right, medium precedence)
3^2		# Exponentiation (result = 9) (evaluated right to left, low precedence)
8%3		# Modulo / Remainder (result = 2) (evaluated left to right, high precedence)
```

These different operations can, and should, be grouped using parentheses. Additionally, certain equivalent structures also exist:
```
2(x)	# Parentheses multiplication (evaluated left to right, very low precedence)
2x		# Coefficient multiplication (evaluated left to right, very low precedence, same as parentheses)
```

#### Rabbits Are Lazy

Most lines of rabbit code constitute function or variable definitions. The syntax for these is fairly straightforward:
```
a = x+1				# A variable definition
f(x,y) = 2(x+y)		# A function definition
```

You might notice that at the point when a is defined x has not yet been defined, and yet a is told that it needs to have one greater than the value of x. Not only will this construction not raise an error in Rabbit, Rabbit won't even known until you do something with a. That's because Rabbit uses lazy evaluation. By default, when you define a variable, Rabbit will simply store the string of characters you typed in and not actually do anything with it until you try to use it somewhere else. This can be very useful when wanting one variable (a) to reflect the possibly changing values of another variable (x).

It is, however, possible to circumvent lazy evaluation and force Rabbit to figure out what the value is and calculate it then and there. This can't be used with functions, however, because that wouldn't make sense: Rabbit can't calculate them yet no matter what because they haven't been supplied with arguments. The syntax for circumventing lazy evaluation is very simple:
```
a := x+1		# The colon tells the interpreter not to do lazy evaluation
```

Because one of the most common reasons to circumvent lazy evaluation is to increment or decrement a variable, or otherwise use the variable itself in giving it a new value, special syntax was added to do so:
```
# The new syntax:
a += x		# While addition is used here, most other mathematical operators will also work

# The same thing in the old syntax:
a := a+x
```

#### Rabbits Have Bools

In addition to basic mathematical operators, Rabbit also features basic conditional operators, used most commonly in conditionals. Rabbit's conditionals use two symbols each with their own, well-defined, independent function, that when put together, allow the formation of conditions. Within them, logical, inequality, and equality operators can all be used. All of these symbols have higher precedence than mathematical operators, as well as themselves having a precedence of their own.

The basic syntax for conditionals is:
```
x @ x>0			# The 'at' operator will perform the operation to the left only if the right is true (Python truth rules), otherwise returning none (right to left, high precedence)
x ; 0			# The 'else' operator will check to see whether the item to the left is none, if so, it will continue to the right, if not, stop (left to right, highest precedence)
x @ x>0; 0		# Together, these two operators allow the formation of if-else clauses
```

The different types of equality and inequality operators, in order of precedence, are:
```
1 | 0		# Or (result = 1) (left to right)
0 & 1		# And (result = 0) (left to right)
2 >= 2		# Greater than or equal to (=> also accepted) (result = 1) (left to right)
3 <= 4		# Less than or equal to (=< also accepted) (result = 1) (left to right)
3 > 5		# Greater than (result = 0) (left to right)
6 < 6		# Less than (result = 0) (left to right)
2 != 3		# Not equal to (<> or >< also accepted, but with higher precedence) (result = 1) (left to right)
5 ?= 4		# Equal to (= also accepted, but discouraged) (result = 0) (left to right)
```
These will return 1 when true and 0 when false, allowing them to properly function with the 'at' operator.

#### Rabbits Use Matrices

Rabbit uses three basic container objects, the list, the row, and the matrix. While initially these three objects appear to be very different, they're actually very similar. Rabbit actually uses mathematical matrices to store and compute all of them. In fact, each different container object is just a different way of storing data in a matrix. This means that on a base level, all three container objects behave very similarly. That doesn't mean, however, that Rabbit treats them all the same. Rabbit will detect what type of matrix each one is and adjust accordingly.

We'll start with the list, the most common and the most useful container object in Rabbit, and consequently the one with the simplest syntax:
```
(1,2,3)		# This will define a 3 by 3 matrix with 1, 2, and 3 along its main diagonal (the other locations will be ignored or treated as zero unless something is done to them)
1,2,3		# Lists are simply expressions separated by commas, the parentheses aren't necessary (left to right, high precedence)
```
Precedence for these and other container operations is between booleans and math. 

Next is the row, so named because it is nothing more than a matrix with one row and many columns. The syntax for creating rows is:
```
[1,2,3]		# This will define a 1 by 3 matrix with the items 1, 2, and 3 in it
[(1,2,3)]	# The colons are actually converting a list into a row, so the inside can actually be any list
```

Because it is more complicated and the syntax to define it includes operations you don't know yet, we'll hold off on explaining full matrices until later. For now we'll just tell you that they're just multiple rows joined together into a full matrix.

Additionally, all the different container objects support various types of operations that can be performed on them. Because they are matrices, they all support basic matrix math. The syntax for these basic operations is:
```
(1,2,3)*2			# Scalar multiplication (result = (2,3,6))
(1,2,3)+10			# Applied addition (result = (11,12,13))
(1,2)+(10,20)		# Matrix addition (result = (11,22))
(1,2)*(10,20)		# Matrix multiplication (result = (10,40))
[1,2]*[10,20]		# Dot product (result = 50)
[1,0,0]%[0,1,0]		# Cross product (result = [0,0,1])
```

Additionally, there are a couple of other, special operations that can be done only with container objects, the syntax for which is:
```
[1,2] .. [3,4]	# Concatenation (result = [1,2,3,4]) (left to right, high precedence)
[1,2,3,4]:1		# Item indexes (result = 2) (left to right, lowest precedence, same as colon for function calls)
(1,2,3):2		# These work for lists as well (result = 3)
(1,2,3):0:2		# And can also be used to perform item indices (result = 1,2)
```

#### Rabbits Love Functions

How to define functions was mentioned earlier but how to call them never was. Rabbit provides two different methods of calling functions, using colons and using parentheses. The two methods are similar in many ways but also very different. Here are a couple of examples that explain the differences:
```
# First, let's define three different functions, one that takes no arguments, we'll call it t,
t() = 1 
# One that takes one argument, we'll call it f,
f(x) = x+1
# And one that takes two arguments, we'll call it g
g(x,y) = 2*x*y

# First, we'll show two different, equivalent ways of calling the zero-variable function:
t()+1
t:+1
# result = 2

# Second, we'll show two different, equivalent ways of calling the one-variable function:
f(2,)*3		# Note the use of a comma after the first variable--we'll learn why this is important later
f:2*3
# result = 9

# Third, we'll show two different, equivalent ways of calling the two-variable function:
g(2,3)-5
g:2:3-5
# result = 7

# Now, we'll show ways in which the two syntaxes can differ. First, we'll talk about parentheses syntax.

# Parentheses syntax essentially forms a list out of what is inside the parentheses, and then calls the function with those arguments.
# That means that this:
add(x,y,z) = x+y+z
a = 1,2,3
add(a)
# Will call add with the three variables 1, 2, and 3, instead of with the one variable (1,2,3) as its argument. This can often be useful, as is shown in the example.

# Colon syntax, on the other hand, will never do that. Whatever is after the first colon is the first argument, a second argument requires a second colon.
# What colon syntax will do, however, that parentheses syntax will not, is curry multiple arguments. This is useful when dealing with functions that return other functions.
# Before we can get into that, however, you need to understand how to define in-line functions, or lambdas.
```

Lambda syntax in Rabbit is fairly straightforward, with a couple of strange quirks that result from Rabbit being dynamically scoped. Lambdas are defined using the backslash (\) operator. Here're some examples of how to define different lambda functions:
```
\1				# A zero-argument function that returns 1
\x\(x+1)		# A one-variable function (x) that returns that variable plus one (x+1)
(\x\x)+1		# The same as above--Rabbit will just curry any basic mathematical operation done to a function
\(x,y)\(x+y)	# A two-variable function that adds the two variables
\(x,x:(1))\x	# A one-variable function, whose one variable defaults to one, that returns the variable
				# This syntax is particularly useful because the defaults are evaluated in the scope where the function is defined instead of the scope where it is called, allowing arguments to be passed between scopes
f(x) = x
\f				# Since f is a previously defined function, this will just return that function
\\f				# This syntax is required to create a new zero-variable function that returns f
```

Now that we know how to define lambdas, here's what's special about colon syntax:
```
gen_func(n) = \(x,n:(n))\(x%n)	# Creates and returns a function that will take the mod of its variable with the base equal to the variable of the generator
gen_func:2:5					# Because gen_func only takes one variable, colon syntax will pass the remaining variables on to whatever is returned by gen_func
# result = 5 % 2 = 1
```

#### Rabbits Eat Strings

Strings in rabbit are also not complicated, and are really very similar to strings in any other language. Here's the basic syntax:
```
"hello, world"		# Creates a string--it should be noted that single quotes will NOT work--they are reserved for global defaults
"Answer: "+2		# Strings support addition, even with other things that are not strings (result = "Answer: 2")
"hello"*2			# Multiplication behaves like one would expect, in this case doubling the string (result = "hellohello")
"01234":2			# Strings also support indexes, just like matrices (result = "2")
"01234":1:3			# As well as indices, just like matrices (result = "12")
```

#### Rabbits Take Classes

Classes in Rabbit are essentially namespace objects. What that means is that classes are just groups of commands that are fed to them, and then any new definitions put into their own namespace. The basic syntax for classes is:
```
{ x = 1 }		# Will create a class whose only variable, x, is set to 1
			# NOTE: This will only work if x is not currently set to 1--if it is, Rabbit won't detect any change, and you'll end up with an empty class
{ x = 1 ;; y = 2 }	# Because the interior of a class is just treated as a command, command seperators can be used to define multiple items inside of a class
{ f(x) = x }		# That also means that functions can be defined within classes just the same as if they were being defined at the top level
```

Once a class has been created, a variety of different things can be done with it. The different sytnax for calling classes, and a further explanation of methods, is below:
```
a = { x := x+1 }	# Remember, any valid top-level command is valid inside of a class
a.x + 1			# This will retreive x from the class a and add 1 to it
a:"x+1"			# Same as above--this will evaluate "x+1" in the namespace of the class
```

Since class definitions can often get very long, it is reccomended that line continuations be used. Since we haven't introduced those yet, we'll do so here. Line continuations follow a very simple rule: any line that starts with whitespace will be added onto the previous line. It should be noted that this only works when running code from a file, not from the command line. Some common uses of this syntax are:
```
# Defining a piecewise function:
f(x) =
 x+1 @ x>0;
 -1/x

# Defining a class:
a = {
 f(x) = x ;;
 x = 1
 }
```

When a function is defined inside of a class this turns it into a method. Methods are the same as any old function, except that the class they are in will always be passed to them as the variable "self". Here's an example of a method:
```
a = {
 fact(x, n) =				# Since this function is being defined inside of a class it becomes a method
  x*self.fact(x-1, n-1) @ n>0;		# Here we use the self variable to allow the function to call itself
  1
 }
```

Since a very common use of classes is to define a temporary variable that is going to be used in multiple places but only in the same expression, with, or where, clauses were added to facilitate that. The syntax for these statements is:
```
# In with clause syntax:
f(x) = gx*floor(gx) $ gx = g(x)		# Calls what comes before the dollar sign in the namespace of what comes after (right to left, highest precedence, right above at)
# The same thing in class syntax:
f(x) = { gx = g(x) } : "gx*floor(gx)"

# In with clause syntax:
g(x) = m(z) $ z = x^2 $ m(z) = z%10	# Multiple dollar signs are used instead of double semicolons to seperate multiple commands
# The same thing in class syntax:
g(x) = { z = x^2 ;; m(z) = z%10 } : "m(z)"
```

#### Other Rabbits

Before we move on, there are four additional more complex, less-used operators that deserve attention.

First is the loop operator (~). The loop operator allows for the looping of functions over lists. The basic syntax is:
```
1,2,3~ \x\x			# Loops over 1,2,3 with \x\x (result = (1,2,3)) (right to left, highest precedence for a mathematical operator)
1,2,3,4~ \(x,y)\(x+y)		# Loops over 1,2,3,4, taking every two variables for each function call (result = (3,7))
2,4,6,8~ \x\(last+x)		# Like a method, a loop function will be given a special variable "last" that will be set to the last value returned by the loop function in the loop
10,20~ 1,2~ \(x,y)\(x+y)	# Loops over 1,2, within a loop over 10,20, feeding each into the function (result = ((11,12),(21,22)))
```

Second is the function of a function operator (.). While the syntax is the same as that for methods, since functions don't have methods, function of a function is used like methods for functions. The basic syntax is:
```
f(x) = x^2
g(x) = x+1
f.g(2)		# Read as f(g(x)) (result = 9)
```

Third is the factorial operator (!). Because confusion is possible between factorials and not equals, parentheses should usually be used to make it unambiguous, since not equals will always take precedence. The basic syntax is:
```
(3!)+1	# The basic factorial operator (result = 7) (right to left, very low precedence)
```

Fourth is the default variable operator ('). In most cases, the single quote is reserved for use in variable names--most commonly put at the end of the name--but if put at the very beginning, it functions as the default variable operator. The basic use is:
```
'var = 5	# Works just like a normal function definition
1+'var		# You can even still call it using its full name (result = 6)
1+var		# Same as above--this will check for var first, and if it doesn't find it, then it will go to 'var (result = 6)

var = 2
1+'var		# When the normal variable is redefined, the default isn't affected (result = 6)
1+var		# But the normal variable is, now using its new value instead of the default (result = 3)
```

#### Rabbits Come With Functions

Rabbit comes with a lot of built-in functions. We'll list all of them below, but this list might not always stay updated. An updated list should always be available in eval.py and cmd.py. The different built-in rabbit functions are:
```
# Built-In Base Rabbit Functions:
copy
type
to
str
repr
chars
calc
fold
D
S
L
I
list
matrix
cont
det
sum
prod
join
merge
sort
reverse
round
num
eval
find
split
replace
contains
range
len
size
abs
data
frac
simp
d
floor
ceil
log
ln
sqrt
tan
sin
cos
atan
asin
acos
deg
rad
normdist
binomP
hypgeoP
tdist
teq
chisqdist
chisqeq
normP
tP
chisqP
poissonP
gamma
gcd
lcm
perm
comb

# Built-In Base Rabbit Variables:
i
e
pi
none
true
false

# Built-In Rabbit Interpreter Functions:
ans
grab
print
```

#### More Rabbits?

That's currently the end of the basic Rabbit tutorial. Check back here for information on additional features as they get added, and see below for more information on how the actual processing of Rabbit code is done.

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
f(x) # a comment	# The # operator will tell the interpreter to ignore everything after it
x+1			# A plain expression will simply print the result to the console
x = 1             	# Sets the variable x to the yet-to-be-evaluated value 1
x := x            	# Sets the variable x to the result of evaluating x
f(x) = x          	# The preferable notation for creating functions
a = 1 ;; b = 2    	# The ;; operator is used to seperate top-level commands
del x             	# Deletes the variable x
debug             	# Toggles debug mode
get               	# Shows all set variables
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

All different types of parentheses as well as conditionals are evaluated at this stage. In order, the different operators evaluated are:
```
"hello, world"  # Strings (after this step whitespace is eliminated)
{ x = 1 }       # Classes
[1, 2, 3]       # Matrix rows
(x+2)*2         # Parentheses
x $ x = 1	# With clauses
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

##### Debug Output
```
=>> >;1+1;2       # Begins evaluating an equation (turns it into prefix notation and seperates with semicolons)
0 <<= >;1+1;2     # Shows the result when an equation has finished evaluating
```

#### 5. Expression (eval)

The fifth stage is high-level operator evaluation.

High-precedence mathematical and functional operators are evaluated at this stage. In order, the different operators evaluated are:
```
1,2,3~\x\x    # List looping
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
