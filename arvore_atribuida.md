# Árvore Sintática Atribuída

**Arquivo analisado:** `teste1.txt`

## Tabela de Símbolos

| Variável | Escopo | Tipo | Linha Def | Linhas Uso |
|----------|--------|------|-----------|------------|
| `A` | `global` | `int` | 9 | 15, 16, 17, 18, 19, 20, 24, 25, 26, 54 |
| `ALERTA` | `global` | `bool` | 43 | — |
| `ANTERIOR` | `global` | `any` | 52 | — |
| `B` | `global` | `int` | 10 | 15, 16, 17, 18, 19, 20, 24, 25, 54 |
| `CONTADOR` | `global` | `int` | 38 | 36, 38, 41 |
| `DESLIGADO` | `global` | `bool` | 29 | — |
| `DIV_INT` | `global` | `int` | 18 | — |
| `DIV_REAL` | `global` | `real` | 21 | — |
| `E_LOG` | `global` | `bool` | 30 | — |
| `GRANDE` | `global` | `bool` | 24 | — |
| `IGUAL` | `global` | `bool` | 26 | — |
| `LIGADO` | `global` | `bool` | 12 | 29, 30, 30, 31, 31 |
| `MOD_INT` | `global` | `int` | 19 | — |
| `MULT` | `global` | `int` | 17 | — |
| `OU_LOG` | `global` | `bool` | 31 | — |
| `PEQUENO` | `global` | `bool` | 25 | — |
| `POW` | `global` | `int` | 20 | — |
| `RAIO` | `global` | `real` | 11 | 21 |
| `RESULTADO_FINAL` | `global` | `int` | 54 | — |
| `SOMA` | `global` | `int` | 15 | — |
| `SUB` | `global` | `int` | 16 | — |

## Erros Semânticos

_Nenhum erro semântico detectado._

## Regras de Tipo (Cálculo de Sequentes)

> Consulte também o arquivo `sequentes.md` para a versão completa e detalhada.

> **Nota sobre inferência de tipos (Seção 2.3):** o sistema é estático e forte.
> O tipo de cada variável é determinado no momento de sua definição via `(V MEM)`.
> Usos posteriores em contexto incompatível geram erro semântico — não há
> redefinição implícita de tipo pelo contexto de uso.

```
[INT-LIT]   ⊢ n : int             (n literal inteiro)
[REAL-LIT]  ⊢ r : real            (r literal real)
[BOOL-LIT]  ⊢ b : bool            (b ∈ {TRUE, FALSE})

[VAR]       x:T ∈ Γ
            ────────
            Γ ⊢ x : T

[ARIT-INT]  Γ ⊢ e1:int, Γ ⊢ e2:int, op ∈ {+,-,*,^}  ⊢  (e1 e2 op) : int
[ARIT-REAL] Γ ⊢ e1:T1, Γ ⊢ e2:T2, op ∈ {+,-,*,^}, T1∨T2=real  ⊢  (e1 e2 op) : real
[DIV-INT]   Γ ⊢ e1:int, Γ ⊢ e2:int  ⊢  (e1 e2 /) : int
[MOD-INT]   Γ ⊢ e1:int, Γ ⊢ e2:int  ⊢  (e1 e2 %) : int
[DIV-REAL]  Γ ⊢ e1:T1, Γ ⊢ e2:T2, T1,T2 ∈ {int,real}  ⊢  (e1 e2 '|') : real
[REL-NUM]   Γ ⊢ e1:T, Γ ⊢ e2:T, T ∈ {int,real}, op ∈ {>,<}  ⊢  (e1 e2 op) : bool
[EQ]        Γ ⊢ e1:T, Γ ⊢ e2:T, T ∈ {int,real,bool}  ⊢  (e1 e2 ==) : bool
[AND]       Γ ⊢ e1:bool, Γ ⊢ e2:bool  ⊢  (e1 e2 AND) : bool
[OR]        Γ ⊢ e1:bool, Γ ⊢ e2:bool  ⊢  (e1 e2 OR)  : bool
[NOT]       Γ ⊢ e1:bool  ⊢  (e1 NOT) : bool   [unario]
[IF]        Γ ⊢ cond:bool, Γ ⊢ bloco:ok  ⊢  IF(cond,bloco) : ok
[WHILE]     Γ ⊢ cond:bool, Γ ⊢ bloco:ok  ⊢  WHILE(cond,bloco) : ok
[MEM-DEF]   Γ ⊢ v:T  ⊢  (v MEM):ok,  Γ'=Γ[MEM↦T]
[MEM-REDEF] Γ ⊢ v:T, MEM:T ∈ Γ  ⊢  (v MEM):ok  (reatribuição compatível)
[MEM-ERR]   Γ ⊢ v:T', MEM:T ∈ Γ, T'≠T  ⊢  ERRO SEMÂNTICO
[MEM-USO]   MEM:T ∈ Γ  ⊢  (MEM):T  — leitura via instrução (ID) na gramática
[RES]       Γ ⊢ n:int, n≥0  ⊢  (n RES):any
```

