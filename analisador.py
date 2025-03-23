# Helena Kuchinski Ferreira
# Loise Andruski Farion
# Grupo Projeto Compilador 1
import sys
import re
import logging
import os
import matplotlib.pyplot as plt
import antlr4

from antlr4 import *
from SintaticoLexer import SintaticoLexer
from SintaticoParser import SintaticoParser
from SintaticoListener import SintaticoListener
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Trees import Trees
from io import StringIO
from antlr4.tree.Tree import Tree

# Definição de constantes para representar dado
parentesesA = "ParentesesAberto"
numInteiro = "Inteiro"
numFloat = "Float"
opAritmetico = "OperadorAritmetico"
opRelacionais = "OperadorRelacional"
opBusca = "OperadorDeBusca"
opAtribuicao = "OperadorAtribuicao"
parentesesF = "ParenteseFechado"
fim = "Fim"
memVer = "MEM"
resVer = "RES"
If = "if"
Else = "else"
For = "for"
ERRO = "ERRO"
constante = "Constante"


# Analisador Lexico
def mefparentesesA(dado, expressao, contador, stringTokens, index):
  if dado == '(':
    string = str(dado) + ' / ' + str(type(dado)) + ' / ' + str(parentesesA)
    stringTokens.append(string)
    contador += 1
    dado = expressao[contador]
    mefResto(dado, expressao, contador, stringTokens, index)
  else:
    mefparentesesF(dado, expressao, contador, stringTokens, index)


def mefparentesesF(dado, expressao, contador, stringTokens, index):
  if len(expressao) - 1 == contador:
    if dado == ')':
      string = str(dado) + ' / ' + str(type(dado)) + ' / ' + str(parentesesF)
      stringTokens.append(string)
      mefFim(contador, stringTokens, index)
  elif dado == ')':
    string = str(dado) + ' / ' + str(type(dado)) + ' / ' + str(parentesesF)
    stringTokens.append(string)
    contador += 1
    dado = expressao[contador]
    mefResto(dado, expressao, contador, stringTokens, index)
  else:
    mefNum(dado, expressao, contador, stringTokens, index)


def mefNum(dado, expressao, contador, stringTokens, index):
  numTemp = dado.replace('.', '', 1)
  if dado.isdigit() or numTemp.isdigit():
    dado = float(dado)
    if isinstance(dado, float) and dado.is_integer():
      dado = int(dado)
    string = str(dado) + ' / ' + str(type(dado)) + ' / '
    if type(dado) == float:
      string += str(numFloat)
    elif type(dado) == int:
      string += str(numInteiro)
    stringTokens.append(string)
    contador += 1
    dado = expressao[contador]
    mefResto(dado, expressao, contador, stringTokens, index)
  else:
    mefOperador(dado, expressao, contador, stringTokens, index)


def mefOperador(dado, expressao, contador, stringTokens, index):
  if dado in ['+', '-', '*', '|', '/', '%', '^']:
    string = str(dado) + ' / ' + str(type(dado)) + ' / ' + str(opAritmetico)
    stringTokens.append(string)
    contador += 1
    dado = expressao[contador]
    mefResto(dado, expressao, contador, stringTokens, index)
  else:
    mefMEM(dado, expressao, contador, stringTokens, index)


def mefMEM(dado, expressao, contador, stringTokens, index):
  if dado == 'MEM':
    string = str(dado) + ' / ' + str(type(dado)) + ' / ' + str(memVer)
    stringTokens.append(string)
    contador += 1
    dado = expressao[contador]
    mefResto(dado, expressao, contador, stringTokens, index)
  else:
    mefRES(dado, expressao, contador, stringTokens, index)


def mefRES(dado, expressao, contador, stringTokens, index):
  if dado == 'RES':
    string = str(dado) + ' / ' + str(type(dado)) + ' / ' + str(resVer)
    stringTokens.append(string)
    contador += 1
    dado = expressao[contador]
    mefResto(dado, expressao, contador, stringTokens, index)
  else:
    mefIf(dado, expressao, contador, stringTokens, index)


