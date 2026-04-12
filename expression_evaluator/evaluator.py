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


def evaluate(tree: str):
    # Evaluates the expression tree recursively
    tree = tree.strip()
    if tree.isdigit():
        return int(tree)  # Base case: if it's a number, return its integer value
    
    parts = split_tree(tree)  # Split the tree into its components
    if not parts or len(parts) != 3:
        return "ERROR"  # If there are no parts or not exactly 3 parts, it's an error
    if parts[0] == 'neg':
        return -evaluate(parts[1])  # Handle unary minus

    op = parts[0]  # Get the operator
    left = parts[1]  # Get the left operand
    right = parts[2]  # Get the right operand

    if op == '+':
        return evaluate(left) + evaluate(right)  # Evaluate addition
    elif op == '-':
        return evaluate(left) - evaluate(right)  # Evaluate subtraction
    elif op == '*':
        return evaluate(left) * evaluate(right)  # Evaluate multiplication
    elif op == '/':
        right_value = evaluate(right)
        if right_value == 0:
            return "ERROR"  # Handle division by zero
        return evaluate(left) // right_value  # Evaluate division using integer division
    else:
        return "ERROR"  # Invalid operator


