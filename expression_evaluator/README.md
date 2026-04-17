# Expression Evaluator

A Python-based mathematical expression evaluator that parses and evaluates arithmetic expressions with proper operator precedence and support for parentheses.

## Overview

The Expression Evaluator processes mathematical expressions through a multi-stage pipeline:

1. **Tokenization** - Breaks input expressions into individual tokens (numbers, operators, parentheses)
2. **Parsing** - Constructs an abstract syntax tree (AST) respecting operator precedence
3. **Evaluation** - Traverses the AST to compute the final result
4. **Output** - Generates detailed results including tokens, parse tree, and computed value

## Usage

### Setup
Place mathematical expressions in `sample_input.txt`, one expression per line.

### Execution
```bash
python evaluator.py
```

### Output
Results are written to `output.txt` with the following information for each expression:
- Input expression
- Parse tree representation
- Tokenized components
- Computed result

## Examples

**Input:**
```
2 + 3 * 4
(5 - 2) * (8 / 4)
10 / 3
```

**Output (sample):**
```
Input: 2 + 3 * 4
Tree: [expression tree]
Tokens: 2 + 3 * 4
Result: 14

Input: (5 - 2) * (8 / 4)
Tree: [expression tree]
Tokens: ( 5 - 2 ) * ( 8 / 4 )
Result: 6

Input: 10 / 3
Tree: [expression tree]
Tokens: 10 / 3
Result: 3.3333
```

## Features

- Respects standard order of operations (PEMDAS)
- Supports parenthetical grouping
- Handles floating-point arithmetic with 4-decimal-place precision
- Comprehensive error reporting
- Detailed output with parse trees and tokenization information

## Error Handling

Invalid expressions are identified during tokenization or parsing stages and marked as `ERROR` in the output without halting execution.

## Files

- `evaluator.py` - Main implementation
- `sample_input.txt` - Input expressions
- `output.txt` - Evaluation results
- `README.md` - Documentation
