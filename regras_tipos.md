# Sistema de Regras de Validação de Tipos — Cálculo de Sequentes

> **Tipos suportados:** `int`, `real`, `bool`  
> **Sistema de tipos:** estático e forte (Seção 2.3 da especificação)  
> **Ambiente de tipos:** Γ (contexto) mapeia nomes de variáveis para tipos

---

## 1. Regras para Literais

```
                          ⊢ n : int
[INT-LIT]  ─────────────────────────────────
           n é um literal inteiro (ex: 3, -7, 0)

                          ⊢ r : real
[REAL-LIT] ─────────────────────────────────
           r é um literal de ponto flutuante (ex: 3.14, -0.5)

                          ⊢ b : bool
[BOOL-LIT] ─────────────────────────────────
           b ∈ { TRUE, FALSE }
```

---

## 2. Regra para Variáveis

```
           x : T ∈ Γ
[VAR]      ──────────
           Γ ⊢ x : T

  Nota: variável deve estar definida em Γ antes do uso.
  Uso de variável não declarada é ERRO SEMÂNTICO FATAL.
```

---

## 3. Regras para Operadores Aritméticos

```
           Γ ⊢ e1 : int    Γ ⊢ e2 : int    op ∈ {+, -, *, ^}
[ARIT-INT] ────────────────────────────────────────────────────
           Γ ⊢ (e1 e2 op) : int

           Γ ⊢ e1 : T1    Γ ⊢ e2 : T2
           op ∈ {+, -, *, ^}    T1 ∈ {int, real}    T2 ∈ {int, real}
           T1 = real  ∨  T2 = real
[ARIT-REAL]────────────────────────────────────────────────────
           Γ ⊢ (e1 e2 op) : real

           Γ ⊢ e1 : int    Γ ⊢ e2 : int
[DIV-INT]  ──────────────────────────────
           Γ ⊢ (e1 e2 /) : int
  (divisão inteira — operandos DEVEM ser int)

           Γ ⊢ e1 : int    Γ ⊢ e2 : int
[MOD-INT]  ──────────────────────────────
           Γ ⊢ (e1 e2 %) : int
  (resto inteiro — operandos DEVEM ser int)

           Γ ⊢ e1 : T1    Γ ⊢ e2 : T2
           T1 ∈ {int, real}    T2 ∈ {int, real}
[DIV-REAL] ──────────────────────────────
           Γ ⊢ (e1 e2 '|') : real
  (divisão real — aceita int ou real, resultado sempre real)
```

---

## 4. Regras para Operadores Relacionais

```
           Γ ⊢ e1 : T    Γ ⊢ e2 : T
           T ∈ {int, real}    op ∈ {>, <}
[REL-NUM]  ──────────────────────────────
           Γ ⊢ (e1 e2 op) : bool

  Restrição: bool NÃO pode ser operando de > ou <.

           Γ ⊢ e1 : T    Γ ⊢ e2 : T
           T ∈ {int, real, bool}    op = ==
[EQ]       ──────────────────────────────
           Γ ⊢ (e1 e2 ==) : bool

  Operador == aceita int, real ou bool, desde que ambos os lados
  sejam do mesmo tipo (ou ambos numéricos). bool == bool é VÁLIDO.
```

---

## 4b. Regras para Operadores Lógicos

```
           Γ ⊢ e1 : bool    Γ ⊢ e2 : bool
[AND]      ──────────────────────────────────
           Γ ⊢ (e1 e2 AND) : bool

  Conjunção lógica. Ambos os operandos DEVEM ser bool.

           Γ ⊢ e1 : bool    Γ ⊢ e2 : bool
[OR]       ──────────────────────────────────
           Γ ⊢ (e1 e2 OR) : bool

  Disjunção lógica. Ambos os operandos DEVEM ser bool.

           Γ ⊢ e1 : bool
[NOT]      ──────────────────────────────────
           Γ ⊢ (e1 NOT) : bool

  Negação lógica. Operador UNÁRIO: usa apenas o topo da pilha.
  O operando DEVE ser bool.
```

---

## 5. Regras para Estruturas de Controle

