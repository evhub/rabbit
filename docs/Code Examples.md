Code Examples
=============

### Quicksort

#### Python:
```
def quickSort(arr):
    less = []
    pivotList = []
    more = []
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        for i in arr:
            if i < pivot:
                less.append(i)
            elif i > pivot:
                more.append(i)
            else:
                pivotList.append(i)
        less = quickSort(less)
        more = quickSort(more)
        return less + pivotList + more
```
Source: [Rosetta Code](http://rosettacode.org/wiki/Sorting_algorithms/Quicksort#Python)

#### Haskell:
```
quicksort :: (Ord a) => [a] -> [a]
quicksort [] = []
quicksort (x:xs) =
    let smallerSorted = quicksort [a | a <- xs, a <= x]
        biggerSorted = quicksort [a | a <- xs, a > x]
    in  smallerSorted ++ [x] ++ biggerSorted
```
Source: [Learn You A Haskell For Great Good!](http://learnyouahaskell.com/recursion#quick-sort)

#### Rabbit:

Uncommented:
```
qsort(l) = (
    qsort: (as ~ \x\(x @ x<=a)) ++ a ++ qsort: (as ~ \x\(x @ x>a))
    $ a,as = l
    ) @ len:l
```

Commented:
```
# The quick sort function:

qsort(l) = # qsort is defined as a function of one argument, l
    (

        qsort: # The qsort function is called recursively on all the
               #  elements in the list less than or equal to the pivot.
            (as ~ # The tilde operator loops over the list with a function
                 \x\( # An in-line function definition using backslashes
                     x @ x<=a # The main body of the function
                     ))

        ++ a ++ # That sort is joined with the pivot, which is then joined
                #  with the next sort.

        qsort: # The qsort function is called recursively on all the
               #  elements in the list greater than the pivot.
            (as ~ # The tilde operator loops over the list with a function
                 \x\( # An in-line function definition using backslashes
                     x @ x>a # The main body of the function
                     ))

        $ a,as = l # The original argument, l, is split up into two parts,
                   #  its head, a, which will be used as the pivot, and its
                   #  tail, as, which will be the list that is split up
                   #  into two parts and each part sorted.
        )

    @ len:l # The whole body of the function is only performed if l is not
            #  empty, otherwise null, the empty list, is returned
```
