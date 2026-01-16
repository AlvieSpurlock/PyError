# PyError

PyError is an intelligent, console‑friendly error‑handling engine designed to capture, classify, and display Python exceptions with clean, readable, and fully contextualized output. It integrates tightly with PyConsole to produce branded, structured error messages that help developers debug faster and understand exactly what went wrong.

## Overview

PyError automatically extracts traceback information, analyzes argument mismatches, detects common error categories, and logs detailed diagnostic reports. It acts as a drop‑in enhancement to Python’s default exception system, giving developers clearer insights without modifying their existing code structure.

This makes PyError ideal for:

- CLI tools

- Debugging utilities

- Text‑based engines

- Teaching environments

- Automation scripts

- Any project where readable error output matters

Its output includes file paths, method names, line numbers, timestamps, and categorized error messages — all formatted using PyConsole’s visual language.

## Why PyError?

Python’s default exceptions are powerful but often noisy, inconsistent, or lacking context. PyError solves this by:

- Extracting the exact file, method, and line where the error occurred

- Capturing required vs. given arguments

- Detecting argument count mismatches

- Detecting incorrect argument types

- Detecting index errors, math errors, file I/O errors, import errors, and value errors

- Logging errors automatically to ErrorLog.txt

- Displaying everything in a clean, structured, console‑friendly format

Instead of manually parsing tracebacks or writing repetitive error‑handling code, PyError centralizes the entire process into a single, reusable engine.

## Core Features

### Automatic Traceback Extraction

PyError walks the traceback to identify the deepest frame, capturing:

- File path

- Line number

- Method name

- Timestamp

### Argument Metadata Binding

Using BindMetadeta, PyError can capture:

- The index of the failing item

- Required arguments

- Given arguments

This enables precise argument mismatch detection.

### Error Classification Engine

PyError automatically identifies:

- Argument errors

- Index errors

- File I/O errors

- Math errors

- Value errors

- Import errors

Each category triggers a clean, readable error message.

### Branded Console Output

All error messages use PyConsole’s formatting:

- Headers

- Breakers

- Structured sections

This keeps your debugging output visually consistent across your entire ecosystem.

### Automatic Logging

Every error is written to:

- ErrorLog.txt

Including full context and timestamps.

## Example Output

```txt
File Path of Error:
C:\Projects\MyApp\main.py
------
Method In Question: process_data
Line In Question: 42
------
Time Of Error: January 15, 2026 at 03:14 PM

[======================]
```
## Class Structure

```python
class PyError:
    active = None

    def __init__(self, exception, rI=0):
        self.exception = exception
        self.date_time = dt.now()
        self.i = None
        self.rI = rI
        self.gArgs = []
        self.rArgs = []
        self.file = None
        self.line = None
        self.method = None

        self.extract_traceback(exception)
        self.extract_argument_info(exception)
        self.assign_error_code()
```
(Full implementation included in repository.)

## Usage Example

```python
from PyError import PyError

try:
    result = my_function(10, "wrong_type")
except Exception as e:
    PyError(e)
```

### With metadata binding:

```python
def my_function(a: int, b: int):
    PyError.BindMetadeta(0, my_function, a, b)
    return a + b

try:
    my_function(10, "wrong_type")
except Exception as e:
    PyError(e)
```
## PyError will automatically detect:

- Incorrect argument types

- Required vs. given arguments

- The index of the failing call

And produce a clean, readable error message.

## Summary

PyError is a powerful, modular error‑handling engine that enhances Python’s exception system with structured output, argument analysis, traceback extraction, and automatic logging. It integrates seamlessly with PyConsole to provide a consistent debugging experience across your entire tool ecosystem.

Requires: Python 3.x, PyConsole