```
           Γ ⊢ cond : bool    Γ ⊢ bloco : ok
[IF]       ───────────────────────────────────
           Γ ⊢ IF(cond, bloco) : ok

  Restrição: a condição de IF DEVE ter tipo bool.

           Γ ⊢ cond : bool    Γ ⊢ bloco : ok
[WHILE]    ───────────────────────────────────
           Γ ⊢ WHILE(cond, bloco) : ok

  Restrição: a condição de WHILE DEVE ter tipo bool.
```

---

## 6. Regras para Comandos Especiais

```
           Γ ⊢ v : T    MEM ∉ Γ
[MEM-DEF]  ──────────────────────────────────────────
           Γ ⊢ (v MEM) : ok,    Γ' = Γ ∪ { MEM : T }

  Define variável MEM com tipo T. Após a definição, MEM
  fica disponível em Γ para usos subsequentes.

           Γ ⊢ v : T    MEM : T ∈ Γ
[MEM-REDEF]──────────────────────────────────────────
           Γ ⊢ (v MEM) : ok    (reatribuição compatível)

           Γ ⊢ v : T'    MEM : T ∈ Γ    T' ≠ T
[MEM-ERR]  ──────────────────────────────────────────
           ERRO SEMÂNTICO: redefinição incompatível de tipo

           MEM : T ∈ Γ
[MEM-USO]  ────────────
           Γ ⊢ (MEM) : T

           Γ ⊢ n : int    n ≥ 0
[RES]      ──────────────────────
           Γ ⊢ (n RES) : any

  N deve ser inteiro não negativo. Retorna o resultado da
  expressão N linhas anteriores (array_res[ptr_res - N]).
```

---

## 7. Inferência de Tipos e Sistema Estático/Forte

O sistema de tipos da linguagem é **estático e forte** (Seção 2.3):

- O tipo de uma variável é determinado no **momento de sua definição** via `(V MEM)`, onde o tipo de `V` define o tipo da variável `MEM`.
- Uma vez tipada, a variável **não pode ser redefinida** com tipo incompatível — qualquer tentativa gera erro semântico (`[MEM-ERR]`).
- O uso de uma variável antes de sua definição é **erro semântico fatal**.
- Operações entre `bool` e `int`/`real` são **proibidas**.
- Divisão inteira `/` e resto `%` exigem operandos `int`.
- Divisão real `'|'` aceita `int` ou `real`, produzindo sempre `real`.
- Condições de `IF` e `WHILE` **devem** ter tipo `bool`.
- Operadores `AND` e `OR` exigem ambos os operandos `bool`.
- Operador `NOT` é **unário** e exige operando `bool`.
- Operador `==` aceita `bool == bool` além de numéricos.

```
Tabela de compatibilidade de operadores:

  Operador  | Tipos aceitos (e1, e2)           | Tipo resultado
  --------- | -------------------------------- | --------------
  +, -, *,^ | (int, int)                       | int
  +, -, *,^ | (real, real) ou (int,real)       | real
  /         | (int, int)                       | int
  %         | (int, int)                       | int
  '|'       | (int,int),(real,real),(int,real),(real,int) | real
  >, <      | (int, int) ou (real, real)       | bool
  ==        | (int,int),(real,real),(bool,bool) | bool
  AND, OR   | (bool, bool)                     | bool
  NOT       | (bool)  [unario]                 | bool
  IF/WHILE  | (bool, bloco)                    | ok
```

---

## 8. Nota sobre `(MEM)` como Leitura de Variável (Seção 2.1)

A especificação define dois usos distintos para variáveis:

- `(V MEM)` — **definição/atribuição**: armazena o valor `V` na variável `MEM`.
- `(MEM)` — **leitura**: retorna o valor armazenado em `MEM`.

Na gramática, a forma `(MEM)` (leitura) é implementada como `(ID)` onde `ID`
é o nome da variável (ex: `(X)`, `(CONTADOR)`, `(VAR)`). Isso é correto porque
o nome de uma variável é sempre um conjunto de letras latinas maiúsculas,
portanto categorizado como `ID` (não como `COMMAND`).

A produção `conteudo_rpn ::= valor elementos` com `elementos ::= epsilon`
permite exatamente a construção `(NOME_VAR)` — um único valor `ID` sem
elementos adicionais. A regra semântica `[MEM-USO]` se aplica a esse caso.