def mefIf(dado, expressao, contador, stringTokens, index):
  if dado == 'if':
    string = str(dado) + ' / ' + str(type(dado)) + ' / ' + str(If)
    stringTokens.append(string)
    contador += 1
    dado = expressao[contador]
    mefResto(dado, expressao, contador, stringTokens, index)
  else:
    mefElse(dado, expressao, contador, stringTokens, index)


def mefElse(dado, expressao, contador, stringTokens, index):
  if dado == 'else':
    string = str(dado) + ' / ' + str(type(dado)) + ' / ' + str(Else)
    stringTokens.append(string)
    contador += 1
    dado = expressao[contador]
    mefResto(dado, expressao, contador, stringTokens, index)
  else:
    mefFor(dado, expressao, contador, stringTokens, index)


def mefFor(dado, expressao, contador, stringTokens, index):
  if dado == 'for':
    string = str(dado) + ' / ' + str(type(dado)) + ' / ' + str(For)
    stringTokens.append(string)
    contador += 1
    dado = expressao[contador]
    mefResto(dado, expressao, contador, stringTokens, index)
  else:
    mefComparador(dado, expressao, contador, stringTokens, index)


def mefComparador(dado, expressao, contador, stringTokens, index):
  opRela = ['==', '<', '>', '<=', '>=', '!=']
  opBus = ['in', 'not in']
  opAtri = ['=', '+=', '-=', '*=', '/=', '%=', '^=', '|=']

  if dado in opRela:
    string = str(dado) + ' / ' + str(type(dado)) + ' / ' + str(opRelacionais)
    stringTokens.append(string)
    contador += 1
    dado = expressao[contador]
    mefResto(dado, expressao, contador, stringTokens, index)
  elif dado in opBus:
    string = str(dado) + ' / ' + str(type(dado)) + ' / ' + str(opBusca)
    stringTokens.append(string)
    contador += 1
    dado = expressao[contador]
    mefResto(dado, expressao, contador, stringTokens, index)
  elif dado in opAtri:
    string = str(dado) + ' / ' + str(type(dado)) + ' / ' + str(opAtribuicao)
    stringTokens.append(string)
    contador += 1
    dado = expressao[contador]
    mefResto(dado, expressao, contador, stringTokens, index)
  else:
    mefConstantes(dado, expressao, contador, stringTokens, index)


def mefConstantes(dado, expressao, contador, stringTokens, index):
  constantes = ['i', 'range', ':']
  if dado in constantes:
    string = str(dado) + ' / ' + str(type(dado)) + ' / ' + str(constante)
    stringTokens.append(string)
    contador += 1
    dado = expressao[contador]
    mefResto(dado, expressao, contador, stringTokens, index)
  else:
    mefERRO(dado, expressao, contador, stringTokens, index)


def mefResto(dado, expressao, contador, stringTokens, index):
  if len(expressao) - 1 == contador:
    mefparentesesF(dado, expressao, contador, stringTokens, index)
  else:
    mefparentesesA(dado, expressao, contador, stringTokens, index)


def mefFim(contador, stringTokens, index):
  listaIndexValidos.append(index)
  contador = 0
  finalString = ' '
  string = str(finalString) + ' / ' + str(type(finalString)) + ' / ' + str(fim)
  stringTokens.append(string)
  return stringTokens, listaIndexValidos, contador


def mefERRO(dado, expressao, contador, stringTokens, index):
  while contador > 0:
    stringTokens.pop()
    contador -= 1
  contador = 0
  expressaoInvalida = ' '.join(expressao)
  erro = print("Erro léxico na linha:", index + 1, "na expressão:",
               expressaoInvalida)
  return contador, expressaoInvalida


# Analisador Sintático
class MeuErrorListener(ErrorListener):

  def __init__(self, inputString, linhas):
    super().__init__()
    self.inputString = inputString.replace('\n', '')
    self.linhas = linhas
    self.erro = False

  def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
    self.erro = True
    print(
        f"Erro na linha {self.linhas} na expressão: {self.inputString}, descrição do erro: {msg}"
    )


