def tokenize(line: str) -> list[str]:
    # Tokenizes a line of text into a list of tokens
    tokens = []
    current_number = ''

    for char in line:
        # Accumulate digits into current_number
        if char.isdigit():
            current_number += char
        else:
            # Flush current_number if it exists and is not empty
            if current_number:
                tokens.append(f'[NUM:{current_number}]')
                current_number = ''
            
            # Tokenize special characters and operators
            if char == '(':
                tokens.append('[LPAREN]')
            elif char == ')':
                tokens.append('[RPAREN]')
            elif char in '+-/*':
                tokens.append(f'[OP:{char}]')
            elif char == ' ':
                # Skip whitespace
                pass
            else:
                # Invalid character encountered - return ERROR
                return ['[ERROR]']
    
    # Flush any remaining number at the end of line
    if current_number:
        tokens.append(f'[NUM:{current_number}]')
    
    # Add end-of-line marker
    tokens.append('[END]')
    return tokens


# Parses the list of tokens and evaluates the expression
def parse(tokens: list[str]):
    result,index = expression(tokens,0)  # Start parsing from the first token

    if index != len(tokens) - 1:  # Check if we have consumed all tokens except the end marker
        return "ERROR"  # If not, there are extra tokens that were not parsed
    return result  # Return the final result of the expression


def expression(tokens: list[str], index: int):  # Handles addition and subtraction
    left, index = term(tokens, index)  # Parse the first term

    # Checks for addition or subtraction operators
    while index < len(tokens) and tokens[index] in ('[OP:+]', '[OP:-]'):
        op = tokens[index]  # Get the operator
        index += 1  # Consume the operator
        right, index = term(tokens, index)  # Parse the next term
        
        if op == '[OP:+]':
            left = f"(+ {left} {right})"  # Create an addition node
        else:
            left = f"(- {left} {right})"  # Create a subtraction node
    return left, index


def term(tokens: list[str], index: int):  # Handles multiplication and division
    left, index = factor(tokens, index)  # Parse the first factor

    # Checks for multiplication or division operators
    while index < len(tokens) and tokens[index] in ('[OP:*]', '[OP:/]'):
        op = tokens[index]  # Get the operator
        index += 1  # Consume the operator
        right, index = factor(tokens, index)  # Parse the next factor
        
        if op == '[OP:*]':
            left = f"(* {left} {right})"  # Create a multiplication node
        else:
            left = f"(/ {left} {right})"  # Create a division node
    return left, index


# Parses a factor, which can be a number, a parenthesized expression or unary operator
def factor(tokens: list[str], index: int):
    if tokens[index].startswith('[NUM:'):
        # Extract the number from the token
        number = int(tokens[index][5:-1])  # Remove '[NUM:' and ']'
        index += 1
        return number, index

    elif tokens[index] == '[LPAREN]':
        index += 1  # Consume  '('
        result, index = expression(tokens, index)  # Parse the expression inside parentheses

        if index >= len(tokens) or tokens[index] != '[RPAREN]':
            return "ERROR", index  # Missing closing parenthesis

        index += 1  # Consume ')'
        return result, index

    elif tokens[index] == '[OP:-]':  # Unary minus
        index += 1  # Consume '-'
        result, index = factor(tokens, index)  # Parse the factor after unary minus
        return f"neg:{result}", index
    
    else:
        return "ERROR", index  # Invalid token for a factor






def split_tree(expr: str):
    # Splits a expression into its components
    if expr.startswith('neg:'):
        return ['neg', expr[4:]]  # Handle unary minus case

    if expr.startswith('(') and expr.endswith(')'):
        # Remove the outer parentheses
        inner = expr[1:-1].strip()
        parts = []
        current_part = ''
        depth = 0

        # Split the inner expression into parts based on spaces, but only at the top level (not inside nested parentheses)
        for char in inner:
            if char == ' ' and depth == 0:
                if current_part:
                    parts.append(current_part)
                    current_part = ''
            else:
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                current_part += char
        
        if current_part:
            parts.append(current_part)
        
        return parts



