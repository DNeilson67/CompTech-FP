
# Digits
DIGITS = '0123456789'
# Error Handling
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
        
    def as_string(self):
        result = f'{self.error_name}:{self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result 

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)
        
# Position
 
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx # index
        self.ln = ln #line
        self.col = col #column
        self.fn = fn #file name
        self.ftxt = ftxt #file txt
    
    def advance(self, current_char):
        self.idx += 1
        self.col += 1
        
        if current_char == '\n':
            self.ln +=1
            self.col = 0
        
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
        
        
# Define constant for the token type
TT_INT = 'TT_INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

# Creating the Token
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
        
    def __repr__(self): # Representation of the token
        # Printing the type and the value of the token
        if self.value:
            return f'{self.type}:{self.value}'
        # If it doesn't have any value, then it prints the type only.
        return f'{self.type}'
    
# Creating the Lexer

class Lexer:
    def __init__(self, fn, text):
        self.text = text
        self.fn = fn
        self.pos = Position(-1, 0, 1, fn, text)
        self.current_char = None
        self.advance()
        
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        
    def make_number(self):
        num_str = ''
        dot_count = 0
        
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))    
            
        
    def make_tokens(self):
        tokens = []
        
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                # Return error
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'"+char+"'")
        
        return tokens, None

# Driver

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    
    return tokens, error