def print_tree(node, indent=0):
  if isinstance(node, TerminalNode):
    print('  ' * indent + node.symbol.text)
  else:
    print('  ' * indent + '(' + node.__class__.__name__, end='')
    if hasattr(node, 'symbol'):
      print(': ' + node.symbol.text + ')')
    else:
      print(')')
    if hasattr(node, 'children'):
      for child in node.children:
        print_tree(child, indent + 1)


def analisadorSintatico(input_expr, i, listaIndexValidosTipos):
  input_stream = InputStream(input_expr)
  lexer = SintaticoLexer(input_stream)
  stream = CommonTokenStream(lexer)
  parser = SintaticoParser(stream)
  parser.removeErrorListeners()
  error_listener = MeuErrorListener(input_expr, i)
  parser.addErrorListener(error_listener)
  tree = parser.program()
  if not error_listener.erro:
    print("\033[1m\nÁrvore sintática:\033[m")
    print_tree(tree)
    listaIndexValidosTipos.append(i - 1)
  expTemp = tree.toStringTree(recog=parser)
  return listaIndexValidosTipos


# Análise de tipos
def organizandoExpressao(expressao):

  def verificaOperador(token):
    return token in ['+', '-', '*', '|', '/', '^', '%']

  operando = []
  operadores = []
  tokens = ""
  for char in expressao:
    if char in ['(', ')', '+', '-', '*', '/', '|', '^', '%']:
      tokens += f" {char} "
    else:
      tokens += char
  tokens = tokens.split()
  for token in tokens:
    if token == '(':
      operadores.append(token)
    elif token == ')':
      operando2 = operando.pop()
      operando1 = operando.pop()
      operator = operadores.pop()
      if operando2 != 'RES' and operando1 != 'RES' and operator != 'RES':
        novaExpressao = f"{operando1} {operator} {operando2}"
      if operando2 == 'RES':
        novaExpressao = f"{operando1} {operando2}"
      operando.append(novaExpressao)
      operando[-1] = "(" + operando[-1] + ")"
    elif verificaOperador(token):
      operadores.append(token)
    else:
      operando.append(token)
  return operando[0]


class Stack:

  def __init__(self):
    self.items = []

  def push(self, item):
    self.items.append(item)

  def pop(self):
    if not self.is_empty():
      return self.items.pop()
    else:
      return None

  def is_empty(self):
    return len(self.items) == 0

  def peek(self):
    if not self.is_empty():
      return self.items[-1]
    else:
      return None

  def size(self):
    return len(self.items)

  def print_stack(self):
    print("Stack:", self.items)

  def invert_stack(self):
    return self.items[::-1]

  def pop_stack(self):
    if not self.is_empty():
      return self.items.pop(0)
    else:
      return None

  def insert_at_position(self, item, position):
    if position >= 0 and position <= len(self.items):
      self.items.insert(position, item)



nomeArquivo = sys.argv[1]
nomeArquivo = nomeArquivo.lower()

if not nomeArquivo.endswith(".txt"):
  nomeArquivo += ".txt"
aberturaArquivo = False
try:
  arquivoTxt = open(nomeArquivo, "r")
  linhas = arquivoTxt.readlines()
  aberturaArquivo = True
except:
  print("Erro ao abrir o arquivo")

