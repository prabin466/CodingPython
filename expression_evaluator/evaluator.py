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
                return "ERROR"
    
    # Flush any remaining number at the end of line
    if current_number:
        tokens.append(f'[NUM:{current_number}]')
    
    # Add end-of-line marker
    tokens.append('[END]')
    return tokens



    
# Parses the list of tokens and evaluates the expression
def parse(tokens: list[str]):

    index = 0 
    factor(tokens,index) 



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
        return result, index

        if tokens[index] != '[RPAREN]':
            return "ERROR", index  # Missing closing parenthesis

        index += 1  # Consume ')'
        return result, index


    elif tokens[index] == '[OP:-]':  # Unary minus
        index += 1  # Consume '-'
        result, index = factor(tokens, index)  # Parse the factor after unary minus
        return f"neg:{result}", index
    
    else:
        return "ERROR", index  # Invalid token for a factor



def expression(tokens: list[str], index: int):  # Handles addition and subtraction
    


def term(tokens: list[str], index: int):  # Handles multiplication and division
    left, index = factor(tokens, index)  # Parse the first factor

    # Checks for multiplication or division operators
    while index < len(tokens) and tokens[index] in ('[OP:*]', '[OP:/]'):
        op = tokens[index]  # Get the operator
        index += 1  # Consume the operator
        right, index = factor(tokens, index)  # Parse the next factor

        

