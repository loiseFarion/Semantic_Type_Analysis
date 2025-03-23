# CALCULATOR PROJECT - PHASE 3
This is a Python program designed to perform lexical and syntactic validation of expressions contained in available test files. It also analyzes the types of each operand in valid expressions, generating a text file with the expressions, operand types, the sequence rule used to validate these types, and the final expression type.

## Running the program
If only the following files are available: <br />
analisador.py <br />
formulas1.txt <br />
formulas2.txt <br />
formulas3.txt <br />
MEFAnalisadorLexico.png <br />
readme.md <br />
TabelaDerivacao.png <br />
Run the command: antlr4 -Dlanguage=Python3 Sintatico.g4<br><br>
Otherwise, just do the following: <br />
--- Replit Shell <br />
python analisador.py 'formulasn' <br />
Where n can be: 1, 2, or 3. <br />

### Example of a valid expression pattern
(8 16 -) <br />
(48 (16 1 -) |) <br />
((5 RES) MEM) <br />
(MEM 2 *) <br />
((5.8 4.2 +) (2 3 *) +) <br />
(4 (2 3 *) +) <br />
(2 RES) <br />
(2 (2 (2 (2 (2 2 *) *) *) *) *) <br />
(if MEM >= 5: MEM = 10) <br />
(if MEM < 3: MEM = 1 else: MEM = 5) <br />
(for i in range(MEM): MEM -= 10) <br />
(2 MEM +) <br />

Additionally, valid expressions are separated into tokens, which are used to generate a token string.

After performing lexical analysis, the program validates the syntax of expressions that have no lexical errors. For correct analysis, the syntactic analyzer was developed based on the production rules created and the LL(1) table.

Moreover, the program generates the corresponding syntax tree for the production rules created and validated with FIRST and FOLLOW for LL(1).

## Lexical Analyzer with Finite State Machine
### - Finite State Machine Transition Diagram
<img src="MEFAnalisadorLexico.png"><br>
The finite state machine created for the lexical analyzer is based on the structure of valid expressions mentioned earlier. Its functionality consists of:

#### 1st state:
Checks if the input consists of an open parenthesis '('

#### 2nd state:
Checks if the input consists of a closing parenthesis ')'

#### 3rd state:
Checks if the input consists of a number (int or float)

#### 4th state:
Checks if the input consists of an arithmetic operator ('+', '-', '*', '|', '/', '%', '^')

#### 5th state:
Checks if the input consists of 'MEM'

#### 6th state:
Checks if the input consists of 'RES'

#### 7th state:
Checks if the input consists of 'if'

#### 8th state:
Checks if the input consists of 'else:'

#### 9th state:
Checks if the input consists of 'for'

#### 10th state:
Checks if the input consists of a comparator ('==', '<', '>', '<=', '>=', '!=' or 'in', 'not in' or '=', '+=', '-=', '*=', '/=', '%=', '^=', '|=')

#### 11th state:
Checks if the input consists of a constant ('i', 'range', ':')

The verification is done linearly, where the machine checks state 1. If invalid, it moves to state 2. If it reaches state 11 and it is also invalid, it transitions to the error state, pointing out the lexical error. If the validation is successful in any state, the machine moves to the next state to check if there is more to analyze. If the string reaches the end, the machine finishes, but if the expression is nested, the machine re-enters the verification process.

## Syntactic Analyzer
### Production Rules

E → (op op operand)<br><br>
operand → + OR - OR * OR / OR | OR % OR ^ OR M OR R OR F OR I <br><br>
F → for i ob range ( M ) : M oat n <br><br>
I → if M opr n : M oat n e <br><br>
e → else : M oat n | $ <br><br>
opr → == OR < OR > OR <= OR >= OR != <br><br>
ob → in OR notIn <br><br>
oat → = OR += OR -= <br><br>
op → n OR E OR M OR $ <br><br>
n → num <br><br>
M → mem <br><br>
R → res <br><br>

Meaning of abbreviations:<br><br>
E: Expression<br>
oat: Assignment operator<br>
ob: Search operator<br>
opr: Relational operator<br>
num: [0..9]+ OR [0-9]+\.[0-9]+ <br>

### FIRST and FOLLOW Sets
FIRST(S) = {(}<br>
FIRST(E) = {(}<br>
FIRST(operand) = {+, -, *, /, |, %, ^, mem, res, for, if}<br>
FIRST(F) = {for}<br>
FIRST(I) = {if}<br>
FIRST(e) = {else, $}<br>
FIRST(opr) = {==, <, >, <=, >=, !=}<br>
FIRST(ob) = {in, notin}<br>
FIRST(oat) = {=, +=, -=}<br>
FIRST(op) = {(, $, num, mem}<br>
FIRST(n) = {num}<br>
FIRST(M) = {mem}<br>
FIRST(R) = {res}<br>

FOLLOW(S) = {$}<br>
FOLLOW(E) = {+, -, *, /, |, %, ^, mem, res, for, if, (, $, num}<br>
FOLLOW(operand) = {)}<br>
FOLLOW(F) = {)}<br>
FOLLOW(I) = {)}<br>
FOLLOW(e) = {)}<br>
FOLLOW(opr) = {num}<br>
FOLLOW(ob) = {range}<br>
FOLLOW(oat) = {num}<br>
FOLLOW(op) = {+, -, *, /, |, %, ^, mem, res, for, if, (, $, num}<br>
FOLLOW(n) = {), else, $, :, +, -, *, /, |, %, ^, mem, res, for, if, (, num}<br>
FOLLOW(M) = {), =, +=, -=, ==, <, >, <=, >=, !=, +, -, *, /, |, %, ^, mem, res, for, if, (, $, num}<br>
FOLLOW(R) = {)}<br>

### Derivation Table
<img src="TabelaDerivacao.png"><br>
After creating the production rules with First and Follow for LL(1) and the derivation table, a syntactic analyzer was developed using ANTLR, ensuring it follows the defined grammar.

Moreover, treatments were done to fill in the empty spaces between parentheses with $, allowing the syntactic analyzer to validate correctly.

## Type Analyzer
### Sequence Rules
  Sequence Rule: tipoNumero(int or float) tipoNumero2(int or float) tipoResultado(int or float).
### Functionality
  It analyzes the operand types. This analysis traverses the data stack from the child nodes, recording in a txt file with the expressions, operand types, the sequence rule used to validate these types, and the final expression type.
### Txt File with Type Analysis
  File name: `AnaliseDeTipos.txt`
  File content:
  Expression: ((90 5 /) (4 3 *) +)
  Sequence rule: tipoNumero(int or float) tipoNumero2(int or float) tipoResultado(int or float)
    -> Number type 90: <class 'int'> -> Number type 5: <class 'int'> -> Result type 18: <class 'int'>
    -> Number type 4: <class 'int'> -> Number type 3: <class 'int'> -> Result type 12: <class 'int'>
    -> Number type 18: <class 'int'> -> Number type 12: <class 'int'> -> Result type 30: <class 'int'>
    -> Final expression type: <class 'int'>
