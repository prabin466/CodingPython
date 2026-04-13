def evaluate_file(input_path:str) ->list[dict]:  # Evaluates the expressions in the input file and returns a list of results
    results = []    # List to store the results of each expression
    with open(input_path, 'r') as file:  # Open the input file for reading
        for line in file:  # Iterate through each line in the file
            line = line.strip()  # Remove leading and trailing whitespace
            if not line:  # Skip empty lines
                continue
            
            tokens = tokenize(line)  # Tokenize the line into a list of tokens
            if '[ERROR]' in tokens:  # Check if tokenization resulted in an error
                results.append({"input": line, "tree": "ERROR", "tokens": ["ERROR"], "result": "ERROR"})
                continue
            
            parsed_expr = parse(tokens)  # Parse the list of tokens to create an expression tree
            if parsed_expr == "ERROR":  # Check if parsing resulted in an error
                results.append({"input": line, "tree": "ERROR", "tokens": tokens, "result": "ERROR"})
                continue

            evaluation_result = evaluate(parsed_expr)  # Evaluate the expression tree to get the final result
            if evaluation_result == "ERROR":  # Check if evaluation resulted in an error
                results.append({"input": line, "tree": parsed_expr, "tokens": tokens, "result": "ERROR"})
            else:
                if isinstance(evaluation_result, (int,float)) : # Check if the evaluation result is a number (int or float)
                    if evaluation_result == int(evaluation_result):  # Convert the result to an integer if it's a float
                        evaluation_result = int(evaluation_result)
                    else:
                        evaluation_result = round(evaluation_result, 4)  # Round the result to 4 decimal places if it's a float
                else:
                    evaluation_result = "ERROR"  # If the result is not a number, set it to "ERROR"
                
                results.append({"input": line, "tree": parsed_expr, "tokens": tokens, "result": evaluation_result})  # Append the result to the results list

    with open('output.txt', 'w') as output_file:  # Open the output file for writing
        for result in results:  # Iterate through each result in the results list
            output_file.write(f"Input: {result['input']}\n")  # Write the input expression to the output file
            output_file.write(f"Tree: {result['tree']}\n")  # Write the expression tree to the output file
            output_file.write(f"Tokens: {' '.join(result['tokens'])}\n")  # Write the tokens to the output file
            output_file.write(f"Result: {result['result']}\n\n")  # Write the final result to the output file
    
    return results  # Return the list of results

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
        return f"(neg {result})", index
    
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


def evaluate(tree):
    # Evaluates the expression tree recursively
    
    # If it's already a number, return it
    if isinstance(tree, (int, float)):
        return tree
    
    # Convert to string and strip whitespace
    tree_str = str(tree).strip()
    
    # Base case: if it's a plain number as a string
    if tree_str.isdigit():
        return int(tree_str)
    
    # Handle unary minus
    if tree_str.startswith('neg:'):
        operand = tree_str[4:]  # Remove 'neg:' prefix
        result = evaluate(operand)
        if result == "ERROR":
            return "ERROR"
        return -result
    
    # Handle binary operations in format "(op left right)"
    parts = split_tree(tree_str)
    if not parts or len(parts) != 3:
        return "ERROR"
    
    op = parts[0]  # Get the operator
    left = parts[1]  # Get the left operand
    right = parts[2]  # Get the right operand
    
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
            return "ERROR"  # Handle division by zero
        return left_val / right_val
    else:
        return "ERROR"


evaluate_file('sample_input.txt')  # Call the evaluate_file function with the path to the input file