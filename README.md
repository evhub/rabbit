Rabbit
======

Rabbit is a modern, functional programming language built on top of Python.

![Travis CI Build Status](https://travis-ci.org/evhub/rabbit.svg?branch=master)

## Technical Whitepaper

For the purpose of demonstrations, this paper will assume a bash command line in a Unix environment where there is an existing installation of Python 2.7.8. To do the demonstrations, the command line interface provided by the Rabbit interpreter will be used, shadowed by a bash function named rabbit, defined as such:
```
rabbit() {
python ~/Checkout/rabbit/runcli.py
}
```
