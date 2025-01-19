from ply import lex, yacc

# Lexer
tokens = (
    'IF', 'ELSE', 'FOR', 'WHILE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'ID', 'NUMBER',
    'SEMICOLON', 'EQUALS', 'COMPARISON'
)

# Keywords
keywords = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
}

# Token rules
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_EQUALS = r'='
t_COMPARISON = r'(==|!=|<=|>=|<|>)'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored characters (spaces and tabs)
t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# Parser
def p_program(p):
    '''program : statement
               | program statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : if_statement
                | for_statement
                | while_statement
                | simple_statement'''
    p[0] = p[1]

def p_if_statement(p):
    '''if_statement : IF LPAREN condition RPAREN LBRACE program RBRACE
                   | IF LPAREN condition RPAREN LBRACE program RBRACE ELSE LBRACE program RBRACE'''
    if len(p) == 8:
        p[0] = ('if', p[3], p[6])
    else:
        p[0] = ('if-else', p[3], p[6], p[10])

def p_for_statement(p):
    '''for_statement : FOR LPAREN simple_statement condition SEMICOLON ID RPAREN LBRACE program RBRACE'''
    p[0] = ('for', p[3], p[4], p[6], p[9])

def p_while_statement(p):
    '''while_statement : WHILE LPAREN condition RPAREN LBRACE program RBRACE'''
    p[0] = ('while', p[3], p[6])

def p_simple_statement(p):
    '''simple_statement : ID EQUALS NUMBER SEMICOLON'''
    p[0] = ('assign', p[1], p[3])

def p_condition(p):
    '''condition : ID COMPARISON NUMBER'''
    p[0] = ('condition', p[1], p[2], p[3])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

# Create lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

def pretty_print_ast(node, indent=0):
    """Pretty print the AST structure"""
    if isinstance(node, list):
        for item in node:
            pretty_print_ast(item, indent)
    elif isinstance(node, tuple):
        print("  " * indent + node[0])
        for item in node[1:]:
            pretty_print_ast(item, indent + 1)
    else:
        print("  " * indent + str(node))

def parse_and_print(code):
    """Parse the code and print both tokens and AST"""
    print("\nTokenizing the input:")
    print("-" * 40)
    
    # Reset lexer and tokenize
    lexer.input(code)
    try:
        for tok in lexer:
            print(f"Token: {tok.type:10} Value: {tok.value}")
    except Exception as e:
        print(f"Lexer error: {str(e)}")
        return

    print("\nParsing the input:")
    print("-" * 40)
    
    try:
        result = parser.parse(code)
        if result:
            print("Parse successful! AST structure:")
            pretty_print_ast(result)
        else:
            print("No valid parse result produced.")
    except Exception as e:
        print(f"Parser error: {str(e)}")

def main():
    print("Welcome to the Control Structure Parser!")
    print("Enter your code below. Supported structures:")
    print("""
1. If statement:
   if (x < 10) {
       y = 5;
   }

2. If-else statement:
   if (x < 10) {
       y = 5;
   } else {
       y = 10;
   }

3. For loop:
   for (i = 0; i < 5; i) {
       x = 1;
   }

4. While loop:
   while (count < 3) {
       count = 1;
   }

Enter your code (type 'exit' to quit, 'example' to see examples):
""")

    while True:
        print("\nEnter your code (use multiple lines, end with a blank line, type exit to end the program):")
        lines = []
        while True:
            line = input()
            if line.strip().lower() == 'exit':
                return
            if line.strip().lower() == 'example':
                example_code = """if (x < 10) {
    y = 5;
} else {
    y = 10;
}

for (i = 0; i < 5; i) {
    x = 1;
}

while (count < 3) {
    count = 1;
}"""
                print("\nExample code:")
                print(example_code)
                break
            if not line:
                break
            lines.append(line)
        
        if lines:
            code = '\n'.join(lines)
            parse_and_print(code)

if __name__ == "__main__":
    main()