def evaluate_file(input_path:str) ->list[dict]:
    """
    Reads mathematical expressions from a file, evaluates each one,
    writes the results to an output file and results a list of results dicts.
    Each dict contains the original input, the parsed tree, the tokens, and the evaluation result."""
    results = []    
    with open(input_path, 'r') as file:  
        for line in file: 
            line = line.strip()  
            if not line:  
                continue
            
            tokens = tokenize(line) 
            if '[ERROR]' in tokens:
                # If tokenization fails, we record the error and skip to the next line  
                results.append({"input": line, "tree": "ERROR", "tokens": ["ERROR"], "result": "ERROR"})
                continue
            
            parsed_expr = parse(tokens)  
            if parsed_expr == "ERROR":  
                results.append({"input": line, "tree": "ERROR", "tokens": tokens, "result": "ERROR"})
                continue

            evaluation_result = evaluate(parsed_expr)  
            if evaluation_result == "ERROR":  
                results.append({"input": line, "tree": parsed_expr, "tokens": tokens, "result": "ERROR"})
            else:
                # Normalize the result: if it's a float that is actually an integer, convert it to int; otherwise round to 4 decimal places
                if isinstance(evaluation_result, (int,float)) : 
                    if evaluation_result == int(evaluation_result):  
                        evaluation_result = int(evaluation_result)
                    else:
                        evaluation_result = round(evaluation_result, 4)  
                results.append({"input": line, "tree": parsed_expr, "tokens": tokens, "result": evaluation_result})  

    with open('output.txt', 'w') as output_file: 
        for result in results:  
            output_file.write(f"Input: {result['input']}\n")  
            output_file.write(f"Tree: {result['tree']}\n")  
            output_file.write(f"Tokens: {' '.join(result['tokens'])}\n")  
            output_file.write(f"Result: {result['result']}\n\n")  
    
    return results


def tokenize(line: str) -> list[str]:
    """Converts a string expression into a list of tokens.
    Tokens include numbers, operators, parentheses, and an end token.
    
    Token types:
    - [NUM:<number>]: A number token
    - [OP:<operator>]: An operator token
    - [LPAREN]: A left parenthesis token
    - [RPAREN]: A right parenthesis token
    - [END]: An end token
    """
   
    tokens = []
    current_number = ''

    for char in line:
        # Allow digits and a single decimal point 
        if char.isdigit() or (char == '.' and '.' not in current_number):     
            current_number += char
        else:
            if current_number:
                tokens.append(f'[NUM:{current_number}]')
                current_number = ''
            
            if char == '(':
                tokens.append('[LPAREN]')
            elif char == ')':
                tokens.append('[RPAREN]')
            elif char in '+-/*':
                tokens.append(f'[OP:{char}]')
            elif char == ' ':
                pass
            else:
                return ['[ERROR]']
    

    if current_number:
        tokens.append(f'[NUM:{current_number}]')

    tokens.append('[END]')
    return tokens



def parse(tokens: list[str]):
    """
    Parses a list of tokens into an expression tree. Returns the tree or "ERROR" if parsing fails.
    """
    result,index = expression(tokens,0) 

    if index != len(tokens) - 1: 
        return "ERROR"  
    return result


def expression(tokens: list[str], index: int):
    """
    Parses addition and subtraction operations, respecting operator precedence.
    Delegates higher-precedence operations to the `term` function.
    """
    left, index = term(tokens, index) 

    while index < len(tokens) and tokens[index] in ('[OP:+]', '[OP:-]'):
        op = tokens[index]  
        index += 1  
        right, index = term(tokens, index)  
        
        if op == '[OP:+]':
            left = f"(+ {left} {right})" 
        elif op == '[OP:-]':
            left = f"(- {left} {right})"  
    return left, index


def term(tokens: list[str], index: int):
    """
    Parses multiplication and division operations, respecting operator precedence.
    Returns the parsed expression and the next index to process.
    """
    left, index = factor(tokens, index)  

    while index < len(tokens) and tokens[index] in ('[OP:*]', '[OP:/]'):
        if tokens[index] in ('[OP:*]', '[OP:/]'):
            op = tokens[index]  
            index += 1  
            right, index = factor(tokens, index)  
            
            if op == '[OP:*]':
                left = f"(* {left} {right})"  
            elif op == '[OP:/]':
                left = f"(/ {left} {right})"
        else:
            #Implicit multiplication e.g. 2(3+4) or (1+2)(3+4)
            right, index = factor(tokens, index)
            left = f"(* {left} {right})"
    return left, index



def factor(tokens: list[str], index: int):
    """
    Parses a factor, which can be a number, a parenthesized expression, or a unary minus.
    Returns the parsed factor and the next index to process.
    """
    # Guard against index out of bounds
    if index >= len(tokens):
        return "ERROR", index 
        
    if tokens[index].startswith('[NUM:'):
        # Extract the integer value from the token
        raw = tokens[index][5:-1]
        if '.' in raw:
            number = float(raw)
        else:
            number = int(raw)
        index += 1
        return number, index

    elif tokens[index] == '[LPAREN]':
        index += 1 # Move past the left parenthesis
        result, index = expression(tokens, index) 

        if index >= len(tokens) or tokens[index] != '[RPAREN]':
            return "ERROR", index  # Missing closing parenthesis

        index += 1   # Move past the right parenthesis
        return result, index

    elif tokens[index] == '[OP:-]': 
        # Handle unary minus
        index += 1  
        result, index = factor(tokens, index) 
        return f"(neg {result})", index
    
    else:
        return "ERROR", index  # unexpected token






def split_tree(expr: str):
    """
    Splits a parenthesized expression into its components.
    For example, "(+ 1 2)" would be split into ["+", "1", "2"].
    """

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


def evaluate(tree):
    """
    Recursively evaluates an expression tree. The tree can be a number, a unary operation, 
    or a binary operation. Returns the evaluated result or "ERROR" if evaluation fails (e.g., division by zero).
    """
    if isinstance(tree, (int, float)):
        return tree
    
    tree_str = str(tree).strip()

    # Handle bare number strings returned by split_tree
    try:
        return int(tree_str)
    except ValueError:
        try:
            return float(tree_str)
        except ValueError:
            pass
    
    parts = split_tree(tree_str)

    if not parts:
        return "ERROR"
    
    if parts[0] == 'neg':
        # Handle unary minus
        val = evaluate(parts[1])
        if val == "ERROR":
            return "ERROR"
        return -val
    
    if len(parts) != 3:
        return "ERROR"
    
    op, left, right = parts[0], parts[1], parts[2]
    
    left_val = evaluate(left)
    right_val = evaluate(right)
    
    if left_val == "ERROR" or right_val == "ERROR":
        return "ERROR"

    if op == '+':
        return left_val + right_val
    elif op == '-':
        return left_val - right_val
    elif op == '*':
        return left_val * right_val
    elif op == '/':
        if right_val == 0:
            return "ERROR"  # Division by zero error
        return left_val / right_val
    else:
        return "ERROR" # Unknown operator error


evaluate_file('sample_input.txt')  