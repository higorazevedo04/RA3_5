# Compilador RPN — Analisador Semântico + Geração de Assembly

> **Instituição:** [Nome da Instituição de Ensino]
> **Disciplina:** Compiladores / Construção de Compiladores
> **Ano:** 2025
> **Professor:** [Nome do Professor]
> **Grupo:** RA2_5 — Fase 3

---

## 👥 Integrantes do Grupo (Ordem Alfabética)

| Nome | RA |
|------|----|
| Higor Leonardo da Silva Azevedo | — |
| *(demais integrantes em ordem alfabética)* | — |

> Substitua os campos em branco com os dados reais do grupo.

---

## 📋 Sumário

1. [Descrição da Linguagem](#descrição-da-linguagem)
2. [Tipos Suportados](#tipos-suportados)
3. [Instruções para Compilar e Executar](#instruções-para-compilar-e-executar)
4. [Exemplos de Programas](#exemplos-de-programas)
5. [Tabela de Símbolos](#tabela-de-símbolos)
6. [Árvore Sintática Atribuída](#árvore-sintática-atribuída)
7. [Gramática em EBNF](#gramática-em-ebnf)
8. [Regras Semânticas em Cálculo de Sequentes](#regras-semânticas-em-cálculo-de-sequentes)

---

## Descrição da Linguagem

A linguagem implementada é uma linguagem imperativa de **notação polonesa reversa (RPN — Reverse Polish Notation)**, também chamada de notação pós-fixa. Nela, os operandos são escritos **antes** do operador, eliminando a necessidade de parênteses de precedência.

### Características

- **Paradigma:** Imperativo / procedural
- **Notação:** Pós-fixa (RPN)
- **Estrutura:** Todo programa está delimitado por `(START)` ... `(END)`
- **Instruções:** Cada instrução é delimitada por parênteses `( )`
- **Controle de fluxo:** `IF` e `WHILE`, com blocos entre `{ }`
- **Comentários:** Delimitados por `*{` e `}*`
- **Variáveis:** Declaradas implicitamente via comando `MEM`
- **Saída:** Via comando `RES`, que recupera resultados de instruções anteriores
- **Geração de código:** ARMv7 Assembly (CPulator / DE1-SoC com extensões VFP)

### Exemplo básico

```
(START)
(10 X MEM)          *{ armazena 10 em X }*
(X 5 +)             *{ soma X + 5 }*
(1 RES)             *{ exibe o resultado da instrução anterior }*
(END)
```

---

## Tipos Suportados

| Tipo   | Descrição                          | Exemplos de Literais       |
|--------|------------------------------------|----------------------------|
| `int`  | Inteiro com sinal                  | `42`, `-7`, `0`            |
| `real` | Ponto flutuante (64 bits)          | `3.14`, `-0.5`, `100.0`    |
| `bool` | Booleano lógico                    | `TRUE`, `FALSE`            |

### Regras de compatibilidade de tipos

| Operador | Operandos aceitos            | Resultado |
|----------|------------------------------|-----------|
| `+` `-` `*` `^` | `int` × `int`     | `int`     |
| `+` `-` `*` `^` | qualquer com `real` | `real`  |
| `/`      | `int` × `int` somente        | `int`     |
| `%`      | `int` × `int` somente        | `int`     |
| `\|`     | `int` ou `real` × `int` ou `real` | `real` |
| `>` `<` `==` | numéricos compatíveis    | `bool`    |
| `IF` / `WHILE` | condição deve ser `bool` | `ok`    |
| `RES`    | argumento deve ser `int`     | `any`     |
| `MEM`    | qualquer expressão           | tipo da expressão |

> **Nota:** O tipo `bool` **não pode** ser usado em operações aritméticas.

---

## Instruções para Compilar e Executar

### Pré-requisitos

- **Python 3.8+** instalado
- Sem dependências externas (usa apenas `json`, `os`, `sys`, `re` da biblioteca padrão)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/<usuario>/rpn-compiler.git
cd rpn-compiler
```

### Execução

```bash
# Compilar um arquivo fonte .txt
python AnalisadorSemantico.py exemplos/validos/exemplo1.txt
```

### Saídas geradas

| Arquivo                     | Descrição                                          |
|-----------------------------|----------------------------------------------------|
| `saida_lexica.txt`          | Tokens reconhecidos pelo analisador léxico         |
| `arvore_cst.json`           | Árvore de Derivação Concreta (CST) em JSON         |
| `arvore_ast.json`           | Árvore Sintática Abstrata (AST) em JSON            |
| `arvore_atribuida.json`     | AST com tipos inferidos                            |
| `arvore_atribuida.md`       | Relatório da AST atribuída em Markdown             |
| `tabela_simbolos.json`      | Tabela de símbolos em JSON                         |
| `tabela_simbolos.md`        | Tabela de símbolos em Markdown                     |
| `saida_assembly.s`          | Código Assembly ARMv7 gerado                       |
| `relatorio_validacao_ll1.txt` | Relatório dos conjuntos FIRST/FOLLOW e tabela LL(1) |

### Modo de testes

Execute sem argumentos para rodar a suíte de testes interna:

```bash
python AnalisadorSemantico.py
```

Isso executa automaticamente testes léxicos, sintáticos e semânticos, imprimindo `PASSOU` ou `FALHOU` para cada caso.

### Depuração

Para depurar passo a passo com o Python Debugger:

```bash
python -m pdb AnalisadorSemantico.py exemplos/validos/exemplo1.txt
```

Comandos úteis do `pdb`:

| Comando | Ação                        |
|---------|-----------------------------|
| `n`     | Próxima linha               |
| `s`     | Entrar na função            |
| `c`     | Continuar até o próximo breakpoint |
| `p <var>` | Imprimir variável         |
| `b <linha>` | Definir breakpoint      |
| `q`     | Sair                        |

#### Inspecionar a AST diretamente

```python
import json
with open("arvore_ast.json") as f:
    ast = json.load(f)
print(json.dumps(ast, indent=2, ensure_ascii=False))
```

#### Inspecionar a tabela de símbolos

```python
import json
with open("tabela_simbolos.json") as f:
    dados = json.load(f)

for nome, info in dados["tabela_simbolos"].items():
    print(f"{nome}: tipo={info['tipo']}, def_linha={info['linha_def']}, usos={info['linhas_uso']}")
```

---

## Exemplos de Programas

### ✅ Programas Válidos

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
(10 3 /)     *{ divisao inteira: resultado 3 }*
(10.0 4.0 |) *{ divisao real: resultado 2.5 }*
(END)
```

#### 3. Uso de variáveis com MEM

```
(START)
(42 X MEM)
(3.14 PI MEM)
(X PI *)
(END)
```

#### 4. Condicionais com IF

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

#### 7. Booleanos em controle

```
(START)
(TRUE { (1 2 +) } IF)
(FALSE { (1 RES) } IF)
(END)
```

#### 8. Potenciação e módulo

```
(START)
(2 10 ^)
(17 5 %)
(END)
```

#### 9. Uso de RES

```
(START)
(10 5 +)
(1 RES)
(END)
```

---

### ❌ Programas Inválidos

#### 1. Variável usada sem definição (erro semântico)

```
(START)
(X 1 +)    *{ ERRO: X nao foi definida com MEM }*
(END)
```
> **Erro:** `Variavel 'X' usada sem definicao previa com (V MEM).`

#### 2. Divisão inteira com reais (erro de tipo)

```
(START)
(3.5 2.0 /)   *{ ERRO: / requer inteiros }*
(END)
```
> **Erro:** `Operador '/' requer operandos inteiros. Recebeu 'real' e 'real'.`

#### 3. IF com condição não-booleana (erro de tipo)

```
(START)
(5 X MEM)
(X { (1 RES) } IF)   *{ ERRO: condicao deve ser bool }*
(END)
```
> **Erro:** `Condicao de 'IF' deve ter tipo 'bool', mas recebeu 'int'.`

#### 4. Operação aritmética com booleano (erro de tipo)

```
(START)
(TRUE 2 +)   *{ ERRO: bool nao pode ser operando de + }*
(END)
```
> **Erro:** `Operador '+' nao pode ser aplicado a tipo 'bool'.`

#### 5. Módulo com reais (erro de tipo)

```
(START)
(5.0 2.0 %)   *{ ERRO: % requer inteiros }*
(END)
```
> **Erro:** `Operador '%' requer operandos inteiros. Recebeu 'real' e 'real'.`

#### 6. Estrutura pré-fixa (erro sintático)

```
(START)
(+ 3 4)    *{ ERRO: notacao invalida — RPN exige operandos antes do operador }*
(END)
```
> **Erro:** Falha sintática — operador encontrado no início da instrução.

#### 7. Expressão vazia (erro sintático)

```
(START)
()         *{ ERRO: instrucao vazia }*
(END)
```
> **Erro:** Token inesperado `)` onde era esperado um valor.

#### 8. Caractere inválido no código-fonte (erro léxico)

```
(START)
(3 @ 4 +)   *{ ERRO: '@' nao pertence ao alfabeto }*
(END)
```
> **Erro:** `[ERRO LEXICO] Caractere invalido '@' na posicao 3`

#### 9. Comentário não fechado (erro léxico)

```
(START)
*{ comentario aberto sem fechamento
(1 2 +)
(END)
```
> **Erro:** `[ERRO LEXICO] Linha 2: Comentario nao fechado (falta '}*')`

#### 10. RES com argumento real (erro semântico)

```
(START)
(10 5 +)
(1.5 RES)   *{ ERRO: argumento de RES deve ser inteiro }*
(END)
```
> **Erro:** `O argumento de RES deve ser inteiro, mas recebeu 'real'.`

---

## Tabela de Símbolos

A **Tabela de Símbolos** é implementada pela classe `TabelaSimbolos` e tem como função rastrear todas as variáveis declaradas ao longo da compilação.

### Estrutura interna

Cada entrada na tabela é um dicionário com os seguintes campos:

```python
{
    "nome_variavel": {
        "tipo":       "int" | "real" | "bool" | None,
        "linha_def":  <número da instrução de definição>,
        "linhas_uso": [<lista de instruções onde foi usada>],
        "definida":   True | False
    }
}
```

### Operações disponíveis

| Método           | Descrição                                                         |
|------------------|-------------------------------------------------------------------|
| `definir(nome, tipo, linha)` | Registra ou atualiza uma variável. Retorna `False` em caso de redefinição incompatível. |
| `usar(nome, linha)` | Registra uso de variável. Retorna `False` se não declarada.   |
| `tipo_de(nome)`  | Retorna o tipo inferido da variável.                              |
| `esta_definida(nome)` | Verifica se a variável foi declarada com `MEM`.            |
| `para_dict()`    | Exporta a tabela inteira como dicionário Python.                  |

### Quando uma variável é registrada

- **Definição:** Ao encontrar o comando `MEM` — ex.: `(10 X MEM)` define `X` com tipo `int`.
- **Uso:** Ao aparecer como operando em qualquer expressão.
- **Erro:** Se usada antes de ser definida com `MEM`, um erro semântico fatal é emitido.

### Exemplo de saída (tabela_simbolos.md)

| Variável | Tipo  | Linha Definição | Linhas de Uso |
|----------|-------|-----------------|---------------|
| `X`      | `int` | 1               | 2, 3          |
| `PI`     | `real`| 2               | 3             |

### Redefinição

Redefinir uma variável com um tipo **diferente** e **incompatível** gera erro:

```
(10 X MEM)       → X : int
(3.14 X MEM)     → ERRO: Redefinicao incompativel de 'X': tipo anterior 'int', novo tipo 'real'
```

---

## Árvore Sintática Atribuída

A **Árvore Sintática Atribuída** (ou Annotated/Attributed Syntax Tree) é a AST com os tipos inferidos adicionados a cada nó após a análise semântica.

### Como é gerada

1. O **parser descendente recursivo** constrói a AST usando uma pilha semântica (`pilha_semantica`) durante a análise sintática.
2. Após o parsing, a função `construirTabelaSimbolos()` percorre a árvore para resolver declarações.
3. A função `verificarTipos()` chama `inferir_tipo_no()` recursivamente, preenchendo o campo `tipo_dado` de cada nó.

### Tipos de nós da AST

| Tipo de nó        | Campos principais                                           |
|-------------------|-------------------------------------------------------------|
| `programa_ast`    | `instrucoes: []`                                            |
| `numero`          | `valor`, `tipo_dado` (`int` / `real` / `bool`)             |
| `variavel`        | `nome`, `tipo_dado`                                         |
| `operacao`        | `operador`, `esquerda`, `direita`, `tipo_dado`              |
| `comando` (MEM)   | `val_expr`, `nome_var`, `tipo_dado`                         |
| `comando` (RES)   | `alvo`, `tipo_dado`                                         |
| `controle`        | `estrutura` (`IF`/`WHILE`), `condicao`, `bloco`, `tipo_dado`|
| `bloco`           | `instrucoes: []`, `tipo_dado`                               |

### Exemplo de nó atribuído

Instrução `(3 4 +)` resulta no nó:

```json
{
  "tipo": "operacao",
  "operador": "+",
  "esquerda": { "tipo": "numero", "valor": 3, "tipo_dado": "int" },
  "direita":  { "tipo": "numero", "valor": 4, "tipo_dado": "int" },
  "tipo_dado": "int"
}
```

### Arquivos gerados

- `arvore_ast.json` — AST pura (antes da atribuição de tipos)
- `arvore_atribuida.json` — AST com `tipo_dado` em cada nó
- `arvore_atribuida.md` — Relatório legível com tabela de símbolos, erros e regras de tipo

---

## Gramática em EBNF

```ebnf
programa          ::= '(' START ')' laco_principal

laco_principal    ::= '(' linha_ou_fim

linha_ou_fim      ::= END ')'
                    | conteudo_rpn ')' laco_principal

lista_instrucoes  ::= instrucao { instrucao }

instrucao         ::= '(' conteudo_rpn ')'

conteudo_rpn      ::= valor elementos

elementos         ::= COMMAND
                    | valor acao_final
                    | estrutura_controle

acao_final        ::= operador [ estrutura_controle ]
                    | estrutura_controle
                    | COMMAND

estrutura_controle ::= bloco_codigo tipo_controle

tipo_controle     ::= IF
                    | WHILE

bloco_codigo      ::= '{' lista_instrucoes '}'

valor             ::= ID
                    | NUM
                    | instrucao

operador          ::= '+' | '-' | '*' | '|' | '/' | '%' | '^' | '>' | '<' | '=='

COMMAND           ::= RES | MEM
NUM               ::= inteiro | real | TRUE | FALSE
ID                ::= letra { letra | dígito | '_' }
inteiro           ::= [ '-' ] dígito { dígito }
real              ::= [ '-' ] dígito { dígito } '.' dígito { dígito }
comentario        ::= '*{' qualquer_texto '}*'
```

### Terminais

| Terminal     | Descrição                                      |
|--------------|------------------------------------------------|
| `START`      | Palavra-chave de início do programa            |
| `END`        | Palavra-chave de fim do programa               |
| `IF`         | Estrutura condicional                          |
| `WHILE`      | Estrutura de repetição                         |
| `MEM`        | Comando de armazenamento em variável           |
| `RES`        | Comando de recuperação de resultado anterior   |
| `TRUE`/`FALSE` | Literais booleanos                          |
| `ID`         | Identificador de variável                      |
| `NUM`        | Literal numérico (inteiro ou real)             |

---

## Regras Semânticas em Cálculo de Sequentes

As regras de tipo formais da linguagem, escritas em notação de **cálculo de sequentes** (onde `Γ` representa o ambiente de tipos e `⊢` significa "tem tipo"):

```
─────────────────────
[INT-LIT]  ⊢ n : int          (n é literal inteiro)

─────────────────────
[REAL-LIT] ⊢ r : real         (r é literal real)

─────────────────────────────
[BOOL-LIT] ⊢ b : bool         (b ∈ {TRUE, FALSE})

        x : T ∈ Γ
─────────────────────
[VAR]       Γ ⊢ x : T

    Γ ⊢ e1 : int    Γ ⊢ e2 : int    op ∈ {+,-,*,^,%,/}
──────────────────────────────────────────────────────────
[ARIT-INT]      Γ ⊢ (e1 e2 op) : int

    Γ ⊢ e1 : T1    Γ ⊢ e2 : T2    op ∈ {+,-,*,^}    T1=real ∨ T2=real
──────────────────────────────────────────────────────────────────────────
[ARIT-REAL]         Γ ⊢ (e1 e2 op) : real

    Γ ⊢ e1 : int    Γ ⊢ e2 : int
──────────────────────────────────
[DIV-INT]    Γ ⊢ (e1 e2 /) : int

    Γ ⊢ e1 : int    Γ ⊢ e2 : int
──────────────────────────────────
[MOD-INT]    Γ ⊢ (e1 e2 %) : int

    Γ ⊢ e1 : T1    Γ ⊢ e2 : T2    T1 ∈ {int,real}    T2 ∈ {int,real}
──────────────────────────────────────────────────────────────────────
[DIV-REAL]              Γ ⊢ (e1 e2 |) : real

    Γ ⊢ e1 : T    Γ ⊢ e2 : T    T ∈ {int,real}    op ∈ {>,<,==}
──────────────────────────────────────────────────────────────────
[REL]                Γ ⊢ (e1 e2 op) : bool

    Γ ⊢ cond : bool    Γ ⊢ bloco : ok
────────────────────────────────────────
[IF]       Γ ⊢ IF(cond, bloco) : ok

    Γ ⊢ cond : bool    Γ ⊢ bloco : ok
────────────────────────────────────────
[WHILE]    Γ ⊢ WHILE(cond, bloco) : ok

    Γ ⊢ v : T            Γ' = Γ[x ↦ T]
────────────────────────────────────────────
[MEM-DEF]    Γ ⊢ (v x MEM) : ok,  Γ' ⊢ ...

        x : T ∈ Γ
─────────────────────
[MEM-USO]    Γ ⊢ x : T

    Γ ⊢ n : int
─────────────────────
[RES]    Γ ⊢ (n RES) : any
```

### Erros detectados pelas regras

| Regra violada | Mensagem de erro                                                      |
|---------------|-----------------------------------------------------------------------|
| `[VAR]` — x ∉ Γ | `Variavel 'x' usada sem definicao previa com (V MEM).`           |
| `[DIV-INT]` com real | `Operador '/' requer operandos inteiros. Recebeu 'real'.`  |
| `[MOD-INT]` com real | `Operador '%' requer operandos inteiros. Recebeu 'real'.`  |
| `[ARIT-*]` com bool | `Operador '+' nao pode ser aplicado a tipo 'bool'.`          |
| `[IF]` cond ≠ bool | `Condicao de 'IF' deve ter tipo 'bool', mas recebeu 'int'.`   |
| `[WHILE]` cond ≠ bool | `Condicao de 'WHILE' deve ter tipo 'bool', mas recebeu 'int'.` |
| `[RES]` arg ≠ int | `O argumento de RES deve ser inteiro, mas recebeu 'real'.`    |
| `[MEM-DEF]` redefinição | `Redefinicao incompativel de 'x': tipo anterior 'int', novo tipo 'real'.` |

---

## 🗂️ Estrutura do Repositório

```
rpn-compiler/
├── README.md
├── AnalisadorSemantico.py       ← Código principal (léxico + sintático + semântico + assembly)
├── docs/
│   ├── gramatica_ebnf.md        ← Gramática formal em EBNF
│   └── regras_semanticas.md     ← Regras em cálculo de sequentes
├── exemplos/
│   ├── validos/
│   │   ├── exemplo1.txt
│   │   ├── exemplo2.txt
│   │   └── ...
│   └── invalidos/
│       ├── erro_tipo.txt
│       ├── erro_sintatico.txt
│       └── ...
└── src/                         ← (Fases anteriores, se separadas)
```

---

## 📌 Convenções de Commits e Pull Requests

### Mensagens de commit

Use o padrão `tipo(escopo): mensagem`:

| Tipo       | Uso                                               |
|------------|---------------------------------------------------|
| `feat`     | Nova funcionalidade                               |
| `fix`      | Correção de bug                                   |
| `docs`     | Atualização de documentação                       |
| `test`     | Adição ou modificação de testes                   |
| `refactor` | Refatoração sem mudança de comportamento          |
| `chore`    | Tarefas de manutenção (CI, formatação, etc.)      |

**Exemplos:**
```
feat(semantico): adiciona verificacao de tipos para operador %
fix(lexico): corrige tratamento de numero negativo no AFD
docs(readme): adiciona exemplos de programas invalidos
test(semantico): adiciona casos de teste para WHILE com variavel nao declarada
```

### Pull Requests

- **Título:** Descritivo e no mesmo padrão dos commits
- **Descrição:** O que foi feito, por que e como testar
- **Branch:** `feature/<nome>`, `fix/<nome>` ou `docs/<nome>`
- **Revisão:** Ao menos um integrante deve aprovar antes do merge
- **Squash merge** preferido para manter o histórico limpo

---

## ⚙️ Arquitetura do Compilador

```
Arquivo fonte (.txt)
        │
        ▼
┌───────────────────┐
│  Remoção de       │  *{ comentários }*
│  Comentários      │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Analisador       │  AFD → tokens
│  Léxico           │  saida_lexica.txt
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Analisador       │  Parser LL(1) descendente recursivo
│  Sintático        │  arvore_cst.json / arvore_ast.json
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Analisador       │  Inferência de tipos + tabela de símbolos
│  Semântico        │  tabela_simbolos.json / arvore_atribuida.json
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Gerador de       │  ARMv7 + VFP (CPulator DE1-SoC)
│  Assembly         │  saida_assembly.s
└───────────────────┘
```

---

*Documentação gerada com base no código-fonte da Fase 3 — Analisador Semântico + Geração de Assembly.*
