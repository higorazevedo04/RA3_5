# Analisador Semantico

---

## Identificação

| Campo        | Informação                                        |
|--------------|---------------------------------------------------|
| **Instituição** | Pontifícia Universidade Católica do Paraná (PUCPR)            |
| **Disciplina**  | Linguagens Formais e Compiladores            |
| **Ano**         | 2026                                         |
| **Professor**   | Frank de Alcantara                           |
| **Grupo (Canvas)** | RA3_5                                     |
| **Fase**        | Fase 3 — Analisador Semântico + Assembly     |
| **Linguagem de implementação** | Python 3                      |

---

##  Integrantes do Grupo 

| Nome completo |
|---------------|
| Higor Leonardo da Silva Azevedo | 

---

##  Sumário

1. [Descrição da Linguagem](#1-descrição-da-linguagem)
2. [Linguagem de Implementação](#2-linguagem-de-implementação)
3. [Tipos Suportados](#3-tipos-suportados)
4. [Regras para Definição e Uso de Variáveis](#4-regras-para-definição-e-uso-de-variáveis)
5. [Instruções para Compilar, Executar e Testar](#5-instruções-para-compilar-executar-e-testar)
6. [Arquivos de Saída Gerados](#6-arquivos-de-saída-gerados)
7. [Exemplos de Programas Semanticamente Válidos](#7-exemplos-de-programas-semanticamente-válidos)
8. [Exemplos de Programas Semanticamente Inválidos](#8-exemplos-de-programas-semanticamente-inválidos)
9. [Tabela de Símbolos](#9-tabela-de-símbolos)
10. [Árvore Sintática Atribuída](#10-árvore-sintática-atribuída)
11. [Gramática em EBNF](#11-gramática-em-ebnf)
12. [Regras Semânticas em Cálculo de Sequentes](#12-regras-semânticas-em-cálculo-de-sequentes)
13. [Estrutura do Repositório](#13-estrutura-do-repositório)

---

## 1. Descrição da Linguagem

A linguagem implementada é uma linguagem imperativa em **notação polonesa reversa (RPN — Reverse Polish Notation)**, também chamada de notação pós-fixa. Nela, os operandos são escritos **antes** do operador, eliminando ambiguidades de precedência sem necessidade de parênteses extras.

### Características gerais

| Característica | Descrição |
|----------------|-----------|
| **Paradigma** | Imperativo / procedural |
| **Notação** | Pós-fixa (RPN) |
| **Delimitadores de programa** | `(START)` ... `(END)` |
| **Delimitadores de instrução** | `(` ... `)` |
| **Controle de fluxo** | `IF` e `WHILE`, com blocos entre `{` `}` |
| **Comentários** | `*{` texto `}*` (podem ser multilinha) |
| **Declaração de variáveis** | Implícita via comando `MEM` |
| **Recuperação de resultados** | Via comando `RES` |
| **Geração de código alvo** | ARMv7 Assembly (CPulator / DE1-SoC com extensões VFP) |

### Exemplo básico

```
(START)
(10 X MEM)          *{ armazena 10 em X }*
(X 5 +)             *{ calcula X + 5 }*
(1 RES)             *{ exibe resultado da instrucao anterior }*
(END)
```

---

## 2. Linguagem de Implementação

O compilador foi inteiramente implementado em **Python 3**, sem dependências externas. Todas as bibliotecas utilizadas fazem parte da biblioteca padrão:

| Módulo | Uso |
|--------|-----|
| `sys`  | Leitura de argumentos da linha de comando |
| `os`   | Manipulação de caminhos e arquivos |
| `json` | Serialização das árvores e tabela de símbolos |
| `re`   | Expressões regulares para limpeza de entrada |

**Requisito mínimo:** Python 3.8 ou superior.

---

## 3. Tipos Suportados

A linguagem possui três tipos primitivos:

| Tipo   | Descrição                         | Literais de exemplo     |
|--------|-----------------------------------|-------------------------|
| `int`  | Inteiro com sinal (64 bits)       | `42`, `-7`, `0`         |
| `real` | Ponto flutuante de dupla precisão | `3.14`, `-0.5`, `100.0` |
| `bool` | Booleano lógico                   | `TRUE`, `FALSE`         |

### Regras de compatibilidade por operador

| Operador(es)     | Tipos dos operandos aceitos               | Tipo do resultado |
|------------------|-------------------------------------------|-------------------|
| `+` `-` `*` `^`  | `int` × `int`                             | `int`             |
| `+` `-` `*` `^`  | qualquer combinação com `real`            | `real`            |
| `/`              | `int` × `int` **somente**                 | `int`             |
| `%`              | `int` × `int` **somente**                 | `int`             |
| `\|`             | `int` ou `real` × `int` ou `real`        | `real`            |
| `>` `<` `==`     | numéricos compatíveis (`int`/`real`)      | `bool`            |
| condição de `IF` / `WHILE` | obrigatoriamente `bool`         | `ok`              |
| `RES`            | argumento **int** obrigatório             | `any`             |
| `MEM`            | qualquer expressão válida                 | tipo da expressão |

> **Restrição importante:** O tipo `bool` **não pode** ser operando de nenhuma operação aritmética (`+`, `-`, `*`, `/`, `%`, `|`, `^`).

---

## 4. Regras para Definição e Uso de Variáveis

### 4.1 Definição (declaração)

Variáveis são criadas com o comando `MEM`, que possui a sintaxe:

```
(VALOR NOME_VARIAVEL MEM)
```

- `VALOR` é qualquer expressão válida (literal, outra variável, instrução aninhada).
- `NOME_VARIAVEL` é um identificador: começa com letra ou `_`, seguido de letras, dígitos ou `_`.
- O tipo da variável é **inferido automaticamente** a partir do tipo do valor atribuído.

**Exemplos de definição:**

```
(42 X MEM)          *{ X recebe tipo int  }*
(3.14 PI MEM)       *{ PI recebe tipo real }*
(TRUE FLAG MEM)     *{ FLAG recebe tipo bool }*
(X 1 + CONTADOR MEM)  *{ CONTADOR recebe tipo int }*
```

### 4.2 Uso

Uma variável pode ser usada como operando em qualquer expressão **após** ter sido definida com `MEM`:

```
(START)
(10 X MEM)    *{ definicao de X }*
(X 5 +)       *{ uso valido: X ja existe }*
(END)
```

### 4.3 Regras obrigatórias

| Regra | Descrição |
|-------|-----------|
| **Definição antes do uso** | Toda variável **deve** ser definida com `MEM` antes de aparecer em qualquer expressão. O uso antes da definição é **erro semântico fatal**. |
| **Identificadores válidos** | Devem começar com letra ou `_`; podem conter letras, dígitos e `_`. Não podem ser palavras reservadas (`START`, `END`, `IF`, `WHILE`, `MEM`, `RES`, `TRUE`, `FALSE`). |
| **Tipo fixo após definição** | Após a primeira atribuição, redefnir a mesma variável com um tipo **incompatível** é erro. Ex.: definir `X` como `int` e depois como `real` causa erro de redefinição. |
| **Escopo** | Não há escopos aninhados. Variáveis definidas dentro de blocos `{ }` de `IF`/`WHILE` são visíveis no nível global após o bloco. |
| **Case-sensitive** | `X` e `x` são variáveis diferentes. |

### 4.4 Erros relacionados a variáveis

| Situação | Mensagem de erro emitida |
|----------|--------------------------|
| Usar variável sem `MEM` | `Variavel 'X' usada sem definicao previa com (V MEM).` |
| Redefinir com tipo incompatível | `Redefinicao incompativel de 'X': tipo anterior 'int', novo tipo 'real'.` |
| Nome com caractere inválido | `[ERRO LEXICO] Caractere invalido '@' na posicao N` |

---

## 5. Instruções para Compilar, Executar e Testar

### 5.1 Pré-requisitos

- **Python 3.8 ou superior** instalado e disponível no PATH.
- Sem instalação de dependências externas necessária.

### 5.2 Clonar o repositório

```bash
git clone https://github.com/<usuario>/rpn-compiler.git
cd rpn-compiler
```

### 5.3 Executar o compilador

```bash

python AnalisadorSemantico.py <teste1.txt>

# Sintaxe geral
python AnalisadorSemantico.py <arquivo.txt>

# Exemplo com arquivo válido
python AnalisadorSemantico.py exemplos/validos/controle_fluxo.txt

# Exemplo com arquivo inválido (para ver os erros)
python AnalisadorSemantico.py exemplos/invalidos/erro_tipo_divisao.txt
```

### 5.4 Rodar a suíte de testes automáticos

Execute **sem argumentos** para rodar todos os testes internos (léxicos, sintáticos e semânticos):

```bash
python AnalisadorSemantico.py
```

Saída esperada:

```
[FASE 1: TESTES LEXICOS]
Teste Lexico [Bloquear token '@']: PASSOU
...
[FASE 2: TESTES SINTATICOS LL(1)]
Teste Sintatico [Soma Simples (Float)]: PASSOU
...
[FASE 3: TESTES SEMANTICOS]
Teste Semantico [Tipo valido: int + int]: PASSOU
...
```

Cada linha indica `PASSOU` se o comportamento do compilador corresponde ao esperado, ou `FALHOU` se há regressão.

### 5.5 Depuração

#### Usando o Python Debugger (pdb)

```bash
python -m pdb AnalisadorSemantico.py exemplos/validos/controle_fluxo.txt
```

Comandos úteis dentro do `pdb`:

| Comando     | Ação                                       |
|-------------|--------------------------------------------|
| `n`         | Avança para a próxima linha                |
| `s`         | Entra dentro da função chamada             |
| `c`         | Continua até o próximo breakpoint          |
| `p variavel`| Imprime o valor de uma variável            |
| `b N`       | Define breakpoint na linha N               |
| `l`         | Lista as linhas ao redor do cursor atual   |
| `q`         | Sai do debugger                            |

#### Inspecionar a AST após execução

```python
import json
with open("arvore_ast.json") as f:
    print(json.dumps(json.load(f), indent=2, ensure_ascii=False))
```

#### Inspecionar a tabela de símbolos

```python
import json
with open("tabela_simbolos.json") as f:
    dados = json.load(f)
for nome, info in dados["tabela_simbolos"].items():
    print(f"{nome}: tipo={info['tipo']}, def={info['linha_def']}, usos={info['linhas_uso']}")
```

---

## 6. Arquivos de Saída Gerados

Após a compilação bem-sucedida de um arquivo fonte, os seguintes arquivos são criados no diretório de trabalho:

### 6.1 `saida_lexica.txt`

Lista de todos os tokens reconhecidos pelo analisador léxico, um por linha, no formato `CATEGORIA,valor`.

**Categorias possíveis:** `PARENTESE_ESQUERDA`, `PARENTESE_DIREITA`, `CHAVES`, `OPERADOR`, `BOOLEANO`, `NUMERO`, `PALAVRA`.

**Exemplo de conteúdo:**
```
PARENTESE_ESQUERDA,(
PALAVRA,START
PARENTESE_DIREITA,)
PARENTESE_ESQUERDA,(
NUMERO,10
PALAVRA,X
PALAVRA,MEM
PARENTESE_DIREITA,)
```

---

### 6.2 `arvore_cst.json`

**Árvore de Derivação Concreta (CST — Concrete Syntax Tree)** em formato JSON. Representa a estrutura sintática completa da entrada, incluindo todos os não-terminais intermediários da gramática. Útil para depurar o parser.

**Exemplo de trecho:**
```json
{
  "nome": "programa",
  "filhos": [
    { "terminal": "(" },
    { "terminal": "START" },
    ...
  ]
}
```

---

### 6.3 `arvore_ast.json`

**Árvore Sintática Abstrata (AST — Abstract Syntax Tree)** em formato JSON. Contém apenas os nós semanticamente relevantes, sem os não-terminais auxiliares da gramática. É a entrada da fase semântica.

**Exemplo:**
```json
{
  "tipo": "programa_ast",
  "instrucoes": [
    {
      "tipo": "operacao",
      "operador": "+",
      "esquerda": { "tipo": "numero", "valor": 3 },
      "direita":  { "tipo": "numero", "valor": 4 }
    }
  ]
}
```

---

### 6.4 `arvore_atribuida.json`

**AST Atribuída** — igual à `arvore_ast.json`, porém com o campo `tipo_dado` preenchido em cada nó após a análise semântica. Permite rastrear o tipo inferido de cada subexpressão.

**Exemplo:**
```json
{
  "tipo": "operacao",
  "operador": "+",
  "esquerda": { "tipo": "numero", "valor": 3, "tipo_dado": "int" },
  "direita":  { "tipo": "numero", "valor": 4, "tipo_dado": "int" },
  "tipo_dado": "int"
}
```

---

### 6.5 `arvore_atribuida.md`

Relatório legível em Markdown da AST atribuída. Contém:
- Tabela de símbolos com tipos e linhas de uso.
- Lista de erros semânticos detectados.
- Regras de tipo em notação de cálculo de sequentes.
- O JSON da árvore atribuída em bloco de código.

---

### 6.6 `tabela_simbolos.json`

Tabela de símbolos serializada em JSON. Contém duas chaves de nível superior:

- `tabela_simbolos`: dicionário `nome → {tipo, linha_def, linhas_uso, definida}`.
- `erros_semanticos`: lista de erros com `linha`, `elemento` e `causa`.

**Exemplo:**
```json
{
  "tabela_simbolos": {
    "X": { "tipo": "int", "linha_def": 1, "linhas_uso": [2, 3], "definida": true }
  },
  "erros_semanticos": []
}
```

---

### 6.7 `tabela_simbolos.md`

Versão legível em Markdown da tabela de símbolos. Exibe uma tabela formatada com variável, tipo, linha de definição e linhas de uso, seguida da lista de erros semânticos.

---

### 6.8 `saida_assembly.s`

Código Assembly ARMv7 gerado para o CPulator (DE1-SoC, extensões VFP). Estrutura do arquivo:

- **Seção `.data`:** constantes numéricas (`.double`), variáveis do programa (`.double 0.0`), array de resultados (`array_res`) e ponteiro `ptr_res`.
- **Seção `.text`:** instruções ARM geradas a partir da AST, usando registradores VFP de 64 bits (`D0`–`D3`) e pilha de software via `SP`.

---

### 6.9 `relatorio_validacao_ll1.txt`

Relatório textual da validação teórica do parser LL(1). Contém:
- A gramática completa em EBNF.
- Os conjuntos FIRST de todos os não-terminais.
- Os conjuntos FOLLOW de todos os não-terminais.
- A contagem de transições determinísticas mapeadas e a confirmação de ausência de conflitos FIRST/FIRST e FIRST/FOLLOW.

---

## 7. Exemplos de Programas Semanticamente Válidos

#### 1. Operações aritméticas básicas

```
(START)
(3 4 +)
(10 2 -)
(6 7 *)
(END)
```

#### 2. Divisão inteira e divisão real

```
(START)
(10 3 /)      *{ divisao inteira: resultado 3 }*
(10.0 4.0 |)  *{ divisao real: resultado 2.5 }*
(END)
```

#### 3. Declaração e uso de variáveis com MEM

```
(START)
(42 X MEM)
(3.14 PI MEM)
(X PI *)
(END)
```

#### 4. Condicional IF

```
(START)
(5 X MEM)
(X 0 > { (X 1 -) } IF)
(END)
```

#### 5. Laço WHILE com contador

```
(START)
(0 I MEM)
(I 10 < { (I 1 +) } WHILE)
(END)
```

#### 6. Expressões aninhadas

```
(START)
((2 3 +) (4 5 *) |)
(END)
```

#### 7. Booleanos em estruturas de controle

```
(START)
(TRUE { (1 2 +) } IF)
(END)
```

#### 8. Potenciação e módulo

```
(START)
(2 10 ^)
(17 5 %)
(END)
```

#### 9. Recuperação de resultado com RES

```
(START)
(10 5 +)
(1 RES)
(END)
```

---

## 8. Exemplos de Programas Semanticamente Inválidos

#### 1. Variável usada sem definição prévia

```
(START)
(X 1 +)
(END)
```
> ❌ `Variavel 'X' usada sem definicao previa com (V MEM).`

#### 2. Divisão inteira com operandos reais

```
(START)
(3.5 2.0 /)
(END)
```
> ❌ `Operador '/' requer operandos inteiros. Recebeu 'real' e 'real'.`

#### 3. Módulo com operandos reais

```
(START)
(5.0 2.0 %)
(END)
```
> ❌ `Operador '%' requer operandos inteiros. Recebeu 'real' e 'real'.`

#### 4. Operação aritmética com booleano

```
(START)
(TRUE 2 +)
(END)
```
> ❌ `Operador '+' nao pode ser aplicado a tipo 'bool'.`

#### 5. IF com condição não-booleana

```
(START)
(5 X MEM)
(X { (1 RES) } IF)
(END)
```
> ❌ `Condicao de 'IF' deve ter tipo 'bool', mas recebeu 'int'.`

#### 6. WHILE com condição inteira

```
(START)
(1 { (2 3 +) } WHILE)
(END)
```
> ❌ `Condicao de 'WHILE' deve ter tipo 'bool', mas recebeu 'int'.`

#### 7. Variável não declarada dentro de bloco WHILE

```
(START)
(TRUE { (NAO_DECLARADA 1 +) } WHILE)
(END)
```
> ❌ `Variavel 'NAO_DECLARADA' usada sem definicao previa com (V MEM).`

#### 8. RES com argumento real

```
(START)
(10 5 +)
(1.5 RES)
(END)
```
> ❌ `O argumento de RES deve ser inteiro, mas recebeu 'real'.`

#### 9. Redefinição incompatível de variável

```
(START)
(10 X MEM)
(3.14 X MEM)
(END)
```
> ❌ `Redefinicao incompativel de 'X': tipo anterior 'int', novo tipo 'real'.`

#### 10. Comentário não fechado (erro léxico)

```
(START)
*{ comentario aberto sem fechamento
(1 2 +)
(END)
```
> ❌ `[ERRO LEXICO] Linha 2: Comentario nao fechado (falta '}*')`

---

## 9. Tabela de Símbolos

A **Tabela de Símbolos** (classe `TabelaSimbolos`) rastreia todas as variáveis declaradas durante a compilação.

### Estrutura de cada entrada

```json
{
  "nome_variavel": {
    "tipo":       "int | real | bool | null",
    "linha_def":  1,
    "linhas_uso": [2, 3, 5],
    "definida":   true
  }
}
```

### Operações

| Método | Descrição |
|--------|-----------|
| `definir(nome, tipo, linha)` | Registra ou atualiza variável. Retorna `(False, msg)` em redefinição incompatível. |
| `usar(nome, linha)` | Registra ocorrência de uso; retorna `False` se variável não existe. |
| `tipo_de(nome)` | Retorna o tipo inferido da variável, ou `None`. |
| `esta_definida(nome)` | `True` se a variável foi criada por `MEM`. |
| `para_dict()` | Exporta a tabela inteira como dicionário Python. |

---

## 10. Árvore Sintática Atribuída

A AST atribuída é a AST com o campo `tipo_dado` adicionado a cada nó após a análise semântica.

### Tipos de nós

| Tipo de nó | Campos principais |
|------------|-------------------|
| `programa_ast` | `instrucoes: []` |
| `numero` | `valor`, `tipo_dado` (`int`/`real`/`bool`) |
| `variavel` | `nome`, `tipo_dado` |
| `operacao` | `operador`, `esquerda`, `direita`, `tipo_dado` |
| `comando` MEM | `val_expr`, `nome_var`, `tipo_dado` |
| `comando` RES | `alvo`, `tipo_dado` |
| `controle` | `estrutura` (`IF`/`WHILE`), `condicao`, `bloco`, `tipo_dado` |
| `bloco` | `instrucoes: []`, `tipo_dado` |

### Exemplo de nó atribuído

Instrução `(3 4 +)`:
```json
{
  "tipo": "operacao",
  "operador": "+",
  "esquerda": { "tipo": "numero", "valor": 3, "tipo_dado": "int" },
  "direita":  { "tipo": "numero", "valor": 4, "tipo_dado": "int" },
  "tipo_dado": "int"
}
```

---

## 11. Gramática em EBNF

Consulte o arquivo [`docs/gramatica_ebnf.md`](docs/gramatica_ebnf.md) para a documentação completa com FIRST, FOLLOW e prova de propriedade LL(1).

**Resumo:**

```ebnf
programa          ::= '(' START ')' laco_principal
laco_principal    ::= '(' linha_ou_fim
linha_ou_fim      ::= END ')' | conteudo_rpn ')' laco_principal
lista_instrucoes  ::= instrucao { instrucao }
instrucao         ::= '(' conteudo_rpn ')'
conteudo_rpn      ::= valor elementos
elementos         ::= COMMAND | valor acao_final | estrutura_controle
acao_final        ::= operador [ estrutura_controle ] | estrutura_controle | COMMAND
estrutura_controle ::= bloco_codigo tipo_controle
tipo_controle     ::= IF | WHILE
bloco_codigo      ::= '{' lista_instrucoes '}'
valor             ::= ID | NUM | instrucao
operador          ::= '+' | '-' | '*' | '|' | '/' | '%' | '^' | '>' | '<' | '=='
COMMAND           ::= RES | MEM
```

---

## 12. Regras Semânticas em Cálculo de Sequentes

Consulte o arquivo [`docs/regras_semanticas.md`](docs/regras_semanticas.md) para a formalização completa.

**Resumo das regras principais:**

```
[INT-LIT]   ⊢ n : int
[REAL-LIT]  ⊢ r : real
[BOOL-LIT]  ⊢ b : bool
[VAR]       x:T ∈ Γ  ⊢  x : T
[ARIT-INT]  Γ⊢e1:int, Γ⊢e2:int, op∈{+,-,*,^}  ⊢  (e1 e2 op):int
[ARIT-REAL] T1∨T2=real, op∈{+,-,*,^}           ⊢  (e1 e2 op):real
[DIV-INT]   Γ⊢e1:int, Γ⊢e2:int  ⊢  (e1 e2 /):int
[MOD-INT]   Γ⊢e1:int, Γ⊢e2:int  ⊢  (e1 e2 %):int
[DIV-REAL]  T1,T2∈{int,real}    ⊢  (e1 e2 |):real
[REL]       T∈{int,real}, op∈{>,<,==}  ⊢  (e1 e2 op):bool
[IF]        Γ⊢cond:bool, Γ⊢bloco:ok  ⊢  IF(cond,bloco):ok
[WHILE]     Γ⊢cond:bool, Γ⊢bloco:ok  ⊢  WHILE(cond,bloco):ok
[MEM-DEF]   Γ⊢v:T, Γ'=Γ[x↦T]  ⊢  (v x MEM):ok
[RES]       Γ⊢n:int  ⊢  (n RES):any
```

---

## 13. Estrutura do Repositório

```
rpn-compiler/
├── README.md                        ← Este arquivo
├── CONTRIBUTING.md                  ← Guia de commits e pull requests
├── AnalisadorSemantico.py           ← Compilador completo (todas as fases)
├── docs/
│   ├── gramatica_ebnf.md            ← Gramática EBNF com FIRST/FOLLOW
│   └── regras_semanticas.md         ← Regras semânticas em cálculo de sequentes
└── exemplos/
    ├── validos/
    │   ├── aritmetica_basica.txt
    │   ├── variaveis_mem.txt
    │   └── controle_fluxo.txt
    └── invalidos/
        ├── erro_variavel_nao_declarada.txt
        └── erro_tipo_divisao.txt
```

---

## ⚙️ Arquitetura do Compilador

```
Arquivo fonte (.txt)
        │
        ▼
┌───────────────────┐
│  Remoção de       │  *{ comentários }*  →  texto limpo
│  Comentários      │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Analisador       │  AFD → tokens      →  saida_lexica.txt
│  Léxico           │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Analisador       │  Parser LL(1)      →  arvore_cst.json
│  Sintático        │  Pilha semântica   →  arvore_ast.json
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Analisador       │  Inferência de tipos  →  arvore_atribuida.json
│  Semântico        │  Tabela de símbolos   →  tabela_simbolos.json
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Gerador de       │  ARMv7 + VFP          →  saida_assembly.s
│  Assembly         │
└───────────────────┘
```

---

*Grupo RA2_5 — Fase 3: Analisador Semântico + Geração de Assembly*