## Nós da Árvore Atribuída

```json
{
  "tipo": "programa_ast",
  "instrucoes": [
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "A",
        "tipo_dado": "int",
        "linha": 9
      },
      "val_expr": {
        "tipo": "numero",
        "valor": 20,
        "tipo_dado": "int",
        "linha": 9
      },
      "linha": 9,
      "tipo_dado": "int"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "B",
        "tipo_dado": "int",
        "linha": 10
      },
      "val_expr": {
        "tipo": "numero",
        "valor": 10,
        "tipo_dado": "int",
        "linha": 10
      },
      "linha": 10,
      "tipo_dado": "int"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "RAIO",
        "tipo_dado": "real",
        "linha": 11
      },
      "val_expr": {
        "tipo": "numero",
        "valor": 5.5,
        "tipo_dado": "real",
        "linha": 11
      },
      "linha": 11,
      "tipo_dado": "real"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "LIGADO",
        "tipo_dado": "bool",
        "linha": 12
      },
      "val_expr": {
        "tipo": "numero",
        "valor": true,
        "tipo_dado": "bool",
        "linha": 12
      },
      "linha": 12,
      "tipo_dado": "bool"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "SOMA",
        "tipo_dado": "int",
        "linha": 15
      },
      "val_expr": {
        "tipo": "operacao",
        "operador": "+",
        "esquerda": {
          "tipo": "variavel",
          "nome": "A",
          "tipo_dado": "int",
          "linha": 15
        },
        "direita": {
          "tipo": "variavel",
          "nome": "B",
          "tipo_dado": "int",
          "linha": 15
        },
        "linha": 15,
        "tipo_dado": "int"
      },
      "linha": 15,
      "tipo_dado": "int"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "SUB",
        "tipo_dado": "int",
        "linha": 16
      },
      "val_expr": {
        "tipo": "operacao",
        "operador": "-",
        "esquerda": {
          "tipo": "variavel",
          "nome": "A",
          "tipo_dado": "int",
          "linha": 16
        },
        "direita": {
          "tipo": "variavel",
          "nome": "B",
          "tipo_dado": "int",
          "linha": 16
        },
        "linha": 16,
        "tipo_dado": "int"
      },
      "linha": 16,
      "tipo_dado": "int"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "MULT",
        "tipo_dado": "int",
        "linha": 17
      },
      "val_expr": {
        "tipo": "operacao",
        "operador": "*",
        "esquerda": {
          "tipo": "variavel",
          "nome": "A",
          "tipo_dado": "int",
          "linha": 17
        },
        "direita": {
          "tipo": "variavel",
          "nome": "B",
          "tipo_dado": "int",
          "linha": 17
        },
        "linha": 17,
        "tipo_dado": "int"
      },
      "linha": 17,
      "tipo_dado": "int"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "DIV_INT",
        "tipo_dado": "int",
        "linha": 18
      },
      "val_expr": {
        "tipo": "operacao",
        "operador": "/",
        "esquerda": {
          "tipo": "variavel",
          "nome": "A",
          "tipo_dado": "int",
          "linha": 18
        },
        "direita": {
          "tipo": "variavel",
          "nome": "B",
          "tipo_dado": "int",
          "linha": 18
        },
        "linha": 18,
        "tipo_dado": "int"
      },
      "linha": 18,
      "tipo_dado": "int"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "MOD_INT",
        "tipo_dado": "int",
        "linha": 19
      },
      "val_expr": {
        "tipo": "operacao",
        "operador": "%",
        "esquerda": {
          "tipo": "variavel",
          "nome": "A",
          "tipo_dado": "int",
          "linha": 19
        },
        "direita": {
          "tipo": "variavel",
          "nome": "B",
          "tipo_dado": "int",
          "linha": 19
        },
        "linha": 19,
        "tipo_dado": "int"
      },
      "linha": 19,
      "tipo_dado": "int"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "POW",
        "tipo_dado": "int",
        "linha": 20
      },
      "val_expr": {
        "tipo": "operacao",
        "operador": "^",
        "esquerda": {
          "tipo": "variavel",
          "nome": "A",
          "tipo_dado": "int",
          "linha": 20
        },
        "direita": {
          "tipo": "variavel",
          "nome": "B",
          "tipo_dado": "int",
          "linha": 20
        },
        "linha": 20,
        "tipo_dado": "int"
      },
      "linha": 20,
      "tipo_dado": "int"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "DIV_REAL",
        "tipo_dado": "real",
        "linha": 21
      },
      "val_expr": {
        "tipo": "operacao",
        "operador": "|",
        "esquerda": {
          "tipo": "variavel",
          "nome": "RAIO",
          "tipo_dado": "real",
          "linha": 21
        },
        "direita": {
          "tipo": "numero",
          "valor": 2.0,
          "tipo_dado": "real",
          "linha": 21
        },
        "linha": 21,
        "tipo_dado": "real"
      },
      "linha": 21,
      "tipo_dado": "real"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "GRANDE",
        "tipo_dado": "bool",
        "linha": 24
      },
      "val_expr": {
        "tipo": "operacao",
        "operador": ">",
        "esquerda": {
          "tipo": "variavel",
          "nome": "A",
          "tipo_dado": "int",
          "linha": 24
        },
        "direita": {
          "tipo": "variavel",
          "nome": "B",
          "tipo_dado": "int",
          "linha": 24
        },
        "linha": 24,
        "tipo_dado": "bool"
      },
      "linha": 24,
      "tipo_dado": "bool"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "PEQUENO",
        "tipo_dado": "bool",
        "linha": 25
      },
      "val_expr": {
        "tipo": "operacao",
        "operador": "<",
        "esquerda": {
          "tipo": "variavel",
          "nome": "A",
          "tipo_dado": "int",
          "linha": 25
        },
        "direita": {
          "tipo": "variavel",
          "nome": "B",
          "tipo_dado": "int",
          "linha": 25
        },
        "linha": 25,
        "tipo_dado": "bool"
      },
      "linha": 25,
      "tipo_dado": "bool"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "IGUAL",
        "tipo_dado": "bool",
        "linha": 26
      },
      "val_expr": {
        "tipo": "operacao",
        "operador": "==",
        "esquerda": {
          "tipo": "variavel",
          "nome": "A",
          "tipo_dado": "int",
          "linha": 26
        },
        "direita": {
          "tipo": "numero",
          "valor": 20,
          "tipo_dado": "int",
          "linha": 26
        },
        "linha": 26,
        "tipo_dado": "bool"
      },
      "linha": 26,
      "tipo_dado": "bool"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "DESLIGADO",
        "tipo_dado": "bool",
        "linha": 29
      },
      "val_expr": {
        "tipo": "operacao",
        "operador": "NOT",
        "esquerda": {
          "tipo": "variavel",
          "nome": "LIGADO",
          "tipo_dado": "bool",
          "linha": 29
        },
        "direita": null,
        "linha": 29,
        "tipo_dado": "bool"
      },
      "linha": 29,
      "tipo_dado": "bool"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "E_LOG",
        "tipo_dado": "bool",
        "linha": 30
      },
      "val_expr": {
        "tipo": "operacao",
        "operador": "AND",
        "esquerda": {
          "tipo": "variavel",
          "nome": "LIGADO",
          "tipo_dado": "bool",
          "linha": 30
        },
        "direita": {
          "tipo": "variavel",
          "nome": "LIGADO",
          "tipo_dado": "bool",
          "linha": 30
        },
        "linha": 30,
        "tipo_dado": "bool"
      },
      "linha": 30,
      "tipo_dado": "bool"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "OU_LOG",
        "tipo_dado": "bool",
        "linha": 31
      },
      "val_expr": {
        "tipo": "operacao",
        "operador": "OR",
        "esquerda": {
          "tipo": "variavel",
          "nome": "LIGADO",
          "tipo_dado": "bool",
          "linha": 31
        },
        "direita": {
          "tipo": "variavel",
          "nome": "LIGADO",
          "tipo_dado": "bool",
          "linha": 31
        },
        "linha": 31,
        "tipo_dado": "bool"
      },
      "linha": 31,
      "tipo_dado": "bool"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "CONTADOR",
        "tipo_dado": "int",
        "linha": 34
      },
      "val_expr": {
        "tipo": "numero",
        "valor": 5,
        "tipo_dado": "int",
        "linha": 34
      },
      "linha": 34,
      "tipo_dado": "int"
    },
    {
      "tipo": "controle",
      "estrutura": "WHILE",
      "condicao": {
        "tipo": "operacao",
        "operador": ">",
        "esquerda": {
          "tipo": "variavel",
          "nome": "CONTADOR",
          "tipo_dado": "int",
          "linha": 36
        },
        "direita": {
          "tipo": "numero",
          "valor": 0,
          "tipo_dado": "int",
          "linha": 36
        },
        "linha": 36,
        "tipo_dado": "bool"
      },
      "bloco": {
        "tipo": "bloco",
        "instrucoes": [
          {
            "tipo": "comando",
            "comando": "MEM",
            "nome_var": {
              "tipo": "variavel",
              "nome": "CONTADOR",
              "tipo_dado": "int",
              "linha": 38
            },
            "val_expr": {
              "tipo": "operacao",
              "operador": "-",
              "esquerda": {
                "tipo": "variavel",
                "nome": "CONTADOR",
                "tipo_dado": "int",
                "linha": 38
              },
              "direita": {
                "tipo": "numero",
                "valor": 1,
                "tipo_dado": "int",
                "linha": 38
              },
              "linha": 38,
              "tipo_dado": "int"
            },
            "linha": 38,
            "tipo_dado": "int"
          },
          {
            "tipo": "controle",
            "estrutura": "IF",
            "condicao": {
              "tipo": "operacao",
              "operador": "==",
              "esquerda": {
                "tipo": "variavel",
                "nome": "CONTADOR",
                "tipo_dado": "int",
                "linha": 41
              },
              "direita": {
                "tipo": "numero",
                "valor": 2,
                "tipo_dado": "int",
                "linha": 41
              },
              "linha": 41,
              "tipo_dado": "bool"
            },
            "bloco": {
              "tipo": "bloco",
              "instrucoes": [
                {
                  "tipo": "comando",
                  "comando": "MEM",
                  "nome_var": {
                    "tipo": "variavel",
                    "nome": "ALERTA",
                    "tipo_dado": "bool",
                    "linha": 43
                  },
                  "val_expr": {
                    "tipo": "numero",
                    "valor": true,
                    "tipo_dado": "bool",
                    "linha": 43
                  },
                  "linha": 43,
                  "tipo_dado": "bool"
                }
              ],
              "tipo_dado": "ok"
            },
            "linha": 45,
            "tipo_dado": "ok"
          }
        ],
        "tipo_dado": "ok"
      },
      "linha": 48,
      "tipo_dado": "ok"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "ANTERIOR",
        "tipo_dado": "any",
        "linha": 52
      },
      "val_expr": {
        "tipo": "comando",
        "comando": "RES",
        "alvo": {
          "tipo": "numero",
          "valor": 1,
          "tipo_dado": "int",
          "linha": 52
        },
        "linha": 52,
        "tipo_dado": "any"
      },
      "linha": 52,
      "tipo_dado": "any"
    },
    {
      "tipo": "comando",
      "comando": "MEM",
      "nome_var": {
        "tipo": "variavel",
        "nome": "RESULTADO_FINAL",
        "tipo_dado": "int",
        "linha": 54
      },
      "val_expr": {
        "tipo": "operacao",
        "operador": "*",
        "esquerda": {
          "tipo": "variavel",
          "nome": "A",
          "tipo_dado": "int",
          "linha": 54
        },
        "direita": {
          "tipo": "variavel",
          "nome": "B",
          "tipo_dado": "int",
          "linha": 54
        },
        "linha": 54,
        "tipo_dado": "int"
      },
      "linha": 54,
      "tipo_dado": "int"
    }
  ],
  "tipo_dado": "ok"
}
```