if aberturaArquivo == True:
  expressaoConta = []
  for expressao in linhas:
    expressao = expressao.replace(',', '.')
    expressaoSplit = []
    dado = re.findall(r'\(|\)|\d+(?:\.\d+)?|\d+|[^\(\) ]+', expressao)
    dadoSemNovaLinha = [t.replace('\n', '') for t in dado]
    dadoSemEspacos = [t for t in dadoSemNovaLinha if t.strip()]
    expressaoSplit.extend(dadoSemEspacos)
    expressaoConta.append(expressaoSplit)

  index = 0
  contador = 0
  stringTokens = []
  listaIndexValidos = []
  listaIndexValidosTipos = []
  listaResposta = []

  print('\033[1mAnálise Lexica:\n\033[m')

  while index < len(expressaoConta):
    i = expressaoConta[index][0]
    mefparentesesA(i, expressaoConta[index], contador, stringTokens, index)
    index += 1
  print('\033[1m\nString de Tokens: \033[m', stringTokens, '\n')

  for i in listaIndexValidos:
    tmp = linhas[i]
    listaTmp = re.findall(r'\(|\)|\d+(?:\.\d+)?|\d+|[^\(\) ]+', tmp)
    if 'RES' in listaTmp:
      indice = listaTmp.index('RES')
      num = listaTmp[indice - 1]
      numero = int(num)
      if numero > i + 1:
        listaIndexValidos.remove(i)

  print('\033[1mAnálise Sintática:\n\033[m')
  for x in listaIndexValidos:
    expTemp = linhas[x]
    if 'for' in expTemp:
      expTemp = re.sub(r'\b(for\b)', r'$ $ \1', expTemp)
    elif 'if' in expTemp:
      expTemp = re.sub(r'\b(if\b)', r'$ $ \1', expTemp)
    elif 'RES' in expTemp:
      expTemp = re.sub(r'(\d+)\s+(RES)', r'$ \1 \2', expTemp)

    print("Expressao: ", expTemp)
    indiceTmp = x + 1
    listaValidosTipos = analisadorSintatico(expTemp, indiceTmp,
                                            listaIndexValidosTipos)
    print('\n')

 #Analise Tipos

  print('\033[1mAnálise de Tipos:\n\033[m')
  if os.path.exists('AnaliseDeTipos.txt'):
    os.remove('AnaliseDeTipos.txt')
  f = open('AnaliseDeTipos.txt', 'a')

  for i in listaValidosTipos:
    expressao = linhas[i]
    f.write("Expressao: " + expressao)
    f.write("  Regra de sequentes: tipoNumero(int or float) tipoNumero2(int or float) tipoResultado(int or float)\n")

    expressaoOrganizada = organizandoExpressao(expressao)
    expOrganizadaTmp = re.findall(r'\(|\)|\d+(?:\.\d+)?|\d+|[^\(\) ]+',expressaoOrganizada)

    stack = Stack()
    for y in range(len(expOrganizadaTmp)):
      stack.push(expOrganizadaTmp[y])

    pilha_str = ''.join(str(item) for item in stack.items)
    padrao = r"\([^0-9()]*[0-9]+[^\d()]*[+\-*/][^\d()]*\("
    inversao = False
    if re.search(padrao, pilha_str):
      stack_invertida = stack.invert_stack()
      stack_transformada = Stack()
      for item in stack_invertida:
        if item == '(':
          stack_transformada.push(')')
        elif item == ')':
          stack_transformada.push('(')
        else:
          stack_transformada.push(item)
      stack = stack_transformada
      inversao = True

    dado1 = None
    dado2 = None
    dado3 = None
    dado1Tmp = None
    dado2Tmp = None
    dado3Tmp = None
    resposta = None
    memoriaMEM = 0

    while not stack.is_empty():
      dado = stack.items[0]
      if stack.size() == 1:
        resposta = dado
        stack.pop_stack()
      if dado1 != None and dado2 != None and dado == '(':
        tmp1 = stack.items[1]
        numTemp = tmp1.replace('.', '', 1)
        if tmp1.isdigit() or numTemp.isdigit():
          dado1Tmp = float(tmp1)
          if isinstance(dado1Tmp, float) and dado1Tmp.is_integer():
            dado1Tmp = int(tmp1)
        elif tmp1 == 'MEM':
          dado1Tmp = memoriaMEM
        dado2Tmp = stack.items[2]
        tmp2 = stack.items[3]
        numTemp = tmp2.replace('.', '', 1)
        if tmp2.isdigit() or numTemp.isdigit():
          dado3Tmp = float(tmp2)
          if isinstance(dado3Tmp, float) and dado3Tmp.is_integer():
            dado3Tmp = int(tmp2)
        elif tmp2 == 'MEM':
          dado3Tmp = memoriaMEM
        stack.pop_stack()

      if dado == '(' or dado == ')':
        stack.pop_stack()
      elif dado1 is None:
        if type(dado) == int or type(dado) == float:
          dado1 = dado
        elif dado == 'RES':
          dado1 = dado
        else:
          numTemp = dado.replace('.', '', 1)
          if dado.isdigit() or numTemp.isdigit():
            dado1 = float(dado)
            if isinstance(dado1, float) and dado1.is_integer():
              dado1 = int(dado)
          elif dado == 'MEM':
            dado1 = memoriaMEM
          stack.pop_stack()
      elif dado2 is None:
        if dado1 == 'RES' or dado == 'RES':
          if dado.isdigit():
            tmp = int(dado)
            indice = i - tmp
            if indice in listaValidosTipos:
              indiceResp = listaValidosTipos.index(indice)
              dado1 = listaResposta[indiceResp]
              stack.pop_stack()
              stack.insert_at_position(conta, 1)

          elif type(dado1) == int or dado1.isdigit():
            tmp = int(dado1)
            indice = i - tmp
            if tmp > 1:
              indice -= 1
            if indice in listaValidosTipos:
              indiceResp = listaValidosTipos.index(indice)
              dado1 = listaResposta[indiceResp]
              stack.pop_stack()
              stack.insert_at_position(conta, 1)
        elif dado in ['+', '-', '*', '/', '|', '^', '%']:
          dado2 = dado
        stack.pop_stack()
      elif dado3 is None and dado1 != 'RES':
        if type(dado) == int or type(dado) == float:
          dado3 = dado
        else:
          numTemp = dado.replace('.', '', 1)
          if dado.isdigit() or numTemp.isdigit():
            dado3 = float(dado)
            if isinstance(dado3, float) and dado3.is_integer():
              dado3 = int(dado)
          elif dado == 'MEM':
            dado3 = memoriaMEM
          stack.pop_stack()

      if dado1Tmp != None and dado2Tmp != None and dado3Tmp != None:
        if dado2Tmp == '+':
          conta = dado1Tmp + dado3Tmp
          f.write(
              f"    -> Tipo número {dado1Tmp}: {type(dado1Tmp)} -> Tipo número {dado3Tmp}: {type(dado3Tmp)} -> Tipo resultado {conta}: {type(conta)}\n"
          )

        elif dado2Tmp == '-':
          conta = dado1Tmp - dado3Tmp
          if inversao == True and dado1Tmp < dado3Tmp:
            conta = abs(conta)
          elif inversao == False and dado1Tmp < dado3Tmp:
            conta = conta
          elif inversao == True and dado1Tmp > dado3Tmp:
            conta = conta * (-1)
          elif inversao == False and dado1Tmp > dado3Tmp:
            conta = conta
          else:
            conta = conta
          f.write(
              f"    -> Tipo número {dado1Tmp}: {type(dado1Tmp)} -> Tipo número {dado3Tmp}: {type(dado3Tmp)} -> Tipo resultado {conta}: {type(conta)}\n"
          )

        elif dado2Tmp == '*':
          conta = dado1Tmp * dado3Tmp
          f.write(
              f"    -> Tipo número {dado1Tmp}: {type(dado1Tmp)} -> Tipo número {dado3Tmp}: {type(dado3Tmp)} -> Tipo resultado {conta}: {type(conta)}\n"
          )

        elif dado2Tmp == '/':
          if inversao == True:
            conta = dado3Tmp // dado1Tmp
          else:
            conta = dado1Tmp // dado3Tmp
          f.write(
              f"    -> Tipo número {dado1Tmp}: {type(dado1Tmp)} -> Tipo número {dado3Tmp}: {type(dado3Tmp)} -> Tipo resultado {conta}: {type(conta)}\n"
          )

        elif dado2Tmp == '|':
          if inversao == True:
            conta = dado3Tmp / dado1Tmp
          else:
            conta = dado1Tmp / dado3Tmp
          f.write(
              f"    -> Tipo número {dado1Tmp}: {type(dado1Tmp)} -> Tipo número {dado3Tmp}: {type(dado3Tmp)} -> Tipo resultado {conta}: {type(conta)}\n"
          )

        elif dado2Tmp == '^':
          if inversao == True:
            conta = int(dado3Tmp)**int(dado1Tmp)
          else:
            conta = int(dado1Tmp)**int(dado3Tmp)
          f.write(
              f"    -> Tipo número {dado1Tmp}: {type(dado1Tmp)} -> Tipo número {dado3Tmp}: {type(dado3Tmp)} -> Tipo resultado {conta}: {type(conta)}\n"
          )

        elif dado2Tmp == '%':
          if inversao == True:
            conta = dado3Tmp % dado1Tmp
          else:
            conta = dado1Tmp % dado3Tmp
          f.write(
              f"    -> Tipo número {dado1Tmp}: {type(dado1Tmp)} -> Tipo número {dado3Tmp}: {type(dado3Tmp)} -> Tipo resultado {conta}: {type(conta)}\n"
          )
        dado3 = conta

        stack.insert_at_position(dado3, stack.size())
        stack.pop_stack()
        stack.pop_stack()
        stack.pop_stack()

      if dado1 != None and dado2 != None and dado3 != None:
        if dado2 == '+':
          conta = dado1 + dado3
          f.write(
              f"    -> Tipo número {dado1}: {type(dado1)} -> Tipo número {dado3}: {type(dado3)} -> Tipo resultado {conta}: {type(conta)}\n"
          )
        elif dado2 == '-':
          conta = dado1 - dado3
          if inversao == True and dado1 < dado3:
            conta = abs(conta)
          elif inversao == False and dado1 < dado3:
            conta = conta
          elif inversao == True and dado1 > dado3:
            conta = conta * (-1)
          elif inversao == False and dado1 > dado3:
            conta = conta
          else:
            conta = conta
          f.write(
              f"    -> Tipo número {dado1}: {type(dado1)} -> Tipo número {dado3}: {type(dado3)} -> Tipo resultado {conta}: {type(conta)}\n"
          )
        elif dado2 == '*':
          conta = dado1 * dado3
          f.write(
              f"    -> Tipo número {dado1}: {type(dado1)} -> Tipo número {dado3}: {type(dado3)} -> Tipo resultado {conta}: {type(conta)}\n"
          )
        elif dado2 == '/':
          if inversao == True:
            conta = dado3 // dado1
          else:
            conta = dado1 // dado3
          f.write(
              f"    -> Tipo número {dado1}: {type(dado1)} -> Tipo número {dado3}: {type(dado3)} -> Tipo resultado {conta}: {type(conta)}\n"
          )
        elif dado2 == '|':
          if inversao == True:
            conta = dado3 / dado1
          else:
            conta = dado1 / dado3
          f.write(
              f"    -> Tipo número {dado1}: {type(dado1)} -> Tipo número {dado3}: {type(dado3)} -> Tipo resultado {conta}: {type(conta)}\n"
          )
        elif dado2 == '^':
          if inversao == True:
            conta = int(dado3)**int(dado1)
          else:
            conta = int(dado1)**int(dado3)
          f.write(
              f"    -> Tipo número {dado1}: {type(dado1)} -> Tipo número {dado3}: {type(dado3)} -> Tipo resultado {conta}: {type(conta)}\n"
          )
        elif dado2 == '%':
          if inversao == True:
            conta = dado3 % dado1
          else:
            conta = dado1 % dado3
          f.write(
              f"    -> Tipo número {dado1}: {type(dado1)} -> Tipo número {dado3}: {type(dado3)} -> Tipo resultado {conta}: {type(conta)}\n"
          )
        if dado1Tmp == None:
          stack.insert_at_position(conta, 1)
        else:
          stack.insert_at_position(conta, stack.size())

        dado1 = None
        dado2 = None
        dado3 = None
        dado1Tmp = None
        dado2Tmp = None
        dado3Tmp = None

    linha = i + 1
    expressao = expressao.rstrip('\n')

    if resposta == None:
      resposta = 0

    print("Linha", linha, "-> Expressão: ", expressao, " = ", resposta)
    f.write(f"    -> Tipo resposta expressao = {resposta}: {type(resposta)} \n")
    listaResposta.append(resposta)
    resposta = None
