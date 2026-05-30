# Gramática da Linguagem RPN — Documentação EBNF

## Notação utilizada

| Símbolo      | Significado                                          |
|--------------|------------------------------------------------------|
| `::=`        | Definição de regra                                   |
| `\|`         | Alternativa (ou)                                     |
| `{ X }`      | Zero ou mais repetições de X                         |
| `[ X ]`      | X é opcional (zero ou uma ocorrência)                |
| `'texto'`    | Terminal literal                                     |
| `MAIÚSCULO`  | Terminal simbólico (token)                           |
| `minúsculo`  | Não-terminal                                         |

---

## Gramática Completa em EBNF

```ebnf
(* ============================================================ *)
(*  ESTRUTURA DO PROGRAMA                                        *)
(* ============================================================ *)

programa
    ::= '(' START ')' laco_principal

laco_principal
    ::= '(' linha_ou_fim

linha_ou_fim
    ::= END ')'
      | conteudo_rpn ')' laco_principal


(* ============================================================ *)
(*  INSTRUCAO E CONTEUDO RPN                                     *)
(* ============================================================ *)

lista_instrucoes
    ::= instrucao { instrucao }

instrucao
    ::= '(' conteudo_rpn ')'

conteudo_rpn
    ::= valor elementos

elementos
    ::= COMMAND
      | valor acao_final
      | estrutura_controle

acao_final
    ::= operador [ estrutura_controle ]
      | estrutura_controle
      | COMMAND


(* ============================================================ *)
(*  ESTRUTURAS DE CONTROLE                                       *)
(* ============================================================ *)

estrutura_controle
    ::= bloco_codigo tipo_controle

tipo_controle
    ::= IF
      | WHILE

bloco_codigo
    ::= '{' lista_instrucoes '}'


(* ============================================================ *)
(*  VALORES, OPERADORES E COMANDOS                               *)
(* ============================================================ *)

valor
    ::= ID
      | NUM
      | instrucao

operador
    ::= '+'    (* adicao            *)
      | '-'    (* subtracao         *)
      | '*'    (* multiplicacao     *)
      | '^'    (* potenciacao       *)
      | '/'    (* divisao inteira   *)
      | '%'    (* modulo (resto)    *)
      | '|'    (* divisao real      *)
      | '>'    (* maior que         *)
      | '<'    (* menor que         *)
      | '=='   (* igual a           *)

COMMAND
    ::= RES
      | MEM


(* ============================================================ *)
(*  TOKENS TERMINAIS                                             *)
(* ============================================================ *)

NUM
    ::= inteiro
      | real
      | TRUE
      | FALSE

inteiro
    ::= [ '-' ] digito { digito }

real
    ::= [ '-' ] digito { digito } '.' digito { digito }

ID
    ::= ( letra | '_' ) { letra | digito | '_' }

letra
    ::= 'a' .. 'z' | 'A' .. 'Z'

digito
    ::= '0' .. '9'


(* ============================================================ *)
(*  COMENTARIOS (pre-processados antes da analise lexica)        *)
(* ============================================================ *)

comentario
    ::= '*{' qualquer_texto '}*'

qualquer_texto
    ::= { qualquer_caractere_exceto_fechamento }
```

---

## Conjuntos FIRST e FOLLOW

Os conjuntos abaixo são computados automaticamente pelo compilador e verificados no arquivo `relatorio_validacao_ll1.txt`.

### FIRST

| Não-terminal          | FIRST                                                    |
|-----------------------|----------------------------------------------------------|
| `programa`            | `{`(`}`                                                  |
| `laco_principal`      | `{`(`}`                                                  |
| `linha_ou_fim`        | `{END, ID, NUM, (, TRUE, FALSE}`                         |
| `lista_instrucoes`    | `{`(`}`                                                  |
| `continua_lista`      | `{(, EPSILON}`                                           |
| `instrucao`           | `{`(`}`                                                  |
| `conteudo_rpn`        | `{ID, NUM, (, TRUE, FALSE}`                              |
| `elementos`           | `{COMMAND, ID, NUM, (, TRUE, FALSE, {}`                  |
| `acao_final`          | `{+, -, *, \|, /, %, ^, >, <, ==, COMMAND, {}`          |
| `acao_pos_op`         | `{{, EPSILON}`                                           |
| `estrutura_controle`  | `{{}`                                                    |
| `tipo_controle`       | `{IF, WHILE}`                                            |
| `bloco_codigo`        | `{{}`                                                    |
| `valor`               | `{ID, NUM, (, TRUE, FALSE}`                              |
| `operador`            | `{+, -, *, \|, /, %, ^, >, <, ==}`                      |

### FOLLOW

| Não-terminal          | FOLLOW                                                   |
|-----------------------|----------------------------------------------------------|
| `programa`            | `{$}`                                                    |
| `laco_principal`      | `{$}`                                                    |
| `linha_ou_fim`        | `{$}`                                                    |
| `lista_instrucoes`    | `{}`}`                                                   |
| `continua_lista`      | `{}`}`                                                   |
| `instrucao`           | `{ID, NUM, (, TRUE, FALSE, +, -, *, \|, /, %, ^, >, <, ==, COMMAND, {, }, )}`|
| `conteudo_rpn`        | `{)}`                                                    |
| `elementos`           | `{)}`                                                    |
| `acao_final`          | `{)}`                                                    |
| `acao_pos_op`         | `{)}`                                                    |
| `estrutura_controle`  | `{), IF, WHILE}`                                         |
| `tipo_controle`       | `{)}`                                                    |
| `bloco_codigo`        | `{IF, WHILE}`                                            |
| `valor`               | `{+, -, *, \|, /, %, ^, >, <, ==, COMMAND, {, }, )}`    |
| `operador`            | `{{, )}`                                                 |

---

## Propriedade LL(1)

A gramática é **estritamente LL(1)**, verificada por:

1. **Ausência de conflitos FIRST/FIRST:** Para cada não-terminal, as produções alternativas têm conjuntos FIRST disjuntos.
2. **Ausência de conflitos FIRST/FOLLOW:** Para produções que derivam EPSILON, os conjuntos FIRST e FOLLOW correspondentes são disjuntos.
3. **Ausência de recursão à esquerda:** A gramática não possui recursão direta ou indireta à esquerda.

A verificação é executada automaticamente e o resultado é salvo em `relatorio_validacao_ll1.txt`.

---

## Diagrama de Precedência dos Operadores

> Em RPN, a precedência é determinada pela ordem de empilhamento — não há ambiguidade de precedência na gramática.

| Operador | Categoria        | Tipo de entrada | Tipo de saída |
|----------|------------------|-----------------|---------------|
| `+` `-` `*` `^` | Aritmético | int×int ou com real | int ou real |
| `/`       | Divisão inteira  | int×int         | int           |
| `%`       | Módulo           | int×int         | int           |
| `\|`      | Divisão real     | numérico×numérico | real        |
| `>` `<` `==` | Relacional  | numérico×numérico | bool        |
