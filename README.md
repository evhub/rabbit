Rabbit
======

Rabbit is a modern, functional programming language built on top of Python.

![Travis CI Build Status](https://travis-ci.org/evhub/rabbit.svg?branch=master)

## The Code

This repository hosts all the code for the Rabbit interpreter. Simple wrapper Python files for booting up common features are provided in the main repository. These are:

* `runcli.py`: Boots up the Rabbit interpreter Command Line Interface.
* `runcmd.py`: Boots up the Rabbit interpreter GUI Command Line.
* `runcomp.py`: Boots up the Rabbit interpeter data serializer and program executer.
* `rungraph.py`: Boots up the Rabbit interpreter function grapher.
* `runride.py`: Boots up the Rabbit interpreter Integrated Development Environment.
* `runtests.py`: Runs the tests for the Rabbit interpreter.
* `runall.py`: Imports all the Rabbit interpreter libraries for use in Python.

The actual code for the interpreter can be found inside the [rabbit](/rabbit) folder. Inside that, the [rabbit](/rabbit)/[carrot](/rabbit/carrot) folder holds the carrot library, a library for the more general features that the Rabbit interpreter makes use of.

## Executive Summary

For a short explanation of what Rabbit is and what it can do in layman's terms, see the Executive Summary, which can be accessed at [docs](/docs)/[Executive Summary.pdf](/docs/Executive%20Summary.pdf).

## Academic Paper

The full academic research report written on the Rabbit programming language is hosted here, and can be accessed at [docs](/docs)/[The Rabbit Language.pdf](/docs/The%20Rabbit%20Language.pdf).

## Technical Whitepaper

It is recommended that anyone who wishes to become familiar with the Rabbit programming language read the full Technical Whitepaper. The full Rabbit Technical Whitepaper can be accessed at [docs](/docs)/[Technical Whitepaper.md](/docs/Technical%20Whitepaper.md).

## Code Examples

The example code file in the documentation provides comparisons between Rabbit code and code in other languages used to solve the same problem, allowing one to see the differences between the way things are done in Rabbit and the way things are done in other languages. That file can be accessed at [docs](/docs)/[Code Examples.md](/docs/Code%20Examples.md).

Example Rabbit code can be found in many other places as well. The tests for the programming language itself function as good code examples, since, because of their nature as tests of all the features in Rabbit, they cover all the features in Rabbit. They can be accessed at [Tests.rab](/Tests.rab).
