Rabbit
======

Rabbit is a modern, functional programming language built on top of Python.

![Travis CI Build Status](https://travis-ci.org/evhub/rabbit.svg?branch=master)

## Code Examples

### Quicksort

Haskell:

```
quicksort :: (Ord a) => [a] -> [a]  
quicksort [] = []  
quicksort (x:xs) =   
    let smallerSorted = quicksort [a | a <- xs, a <= x]  
        biggerSorted = quicksort [a | a <- xs, a > x]  
    in  smallerSorted ++ [x] ++ biggerSorted  
```
Source: [Learn You A Haskell For Great Good!](http://learnyouahaskell.com/recursion#quick-sort)

Rabbit:
```
qsort(l) = (
    qsort: (as ~ \x\(x @ x<=a)) ++ a ++ qsort: (as ~ \x\(x @ x>a))
    $ a,as = l
    ) @ len:l
```

## Technical Whitepaper

The full Rabbit Technical Whitepaper can be accessed at [docs](/docs)/[Technical Whitepaper.md](/docs/Technical%20Whitepaper.md)
