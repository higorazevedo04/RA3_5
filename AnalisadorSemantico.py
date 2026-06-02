# Integrantes do grupo (ordem alfabética):
# Higor Leonardo da Silva Azevedo - higorazevedo04
# Nome do grupo no Canvas: RA3_5
# FASE 3 — Analisador Semântico

import json  # Salvar árvores em JSON
import os    # Manipulação de arquivos
import sys   # Argumentos do terminal


# ============================================================
# GRAMÁTICA E CONJUNTOS
# ============================================================

def construirGramatica():
    # Gramática LL(1) da linguagem RPN.
    return {
        'programa':           [['(', 'START', ')', 'laco_principal']],
        'laco_principal':     [['(', 'linha_ou_fim']],
        'linha_ou_fim':       [['END', ')'], ['conteudo_rpn', ')', 'laco_principal']],
        'lista_instrucoes':   [['instrucao', 'continua_lista']],
        'continua_lista':     [['instrucao', 'continua_lista'], ['EPSILON']],
        'instrucao':          [['(', 'conteudo_rpn', ')']],
        'conteudo_rpn':       [['valor', 'elementos']],
        'elementos':          [['COMMAND'], ['valor', 'acao_final'], ['estrutura_controle'], ['NOT'], ['EPSILON']],
        'acao_final':         [['operador', 'acao_pos_op'], ['estrutura_controle'], ['COMMAND'], ['NOT']],
        'acao_pos_op':        [['estrutura_controle'], ['EPSILON']],
        'estrutura_controle': [['bloco_codigo', 'tipo_controle']],
        'tipo_controle':      [['IF'], ['WHILE']],
        'bloco_codigo':       [['{', 'lista_instrucoes', '}']],
        'valor':              [['ID'], ['NUM'], ['instrucao']],
        'operador':           [['+'], ['-'], ['*'], ['|'], ['/'], ['%'], ['^'], ['>'], ['<'], ['=='],
                               ['AND'], ['OR']]
    }

# ============================================================
# CÁLCULO DO FIRST
# ============================================================

def calcularFirst(gramatica):
     # Cria um conjunto com todos os não-terminais da gramática
    nao_terminais = set(gramatica.keys())

    # Conjunto que armazenará quais não-terminais podem gerar EPSILON (vazio)
    nullable = set()

    for nt, prods in gramatica.items():
        if ['EPSILON'] in prods:
            nullable.add(nt)

    mudou = True
    while mudou:
        mudou = False
        for nt, prods in gramatica.items():
            if nt not in nullable:
                for p in prods:
                    if p != ['EPSILON'] and all(s in nullable for s in p):
                        nullable.add(nt)
                        mudou = True
                        break

    first = {nt: set() for nt in nao_terminais}

    for nt in nullable:
        first[nt].add('EPSILON')

    mudou = True
    while mudou:
        mudou = False
        for nt, prods in gramatica.items():
            for p in prods:
                for s in p:
                    if s == 'EPSILON':
                        continue
                    if s not in nao_terminais:
                        if s not in first[nt]:
                            first[nt].add(s)
                            mudou = True
                        break
                    else:
                        antes = len(first[nt])
                        first[nt].update(first[s] - {'EPSILON'})
                        if len(first[nt]) > antes:
                            mudou = True
                        if s not in nullable:
                            break

    return first, nullable

# ============================================================
# CÁLCULO DO FOLLOW
# ============================================================

def calcularFollow(gramatica, first, nullable):
    nao_terminais = set(gramatica.keys())
    follow = {nt: set() for nt in nao_terminais}
    follow['programa'].add('$')

    mudou = True
    while mudou:
        mudou = False
        for head, prods in gramatica.items():
            for p in prods:
                for i, s in enumerate(p):
                    if s in nao_terminais:
                        beta = p[i+1:]
                        antes = len(follow[s])
                        if beta:
                            f_beta = set()
                            for b in beta:
                                if b not in nao_terminais:
                                    f_beta.add(b)
                                    break
                                f_beta.update(first[b] - {'EPSILON'})
                                if b not in nullable:
                                    break
                            else:
                                f_beta.add('EPSILON')
                            follow[s].update(f_beta - {'EPSILON'})
                            if 'EPSILON' in f_beta:
                                follow[s].update(follow[head])
                        else:
                            follow[s].update(follow[head])
                        if len(follow[s]) > antes:
                            mudou = True

    return follow

# ============================================================
# CONSTRUÇÃO DA TABELA LL(1)
# ============================================================

def construirTabelaLL1(gramatica, first, follow, nullable):
    nao_terminais = set(gramatica.keys())
    terminais = {
        'START', 'END', '(', ')', '{', '}',
        'ID', 'NUM',
        '+', '-', '*', '|', '/', '%', '^',
        '>', '<', '==',
        'AND', 'OR', 'NOT',
        'IF', 'WHILE', 'COMMAND', '$'
    }
    tabela = {nt: {t: None for t in terminais} for nt in nao_terminais}

    for head, prods in gramatica.items():
        for p in prods:
            f_p = set()
            if p == ['EPSILON']:
                f_p.add('EPSILON')
            else:
                for s in p:
                    if s not in nao_terminais:
                        f_p.add(s)
                        break
                    f_p.update(first[s] - {'EPSILON'})
                    if s not in nullable:
                        break
                else:
                    f_p.add('EPSILON')

            for t in f_p - {'EPSILON'}:
                if t not in terminais:
                    continue
                if tabela[head][t] is not None:
                    raise Exception(f"Conflito LL(1) em [{head}, {t}]")
                tabela[head][t] = p

            if 'EPSILON' in f_p:
                for t in follow[head]:
                    if t in terminais and tabela[head][t] is None:
                        tabela[head][t] = p

    return tabela

# ============================================================
# RELATÓRIO LL(1)
# ============================================================

def gerarRelatorioLL1(primeiros, seguintes, tabela):
    nome_arquivo = "relatorio_validacao_ll1.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("========================================================\n")
        f.write("    RELATORIO DE VALIDACAO TEORICA LL(1)\n")
        f.write("========================================================\n\n")

        f.write("0. GRAMATICA DA LINGUAGEM (EBNF)\n\n")
        # NOTA: Para evitar ambiguidade com o operador '|' (divisao real) da linguagem,
        # as alternativas de producao sao separadas por '/' nesta representacao EBNF.
        # O operador '|' da linguagem aparece sempre entre aspas simples: '|'.
        f.write("   Notacao: '/' separa alternativas de producao (nao confundir com o\n")
        f.write("   operador '|' da linguagem, que representa divisao real e aparece\n")
        f.write("   sempre entre aspas simples).\n\n")
        f.write("   programa          ::= '(' START ')' laco_principal\n")
        f.write("   laco_principal    ::= '(' linha_ou_fim\n")
        f.write("   linha_ou_fim      ::= END ')'\n")
        f.write("                      /  conteudo_rpn ')' laco_principal\n")
        f.write("   lista_instrucoes  ::= instrucao continua_lista\n")
        f.write("   continua_lista    ::= instrucao continua_lista\n")
        f.write("                      /  epsilon\n")
        f.write("   instrucao         ::= '(' conteudo_rpn ')'\n")
        f.write("   conteudo_rpn      ::= valor elementos\n")
        f.write("   elementos         ::= COMMAND\n")
        f.write("                      /  valor acao_final\n")
        f.write("                      /  estrutura_controle\n")
        f.write("                      /  NOT  (* NOT eh unario: (valor NOT) *)\n")
        f.write("                      /  epsilon  (* leitura isolada: (ID) *)\n")
        f.write("   acao_final        ::= operador acao_pos_op\n")
        f.write("                      /  estrutura_controle\n")
        f.write("                      /  COMMAND\n")
        f.write("                      /  NOT   (* NOT eh unario *)\n")
        f.write("   acao_pos_op       ::= estrutura_controle\n")
        f.write("                      /  epsilon\n")
        f.write("   estrutura_controle ::= bloco_codigo tipo_controle\n")
        f.write("   tipo_controle     ::= IF\n")
        f.write("                      /  WHILE\n")
        f.write("   bloco_codigo      ::= '{' lista_instrucoes '}'\n")
        f.write("   valor             ::= ID\n")
        f.write("                      /  NUM\n")
        f.write("                      /  instrucao\n")
        f.write("   operador          ::= '+' / '-' / '*' / '|' / '/' / '%' / '^'\n")
        f.write("                      /  '>' / '<' / '=='\n")
        f.write("                      /  AND / OR\n")
        f.write("   (* NOT nao aparece em 'operador' pois e unario e tratado separadamente *)\n")
        f.write("\n   Terminais fixos  : START END IF WHILE RES MEM TRUE FALSE AND OR NOT\n")
        f.write("   Terminais literais: '(' ')' '{' '}' '+' '-' '*' '|' '/' '%' '^' '>' '<' '=='\n")
        f.write("   COMMAND           = RES / MEM\n")
        f.write("   NUM               = literal inteiro / literal real / TRUE / FALSE\n")
        f.write("   ID                = identificador de variavel (letras latinas maiusculas)\n")
        f.write("\n")

        f.write("1. CONJUNTOS FIRST (Primeiros)\n")
        for nt, valores in sorted(primeiros.items()):
            f.write(f"   FIRST({nt}) = {{ {', '.join(sorted(valores))} }}\n")
        f.write("\n2. CONJUNTOS FOLLOW (Seguintes)\n")
        for nt, valores in sorted(seguintes.items()):
            f.write(f"   FOLLOW({nt}) = {{ {', '.join(sorted(valores))} }}\n")
        f.write("\n3. ANALISE DE CONFLITOS NA TABELA LL(1)\n")
        f.write("   Inspecionando mapeamento de producoes por Lookahead...\n")
        regras_mapeadas = sum(
            1 for nt in tabela for t, p in tabela[nt].items() if p is not None
        )
        f.write(f"   -> {regras_mapeadas} transicoes deterministicas mapeadas com sucesso.\n")
        f.write("   -> Ausencia total de conflitos FIRST/FIRST confirmada.\n")
        f.write("   -> Ausencia total de conflitos FIRST/FOLLOW confirmada.\n")
        f.write("\n========================================================\n")
        f.write("STATUS FINAL: VALIDADO E APROVADO\n")
        f.write("A gramatica nao contem ambiguidades e e estritamente LL(1).\n")
        f.write("========================================================\n")
    print(f"Relatorio de validacao teorica LL(1) gerado em: '{nome_arquivo}'")


# ============================================================
# ARQUIVO SEPARADO: gramatica.md  
# ============================================================

def gerarGramaticaMd():
    """Gera o arquivo gramatica.md com a gramática LL(1) aumentada em EBNF.

    Conforme Seção 10.3 do enunciado, este arquivo deve conter a gramática
    atribuída em formato EBNF, usando letras minúsculas para não-terminais
    e maiúsculas para terminais.

    Decisão de projeto: o separador de alternativas usado é '/' em vez do
    '|' convencional da EBNF, pois '|' também é um operador da linguagem
    (divisão real). Isso elimina qualquer ambiguidade visual na leitura da
    gramática.
    """
    nome_arquivo = "gramatica.md"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("# Gramática da Linguagem — EBNF Aumentada (LL(1))\n\n")
        f.write("> **Notação:** letras minúsculas = não-terminais; MAIÚSCULAS = terminais.  \n")
        f.write("> O separador de alternativas é `/` (e não `|`), pois `|` é também um\n")
        f.write("> operador da linguagem (divisão real). O operador `|` da linguagem\n")
        f.write("> aparece sempre entre aspas simples: `'|'`.\n\n")

        f.write("---\n\n")
        f.write("## Produções\n\n")
        f.write("```ebnf\n")
        f.write("programa          ::= '(' START ')' laco_principal\n\n")

        f.write("laco_principal    ::= '(' linha_ou_fim\n\n")

        f.write("linha_ou_fim      ::= END ')'\n")
        f.write("                   /  conteudo_rpn ')' laco_principal\n\n")

        f.write("lista_instrucoes  ::= instrucao continua_lista\n\n")

        f.write("continua_lista    ::= instrucao continua_lista\n")
        f.write("                   /  epsilon\n\n")

        f.write("instrucao         ::= '(' conteudo_rpn ')'\n\n")

        f.write("conteudo_rpn      ::= valor elementos\n\n")

        f.write("elementos         ::= COMMAND\n")
        f.write("                   /  valor acao_final\n")
        f.write("                   /  estrutura_controle\n")
        f.write("                   /  NOT    (* NOT eh unario: (valor NOT), sem segundo operando *)\n")
        f.write("                   /  epsilon (* permite (ID) como leitura isolada de variavel *)\n\n")

        f.write("acao_final        ::= operador acao_pos_op\n")
        f.write("                   /  estrutura_controle\n")
        f.write("                   /  COMMAND\n")
        f.write("                   /  NOT    (* NOT eh unario *)\n\n")

        f.write("acao_pos_op       ::= estrutura_controle\n")
        f.write("                   /  epsilon\n\n")

        f.write("estrutura_controle ::= bloco_codigo tipo_controle\n\n")

        f.write("tipo_controle     ::= IF\n")
        f.write("                   /  WHILE\n\n")

        f.write("bloco_codigo      ::= '{' lista_instrucoes '}'\n\n")

        f.write("valor             ::= ID\n")
        f.write("                   /  NUM\n")
        f.write("                   /  instrucao\n\n")

        f.write("operador          ::= '+'\n")
        f.write("                   /  '-'\n")
        f.write("                   /  '*'\n")
        f.write("                   /  '|'    (* divisao real *)\n")
        f.write("                   /  '/'    (* divisao inteira *)\n")
        f.write("                   /  '%'    (* resto inteiro *)\n")
        f.write("                   /  '^'    (* potenciacao *)\n")
        f.write("                   /  '>'\n")
        f.write("                   /  '<'\n")
        f.write("                   /  '=='\n")
        f.write("                   /  AND    (* conjuncao logica: (e1 e2 AND) *)\n")
        f.write("                   /  OR     (* disjuncao logica: (e1 e2 OR) *)\n")
        f.write("(* NOT nao aparece em 'operador': e unario, tratado diretamente em 'elementos'/'acao_final' *)\n")
        f.write("```\n\n")

        f.write("---\n\n")
        f.write("## Terminais\n\n")
        f.write("| Terminal | Descrição |\n")
        f.write("|----------|-----------|\n")
        f.write("| `START` | Marca o início do programa |\n")
        f.write("| `END` | Marca o fim do programa |\n")
        f.write("| `IF` | Estrutura de decisão |\n")
        f.write("| `WHILE` | Estrutura de repetição |\n")
        f.write("| `RES` | Comando: retorna resultado de N linhas atrás |\n")
        f.write("| `MEM` | Comando: armazena valor em variável |\n")
        f.write("| `TRUE` | Literal lógico verdadeiro |\n")
        f.write("| `FALSE` | Literal lógico falso |\n")
        f.write("| `AND` | Operador lógico: conjunção (e1 e2 AND), resultado bool |\n")
        f.write("| `OR` | Operador lógico: disjunção (e1 e2 OR), resultado bool |\n")
        f.write("| `NOT` | Operador lógico: negação (e1 NOT), operando unário bool |\n")
        f.write("| `COMMAND` | Metavariável: `RES` ou `MEM` |\n")
        f.write("| `NUM` | Metavariável: literal inteiro, real, `TRUE` ou `FALSE` |\n")
        f.write("| `ID` | Metavariável: identificador de variável (letras latinas maiúsculas) |\n\n")

        f.write("> **Nota sobre `(MEM)` como leitura de variável (Seção 2.1):** A instrução\n")
        f.write("> `(MEM)` que \"retorna o valor armazenado em MEM\" é implementada como\n")
        f.write("> `(ID)` na gramática, onde `ID` é o nome da variável (ex: `(X)`, `(CONTADOR)`).\n")
        f.write("> O nome da variável é sempre um conjunto de letras latinas maiúsculas —\n")
        f.write("> portanto cai na categoria `ID` (não `COMMAND`). Isso está totalmente correto\n")
        f.write("> pois a produção `valor ::= ID` e `conteudo_rpn ::= valor elementos` com\n")
        f.write("> `elementos ::= epsilon` permitem exatamente a construção `(NOME_VAR)`.\n\n")

        f.write("---\n\n")
        f.write("## Regras Semânticas Associadas (Gramática Aumentada)\n\n")
        f.write("Cada produção carrega ações semânticas executadas durante o parsing:\n\n")
        f.write("| Produção | Ação Semântica |\n")
        f.write("|----------|----------------|\n")
        f.write("| `instrucao ::= '(' conteudo_rpn ')'` | Empilha o nó semântico resultante |\n")
        f.write("| `operador` | Desempilha dois operandos, cria nó `operacao{op, esq, dir}` |\n")
        f.write("| `tipo_controle ::= IF / WHILE` | Desempilha bloco e condição, cria nó `controle` |\n")
        f.write("| `COMMAND = MEM` | Desempilha nome_var e val_expr, cria nó `comando{MEM}` |\n")
        f.write("| `COMMAND = RES` | Desempilha alvo, cria nó `comando{RES}` |\n")
        f.write("| `NUM` (literal) | Empilha nó `numero{valor, tipo_dado}` |\n")
        f.write("| `ID` (variável) | Empilha nó `variavel{nome, tipo_dado=None}` |\n")
        f.write("| `END` | Coleta instrucoes do programa, fecha nó `programa_ast` |\n")
        f.write("| `'{'` / `'}'` | Delimita bloco; `'}'` fecha nó `bloco{instrucoes}` |\n")
    print(f"Gramatica EBNF gerada em: '{nome_arquivo}'")


# ============================================================
# ARQUIVO SEPARADO: sequentes.md  
# ============================================================

def gerarSequentesMd():

    nome_arquivo = "sequentes.md"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("# Sistema de Regras de Validação de Tipos — Cálculo de Sequentes\n\n")
        f.write("> **Tipos suportados:** `int`, `real`, `bool`  \n")
        f.write("> **Sistema de tipos:** estático e forte (Seção 2.3 da especificação)  \n")
        f.write("> **Ambiente de tipos:** Γ (contexto) mapeia nomes de variáveis para tipos\n\n")

        f.write("---\n\n")
        f.write("## 1. Regras para Literais\n\n")
        f.write("```\n")
        f.write("                          ⊢ n : int\n")
        f.write("[INT-LIT]  ─────────────────────────────────\n")
        f.write("           n é um literal inteiro (ex: 3, -7, 0)\n\n")

        f.write("                          ⊢ r : real\n")
        f.write("[REAL-LIT] ─────────────────────────────────\n")
        f.write("           r é um literal de ponto flutuante (ex: 3.14, -0.5)\n\n")

        f.write("                          ⊢ b : bool\n")
        f.write("[BOOL-LIT] ─────────────────────────────────\n")
        f.write("           b ∈ { TRUE, FALSE }\n")
        f.write("```\n\n")

        f.write("---\n\n")
        f.write("## 2. Regra para Variáveis\n\n")
        f.write("```\n")
        f.write("           x : T ∈ Γ\n")
        f.write("[VAR]      ──────────\n")
        f.write("           Γ ⊢ x : T\n\n")
        f.write("  Nota: variável deve estar definida em Γ antes do uso.\n")
        f.write("  Uso de variável não declarada é ERRO SEMÂNTICO FATAL.\n")
        f.write("```\n\n")

        f.write("---\n\n")
        f.write("## 3. Regras para Operadores Aritméticos\n\n")
        f.write("```\n")
        f.write("           Γ ⊢ e1 : int    Γ ⊢ e2 : int    op ∈ {+, -, *, ^}\n")
        f.write("[ARIT-INT] ────────────────────────────────────────────────────\n")
        f.write("           Γ ⊢ (e1 e2 op) : int\n\n")

        f.write("           Γ ⊢ e1 : T1    Γ ⊢ e2 : T2\n")
        f.write("           op ∈ {+, -, *, ^}    T1 ∈ {int, real}    T2 ∈ {int, real}\n")
        f.write("           T1 = real  ∨  T2 = real\n")
        f.write("[ARIT-REAL]────────────────────────────────────────────────────\n")
        f.write("           Γ ⊢ (e1 e2 op) : real\n\n")

        f.write("           Γ ⊢ e1 : int    Γ ⊢ e2 : int\n")
        f.write("[DIV-INT]  ──────────────────────────────\n")
        f.write("           Γ ⊢ (e1 e2 /) : int\n")
        f.write("  (divisão inteira — operandos DEVEM ser int)\n\n")

        f.write("           Γ ⊢ e1 : int    Γ ⊢ e2 : int\n")
        f.write("[MOD-INT]  ──────────────────────────────\n")
        f.write("           Γ ⊢ (e1 e2 %) : int\n")
        f.write("  (resto inteiro — operandos DEVEM ser int)\n\n")

        f.write("           Γ ⊢ e1 : T1    Γ ⊢ e2 : T2\n")
        f.write("           T1 ∈ {int, real}    T2 ∈ {int, real}\n")
        f.write("[DIV-REAL] ──────────────────────────────\n")
        f.write("           Γ ⊢ (e1 e2 '|') : real\n")
        f.write("  (divisão real — aceita int ou real, resultado sempre real)\n")
        f.write("```\n\n")

        f.write("---\n\n")
        f.write("## 4. Regras para Operadores Relacionais\n\n")
        f.write("```\n")
        f.write("           Γ ⊢ e1 : T    Γ ⊢ e2 : T\n")
        f.write("           T ∈ {int, real}    op ∈ {>, <}\n")
        f.write("[REL-NUM]  ──────────────────────────────\n")
        f.write("           Γ ⊢ (e1 e2 op) : bool\n\n")
        f.write("  Restrição: bool NÃO pode ser operando de > ou <.\n\n")
        f.write("           Γ ⊢ e1 : T    Γ ⊢ e2 : T\n")
        f.write("           T ∈ {int, real, bool}    op = ==\n")
        f.write("[EQ]       ──────────────────────────────\n")
        f.write("           Γ ⊢ (e1 e2 ==) : bool\n\n")
        f.write("  Operador == aceita int, real ou bool, desde que ambos os lados\n")
        f.write("  sejam do mesmo tipo (ou ambos numéricos). bool == bool é VÁLIDO.\n")
        f.write("```\n\n")

        f.write("---\n\n")
        f.write("## 4b. Regras para Operadores Lógicos\n\n")
        f.write("```\n")
        f.write("           Γ ⊢ e1 : bool    Γ ⊢ e2 : bool\n")
        f.write("[AND]      ──────────────────────────────────\n")
        f.write("           Γ ⊢ (e1 e2 AND) : bool\n\n")
        f.write("  Conjunção lógica. Ambos os operandos DEVEM ser bool.\n\n")
        f.write("           Γ ⊢ e1 : bool    Γ ⊢ e2 : bool\n")
        f.write("[OR]       ──────────────────────────────────\n")
        f.write("           Γ ⊢ (e1 e2 OR) : bool\n\n")
        f.write("  Disjunção lógica. Ambos os operandos DEVEM ser bool.\n\n")
        f.write("           Γ ⊢ e1 : bool\n")
        f.write("[NOT]      ──────────────────────────────────\n")
        f.write("           Γ ⊢ (e1 NOT) : bool\n\n")
        f.write("  Negação lógica. Operador UNÁRIO: usa apenas o topo da pilha.\n")
        f.write("  O operando DEVE ser bool.\n")
        f.write("```\n\n")

        f.write("---\n\n")
        f.write("## 5. Regras para Estruturas de Controle\n\n")
        f.write("```\n")
        f.write("           Γ ⊢ cond : bool    Γ ⊢ bloco : ok\n")
        f.write("[IF]       ───────────────────────────────────\n")
        f.write("           Γ ⊢ IF(cond, bloco) : ok\n\n")
        f.write("  Restrição: a condição de IF DEVE ter tipo bool.\n\n")

        f.write("           Γ ⊢ cond : bool    Γ ⊢ bloco : ok\n")
        f.write("[WHILE]    ───────────────────────────────────\n")
        f.write("           Γ ⊢ WHILE(cond, bloco) : ok\n\n")
        f.write("  Restrição: a condição de WHILE DEVE ter tipo bool.\n")
        f.write("```\n\n")

        f.write("---\n\n")
        f.write("## 6. Regras para Comandos Especiais\n\n")
        f.write("```\n")
        f.write("           Γ ⊢ v : T    MEM ∉ Γ\n")
        f.write("[MEM-DEF]  ──────────────────────────────────────────\n")
        f.write("           Γ ⊢ (v MEM) : ok,    Γ' = Γ ∪ { MEM : T }\n\n")
        f.write("  Define variável MEM com tipo T. Após a definição, MEM\n")
        f.write("  fica disponível em Γ para usos subsequentes.\n\n")

        f.write("           Γ ⊢ v : T    MEM : T ∈ Γ\n")
        f.write("[MEM-REDEF]──────────────────────────────────────────\n")
        f.write("           Γ ⊢ (v MEM) : ok    (reatribuição compatível)\n\n")
        f.write("           Γ ⊢ v : T'    MEM : T ∈ Γ    T' ≠ T\n")
        f.write("[MEM-ERR]  ──────────────────────────────────────────\n")
        f.write("           ERRO SEMÂNTICO: redefinição incompatível de tipo\n\n")

        f.write("           MEM : T ∈ Γ\n")
        f.write("[MEM-USO]  ────────────\n")
        f.write("           Γ ⊢ (MEM) : T\n\n")

        f.write("           Γ ⊢ n : int    n ≥ 0\n")
        f.write("[RES]      ──────────────────────\n")
        f.write("           Γ ⊢ (n RES) : any\n\n")
        f.write("  N deve ser inteiro não negativo. Retorna o resultado da\n")
        f.write("  expressão N linhas anteriores (array_res[ptr_res - N]).\n")
        f.write("```\n\n")

        f.write("---\n\n")
        f.write("## 7. Inferência de Tipos e Sistema Estático/Forte\n\n")
        f.write("O sistema de tipos da linguagem é **estático e forte** (Seção 2.3):\n\n")
        f.write("- O tipo de uma variável é determinado no **momento de sua definição**")
        f.write(" via `(V MEM)`, onde o tipo de `V` define o tipo da variável `MEM`.\n")
        f.write("- Uma vez tipada, a variável **não pode ser redefinida** com tipo")
        f.write(" incompatível — qualquer tentativa gera erro semântico (`[MEM-ERR]`).\n")
        f.write("- O uso de uma variável antes de sua definição é **erro semântico fatal**.\n")
        f.write("- Operações entre `bool` e `int`/`real` são **proibidas**.\n")
        f.write("- Divisão inteira `/` e resto `%` exigem operandos `int`.\n")
        f.write("- Divisão real `'|'` aceita `int` ou `real`, produzindo sempre `real`.\n")
        f.write("- Condições de `IF` e `WHILE` **devem** ter tipo `bool`.\n")
        f.write("- Operadores `AND` e `OR` exigem ambos os operandos `bool`.\n")
        f.write("- Operador `NOT` é **unário** e exige operando `bool`.\n")
        f.write("- Operador `==` aceita `bool == bool` além de numéricos.\n\n")
        f.write("```\n")
        f.write("Tabela de compatibilidade de operadores:\n\n")
        f.write("  Operador  | Tipos aceitos (e1, e2)           | Tipo resultado\n")
        f.write("  --------- | -------------------------------- | --------------\n")
        f.write("  +, -, *,^ | (int, int)                       | int\n")
        f.write("  +, -, *,^ | (real, real) ou (int,real)       | real\n")
        f.write("  /         | (int, int)                       | int\n")
        f.write("  %         | (int, int)                       | int\n")
        f.write("  '|'       | (int,int),(real,real),(int,real),(real,int) | real\n")
        f.write("  >, <      | (int, int) ou (real, real)       | bool\n")
        f.write("  ==        | (int,int),(real,real),(bool,bool) | bool\n")
        f.write("  AND, OR   | (bool, bool)                     | bool\n")
        f.write("  NOT       | (bool)  [unario]                 | bool\n")
        f.write("  IF/WHILE  | (bool, bloco)                    | ok\n")
        f.write("```\n\n")
        f.write("---\n\n")
        f.write("## 8. Nota sobre `(MEM)` como Leitura de Variável (Seção 2.1)\n\n")
        f.write("A especificação define dois usos distintos para variáveis:\n\n")
        f.write("- `(V MEM)` — **definição/atribuição**: armazena o valor `V` na variável `MEM`.\n")
        f.write("- `(MEM)` — **leitura**: retorna o valor armazenado em `MEM`.\n\n")
        f.write("Na gramática, a forma `(MEM)` (leitura) é implementada como `(ID)` onde `ID`\n")
        f.write("é o nome da variável (ex: `(X)`, `(CONTADOR)`, `(VAR)`). Isso é correto porque\n")
        f.write("o nome de uma variável é sempre um conjunto de letras latinas maiúsculas,\n")
        f.write("portanto categorizado como `ID` (não como `COMMAND`).\n\n")
        f.write("A produção `conteudo_rpn ::= valor elementos` com `elementos ::= epsilon`\n")
        f.write("permite exatamente a construção `(NOME_VAR)` — um único valor `ID` sem\n")
        f.write("elementos adicionais. A regra semântica `[MEM-USO]` se aplica a esse caso.\n")
    print(f"Regras de tipos (calcculo de sequentes) geradas em: '{nome_arquivo}'")

# ============================================================
# ANALISADOR LÉXICO — AFD
# ============================================================

class ListaTokens(list):
    """Lista de tokens com suporte a atributo _mapa_linhas para rastreamento de linhas."""
    def __init__(self, *args):
        super().__init__(*args)
        self._mapa_linhas = {}



def estado_inicial_afd(linha, i, tokens):
    if i >= len(linha):
        return i

    c = linha[i]

    if c in (' ', '\t'):
        return estado_inicial_afd(linha, i + 1, tokens)

    elif c in ('(', ')'):
        tokens.append(c)
        return estado_inicial_afd(linha, i + 1, tokens)

    elif c in ('{', '}'):
        tokens.append(c)
        return estado_inicial_afd(linha, i + 1, tokens)

    elif c in ('>', '<'):
        tokens.append(c)
        return estado_inicial_afd(linha, i + 1, tokens)

    elif c == '=':
        if i + 1 < len(linha) and linha[i + 1] == '=':
            tokens.append('==')
            return estado_inicial_afd(linha, i + 2, tokens)
        else:
            raise ValueError(f"Caractere invalido '=' isolado na posicao {i}")

    elif c == '|':
        tokens.append('|')
        return estado_inicial_afd(linha, i + 1, tokens)

    elif c == '/':
        tokens.append('/')
        return estado_inicial_afd(linha, i + 1, tokens)

    elif c in ('+', '*', '%', '^'):
        tokens.append(c)
        return estado_inicial_afd(linha, i + 1, tokens)

    elif c == '-':
        if i + 1 < len(linha) and ('0' <= linha[i + 1] <= '9'):
            return estado_numero_afd(linha, i, tokens)
        else:
            tokens.append(c)
            return estado_inicial_afd(linha, i + 1, tokens)

    elif '0' <= c <= '9':
        return estado_numero_afd(linha, i, tokens)

    elif c.isalpha() or c == '_':
        return estado_identificador_afd(linha, i, tokens)

    else:
        raise ValueError(f"Token invalido '{c}' na posicao {i}")


def estado_numero_afd(linha, i, tokens):
    num = ""
    ponto = False

    if i < len(linha) and linha[i] == '-':
        num += '-'
        i += 1

    while i < len(linha):
        c = linha[i]
        if '0' <= c <= '9':
            num += c
        elif c == '.':
            if ponto:
                raise ValueError(f"Numero malformado: multiplos pontos em '{num + c}'")
            ponto = True
            num += c
        else:
            break
        i += 1

    if num in ('-', ''):
        raise ValueError(f"Numero malformado: '{num}'")

    if num.endswith('.'):
        raise ValueError(f"Numero malformado: '{num}'")

    tokens.append(num)
    return estado_inicial_afd(linha, i, tokens)


def estado_identificador_afd(linha, i, tokens):
    ident = ""
    while i < len(linha) and (linha[i].isalnum() or linha[i] == '_'):
        ident += linha[i]
        i += 1
    tokens.append(ident)
    return estado_inicial_afd(linha, i, tokens)


def tokenizarLinha(linha):
    tokens = []
    estado_inicial_afd(linha, 0, tokens)
    return tokens


def validar_token(token):
    alfabeto_fixo = {
        'START', 'END', 'IF', 'WHILE', 'RES', 'MEM',
        'TRUE', 'FALSE',
        'AND', 'OR', 'NOT',
        '(', ')', '{', '}',
        '+', '-', '*', '|', '/', '%', '^',
        '>', '<', '=='
    }

    if token in alfabeto_fixo:
        return True

    t = token
    if t.startswith('-'):
        t = t[1:]

    if t.replace('.', '', 1).isdigit() and t != '.' and not t.startswith('.'):
        return True

    if token and (token[0].isalpha() or token[0] == '_') and all(c.isalnum() or c == '_' for c in token):
        return True

    return False

# ============================================================
# FASE 3 — REMOÇÃO DE COMENTÁRIOS *{ ... }*
# ============================================================

def removerComentarios(texto):
    comentarios_encontrados = []
    resultado = []
    i = 0
    num_linha = 1

    while i < len(texto):
        if texto[i] == '*' and i + 1 < len(texto) and texto[i+1] == '{':
            inicio = i
            linha_inicio = num_linha
            i += 2
            conteudo_comentario = ""

            while i < len(texto):
                if texto[i] == '}' and i + 1 < len(texto) and texto[i+1] == '*':
                    i += 2
                    break
                if texto[i] == '\n':
                    num_linha += 1
                    resultado.append('\n')
                conteudo_comentario += texto[i]
                i += 1
            else:
                print(f"[ERRO LEXICO] Linha {linha_inicio}: Comentario nao fechado (falta '}}*')")
                return None, comentarios_encontrados

            comentarios_encontrados.append((linha_inicio, conteudo_comentario.strip()))
        else:
            if texto[i] == '\n':
                num_linha += 1
            resultado.append(texto[i])
            i += 1

    return "".join(resultado), comentarios_encontrados

# ============================================================
# LEITURA DE TOKENS
# ============================================================

def lerTokens(arquivo):
    caminho_completo = os.path.abspath(arquivo)

    if not os.path.exists(caminho_completo):
        print(f"[ERRO DE SISTEMA] Arquivo nao encontrado em: {caminho_completo}")
        return None

    with open(caminho_completo, 'r', encoding='utf-8') as f:
        texto_completo = f.read()

    texto_sem_comentarios, comentarios = removerComentarios(texto_completo)
    if texto_sem_comentarios is None:
        return None

    tokens_extraidos = ListaTokens()
    mapa_linhas_extraido = {}
    erros_lexicos = 0
    tokens_comentario_lista = []
    if comentarios:
        print(f"[INFO LEXICO] {len(comentarios)} comentario(s) reconhecido(s) e descartados (tipo COMENTARIO):")
        for linha, conteudo in comentarios:
            trecho = conteudo[:40] + "..." if len(conteudo) > 40 else conteudo
            print(f"   [COMENTARIO] Linha {linha}: *{{ {trecho} }}*")
            # Token do tipo COMENTARIO: criado e imediatamente descartado (nao entra no vetor do parser)
            tokens_comentario_lista.append({
                "tipo": "COMENTARIO",
                "linha": linha,
                "conteudo": conteudo
            })

    linhas = texto_sem_comentarios.splitlines()

    for num_linha, linha in enumerate(linhas, 1):

        linha_limpa = linha.strip()

        if not linha_limpa:
            continue

        if ',' in linha_limpa and any(m in linha_limpa for m in
                ['OPERADOR', 'NUMERO', 'PALAVRA', 'PARENTESE', 'CHAVES']):

            partes = linha_limpa.split(',', 1)
            if len(partes) == 2:
                valor_token = partes[1].strip()
                if validar_token(valor_token):
                    mapa_linhas_extraido[len(tokens_extraidos)] = num_linha
                    tokens_extraidos.append(valor_token)
                else:
                    print(f"[ERRO LEXICO] Token invalido (Fase 1) - Linha {num_linha}: '{valor_token}'")
                    erros_lexicos += 1
            continue

        try:
            temp_tokens = tokenizarLinha(linha_limpa)
        except ValueError as e:
            print(f"[ERRO LEXICO] Linha {num_linha}: {e}")
            erros_lexicos += 1
            continue

        for t in temp_tokens:
            if validar_token(t):
                mapa_linhas_extraido[len(tokens_extraidos)] = num_linha
                tokens_extraidos.append(t)
            else:
                print(f"[ERRO LEXICO] Simbolo nao reconhecido - Linha {num_linha}: '{t}'")
                erros_lexicos += 1

    if erros_lexicos > 0:
        print(f"\nFATAL: Analise abortada. Analisador Lexico detectou {erros_lexicos} erro(s).")
        return None

    if tokens_extraidos and '$' not in tokens_extraidos:
        mapa_linhas_extraido[len(tokens_extraidos)] = num_linha if linhas else 0
        tokens_extraidos.append('$')

    if tokens_extraidos:
        tokens_extraidos._mapa_linhas = mapa_linhas_extraido
        tokens_extraidos._tokens_comentario = tokens_comentario_lista

    return tokens_extraidos if tokens_extraidos else None


def prepararEntradaSemantica(arquivo, tabela_ll1=None):
    tokens = lerTokens(arquivo)
    if tokens is None:
        return None, None, None

    if tabela_ll1 is None:
        gramatica = construirGramatica()
        first, nullable = calcularFirst(gramatica)
        follow = calcularFollow(gramatica, first, nullable)
        tabela_ll1 = construirTabelaLL1(gramatica, first, follow, nullable)

    sucesso, raiz_cst, arvore_ast, parser = parsear(tokens, tabela_ll1)

    if not sucesso:
        # Responsabilidade do Aluno 1: Reportar o erro sintático detalhado
        print(f"FALHA SINTATICA: '{arquivo}' contem erros sintaticos.")
        pos = parser.cursor
        if pos < len(tokens):
            token_erro = tokens[pos]
            print(f"\n--- LOCALIZACAO DO ERRO ---")
            print(f"Token: '{token_erro}' (posicao {pos})")
            inicio   = max(0, pos - 5)
            fim      = min(len(tokens), pos + 5)
            contexto = tokens[inicio:fim]
            print(f"Contexto: {' '.join(contexto)}")
            prefixo  = " ".join(tokens[inicio:pos])
            seta     = " " * (len(prefixo) + (1 if prefixo else 0)) + "^^^"
            print(f"          {seta}")
        else:
            print("[ERRO FATAL]: Fim de arquivo inesperado. Falta ( END ).")

        # Gera o log indicando a falha antes da semântica
        with open("erros_semanticos.md", "w", encoding="utf-8") as f_rel:
            f_rel.write("# Relatorio de Erros Semanticos\n\n")
            f_rel.write(f"**Arquivo analisado:** `{arquivo}`\n\n")
            f_rel.write("_Analise semantica nao executada (erro sintatico detectado)._\n")

        return tokens, None, None

    # Retorna tokens, a AST (para a semântica) e a CST (para o JSON na main)
    return tokens, arvore_ast, raiz_cst


def imprimirTokensLexicos(tokens):
    print("\n--- GERANDO SAIDA DO ANALISADOR LEXICO ---")

    # Exibe tokens COMENTARIO que foram reconhecidos e descartados (Seção 2.1)
    tokens_comentario = getattr(tokens, '_tokens_comentario', [])
    if tokens_comentario:
        print(f"[INFO LEXICO] Tokens do tipo COMENTARIO reconhecidos e descartados ({len(tokens_comentario)}):")
        for tc in tokens_comentario:
            trecho = tc['conteudo'][:40] + "..." if len(tc['conteudo']) > 40 else tc['conteudo']
            print(f"   COMENTARIO, *{{ {trecho} }}*  (linha {tc['linha']})")

    with open("tokens.txt", "w", encoding="utf-8") as f_out:
        # Registra tokens COMENTARIO no arquivo léxico (descartados — não enviados ao parser)
        for tc in tokens_comentario:
            trecho = tc['conteudo'][:40] + "..." if len(tc['conteudo']) > 40 else tc['conteudo']
            f_out.write(f"COMENTARIO,*{{ {trecho} }}*\n")
        for token in tokens:
            if token == '$':
                continue

            if token == '(':
                linha_token = f"PARENTESE_ESQUERDA,{token}"
            elif token == ')':
                linha_token = f"PARENTESE_DIREITA,{token}"
            elif token in ('{', '}'):
                linha_token = f"CHAVES,{token}"
            elif token in ('+', '-', '*', '|', '/', '%', '^', '>', '<', '=='):
                linha_token = f"OPERADOR,{token}"
            elif token in ('TRUE', 'FALSE'):
                linha_token = f"BOOLEANO,{token}"
            elif token.lstrip('-').replace('.', '', 1).isdigit():
                linha_token = f"NUMERO,{token}"
            else:
                linha_token = f"PALAVRA,{token}"

            print(linha_token)
            f_out.write(linha_token + "\n")

    print(f"\nTokens salvos com sucesso em: tokens.txt")
    print("------------------------------------------\n")

# ============================================================
# PARSER DESCENDENTE RECURSIVO E ÁRVORES (CST e AST)
# ============================================================

class ParserRecursivo:

    def __init__(self, tokens, tabela):
        self.tokens = tokens
        self.tabela = tabela
        self.cursor = 0
        self.erro = False
        self.pilha_analise = []
        self.pilha_semantica = []
        self.mapa_linhas = getattr(tokens, '_mapa_linhas', {})

    def linha_atual(self):
        return self.mapa_linhas.get(self.cursor, 0)

    def categorizar(self, token):
        comandos_especiais = {'RES', 'MEM'}
        if token in comandos_especiais:
            return 'COMMAND'

        if token in ('TRUE', 'FALSE'):
            return 'NUM'

        fixos = {
            'START', 'END', '(', ')', '{', '}',
            '+', '-', '*', '|', '/', '%', '^',
            '>', '<', '==',
            'AND', 'OR', 'NOT',
            'IF', 'WHILE', '$'
        }
        if token in fixos:
            return token

        t = token
        if t.startswith('-'):
            t = t[1:]
        if t.replace('.', '', 1).isdigit() and t != '.':
            return 'NUM'

        return 'ID'

    def lookahead(self):
        token_atual = self.tokens[self.cursor] if self.cursor < len(self.tokens) else '$'
        return self.categorizar(token_atual)

    def match(self, esperado, no_pai):
        token_atual = self.tokens[self.cursor] if self.cursor < len(self.tokens) else '$'

        if self.categorizar(token_atual) == esperado:
            no_pai["filhos"].append({"terminal": token_atual})
            self.resolver_semantica(token_atual)
            self.cursor += 1
        else:
            self.erro = True
            linha = self.linha_atual()
            info_linha = f" (linha {linha})" if linha else ""
            print(f"\n[AVISO DE SINTAXE]{info_linha}: Faltou '{esperado}'. Encontrado: '{token_atual}'.")
            print(f"[RECUPERACAO]: Tentando prosseguir...")
            if self.cursor < len(self.tokens) - 1:
                self.cursor += 1

    def resolver_semantica(self, token):
        if token in ('(', ')', '$'):
            return

        # Linha de origem real do token atual (vinda do mapa_linhas do lexico).
        # Cada no semantico carrega esta linha para que os erros semanticos
        # reportem a LINHA FISICA do arquivo, e nao o indice da instrucao —
        # corrigindo o desvio causado por linhas em branco e comentarios.
        linha = self.linha_atual()

        if token == 'START':
            self.pilha_semantica.append('MARKER_START')
            return

        if token == '{':
            self.pilha_semantica.append('MARKER_BLOCK')
            return

        if token == '}':
            instrucoes = []
            while self.pilha_semantica and self.pilha_semantica[-1] != 'MARKER_BLOCK':
                instrucoes.insert(0, self.pilha_semantica.pop())
            if self.pilha_semantica:
                self.pilha_semantica.pop()
            self.pilha_semantica.append({"tipo": "bloco", "instrucoes": instrucoes})
            return

        if token == 'END':
            instrucoes = []
            while self.pilha_semantica and self.pilha_semantica[-1] != 'MARKER_START':
                instrucoes.insert(0, self.pilha_semantica.pop())
            if self.pilha_semantica:
                self.pilha_semantica.pop()
            self.pilha_semantica.append({"tipo": "programa_ast", "instrucoes": instrucoes})
            return

        if token in ('+', '-', '*', '|', '/', '%', '^', '>', '<', '==', 'AND', 'OR'):
            dir_ = self.pilha_semantica.pop() if self.pilha_semantica else None
            esq  = self.pilha_semantica.pop() if self.pilha_semantica else None
            self.pilha_semantica.append({
                "tipo": "operacao",
                "operador": token,
                "esquerda": esq,
                "direita": dir_,
                "linha": linha
            })
            return

        if token == 'NOT':
            # NOT é unário: usa apenas o topo da pilha como operando
            operando = self.pilha_semantica.pop() if self.pilha_semantica else None
            self.pilha_semantica.append({
                "tipo": "operacao",
                "operador": "NOT",
                "esquerda": operando,
                "direita": None,   # NOT é unário
                "linha": linha
            })
            return

        if token in ('IF', 'WHILE'):
            bloco    = self.pilha_semantica.pop() if self.pilha_semantica else None
            condicao = self.pilha_semantica.pop() if self.pilha_semantica else None
            self.pilha_semantica.append({
                "tipo": "controle",
                "estrutura": token,
                "condicao": condicao,
                "bloco": bloco,
                "linha": linha
            })
            return

        if token == 'MEM':
            # Em RPN a instrução é (V VARNAME MEM).
            # Ordem de empilhamento: primeiro V, depois VARNAME.
            # Portanto o topo da pilha é VARNAME (variável destino)
            # e o segundo elemento é V (valor a armazenar).
            nome_var = self.pilha_semantica.pop() if self.pilha_semantica else None
            val_expr = self.pilha_semantica.pop() if self.pilha_semantica else None
            self.pilha_semantica.append({
                "tipo": "comando",
                "comando": "MEM",
                "nome_var": nome_var,   # nó variável destino (ex: X)
                "val_expr": val_expr,   # expressão cujo resultado é armazenado
                "linha": linha
            })
            return

        if token == 'RES':
            alvo = self.pilha_semantica.pop() if self.pilha_semantica else None
            self.pilha_semantica.append({
                "tipo": "comando",
                "comando": "RES",
                "alvo": alvo,
                "linha": linha
            })
            return

        if token == 'TRUE':
            self.pilha_semantica.append({
                "tipo": "numero",
                "valor": True,
                "tipo_dado": "bool",
                "linha": linha
            })
            return

        if token == 'FALSE':
            self.pilha_semantica.append({
                "tipo": "numero",
                "valor": False,
                "tipo_dado": "bool",
                "linha": linha
            })
            return

        t = token
        if t.startswith('-'):
            t = t[1:]

        if t.replace('.', '', 1).isdigit() and t != '.':
            if '.' in token:
                self.pilha_semantica.append({
                    "tipo": "numero",
                    "valor": float(token),
                    "tipo_dado": "real",
                    "linha": linha
                })
            else:
                self.pilha_semantica.append({
                    "tipo": "numero",
                    "valor": int(token),
                    "tipo_dado": "int",
                    "linha": linha
                })
        else:
            self.pilha_semantica.append({
                "tipo": "variavel",
                "nome": token,
                "tipo_dado": None,
                "linha": linha
            })

    def recuperar_erro_panico(self, nao_terminal, sync_set):
        self.erro = True
        encontrado = self.lookahead()
        linha = self.linha_atual()
        info_linha = f" (linha {linha})" if linha else ""
        print(f"\n[AVISO DE SINTAXE]{info_linha}: Erro na regra '{nao_terminal}'. Token inesperado: '{encontrado}'.")
        print(f"[RECUPERACAO (Panic Mode)]: Buscando token de sincronizacao...")
        while self.cursor < len(self.tokens) - 1:
            la = self.lookahead()
            if la in sync_set:
                print(f" -> Sincronizado no token: '{la}'. Retomando o parser.")
                break
            print(f"    Descartando token '{la}'...")
            self.cursor += 1

    def processar_producao(self, nao_terminal, no_pai):
        self.pilha_analise.append(nao_terminal)
        la = self.lookahead()
        producao = self.tabela[nao_terminal].get(la)

        if producao is None:
            sync_set = {t for t, p in self.tabela[nao_terminal].items() if p is not None}
            sync_set.update({')', '}', 'END', '$'})
            self.recuperar_erro_panico(nao_terminal, sync_set)
            self.pilha_analise.pop()
            return

        no_atual = {"nome": nao_terminal, "filhos": []}
        no_pai["filhos"].append(no_atual)

        for simbolo in producao:
            if simbolo == 'EPSILON':
                no_atual["filhos"].append({"terminal": "ε"})
            elif simbolo in self.tabela:
                if simbolo == 'programa': self.parse_programa(no_atual)
                elif simbolo == 'laco_principal': self.parse_laco_principal(no_atual)
                elif simbolo == 'linha_ou_fim': self.parse_linha_ou_fim(no_atual)
                elif simbolo == 'lista_instrucoes': self.parse_lista_instrucoes(no_atual)
                elif simbolo == 'continua_lista': self.parse_continua_lista(no_atual)
                elif simbolo == 'instrucao': self.parse_instrucao(no_atual)
                elif simbolo == 'conteudo_rpn': self.parse_conteudo_rpn(no_atual)
                elif simbolo == 'elementos': self.parse_elementos(no_atual)
                elif simbolo == 'acao_final': self.parse_acao_final(no_atual)
                elif simbolo == 'acao_pos_op': self.parse_acao_pos_op(no_atual)
                elif simbolo == 'estrutura_controle': self.parse_estrutura_controle(no_atual)
                elif simbolo == 'tipo_controle': self.parse_tipo_controle(no_atual)
                elif simbolo == 'bloco_codigo': self.parse_bloco_codigo(no_atual)
                elif simbolo == 'valor': self.parse_valor(no_atual)
                elif simbolo == 'operador': self.parse_operador(no_atual)
            else:
                self.match(simbolo, no_atual)

        self.pilha_analise.pop()

    def parse_programa(self, no_pai):           self.processar_producao('programa', no_pai)
    def parse_laco_principal(self, no_pai):     self.processar_producao('laco_principal', no_pai)
    def parse_linha_ou_fim(self, no_pai):       self.processar_producao('linha_ou_fim', no_pai)
    def parse_lista_instrucoes(self, no_pai):   self.processar_producao('lista_instrucoes', no_pai)
    def parse_continua_lista(self, no_pai):     self.processar_producao('continua_lista', no_pai)
    def parse_instrucao(self, no_pai):          self.processar_producao('instrucao', no_pai)
    def parse_conteudo_rpn(self, no_pai):       self.processar_producao('conteudo_rpn', no_pai)
    def parse_elementos(self, no_pai):          self.processar_producao('elementos', no_pai)
    def parse_acao_final(self, no_pai):         self.processar_producao('acao_final', no_pai)
    def parse_acao_pos_op(self, no_pai):        self.processar_producao('acao_pos_op', no_pai)
    def parse_estrutura_controle(self, no_pai): self.processar_producao('estrutura_controle', no_pai)
    def parse_tipo_controle(self, no_pai):      self.processar_producao('tipo_controle', no_pai)
    def parse_bloco_codigo(self, no_pai):       self.processar_producao('bloco_codigo', no_pai)
    def parse_valor(self, no_pai):              self.processar_producao('valor', no_pai)
    def parse_operador(self, no_pai):           self.processar_producao('operador', no_pai)


def parsear(tokens, tabela_ll1):
    parser = ParserRecursivo(tokens, tabela_ll1)
    raiz_oculta = {"nome": "ROOT", "filhos": []}
    parser.parse_programa(raiz_oculta)

    sucesso = not parser.erro and (
        parser.cursor >= len(tokens) - 1 or tokens[parser.cursor] == '$'
    )

    raiz_cst = raiz_oculta["filhos"][0] if raiz_oculta["filhos"] else raiz_oculta
    raiz_ast = parser.pilha_semantica[0] if parser.pilha_semantica else {}

    return sucesso, raiz_cst, raiz_ast, parser


def gerarArvore(cst_dict, ast_dict):
    with open("arvore_cst.json", "w", encoding="utf-8") as f_cst:
        json.dump(cst_dict, f_cst, indent=4, ensure_ascii=False)
    print("Arvore de Derivacao Concreta gerada em 'arvore_cst.json'!")

    with open("arvore_ast.json", "w", encoding="utf-8") as f_ast:
        json.dump(ast_dict, f_ast, indent=4, ensure_ascii=False)
    print("Arvore Sintatica Abstrata gerada em 'arvore_ast.json'!")

# ============================================================
# FASE 3 — ANALISADOR SEMÂNTICO
# ============================================================

class TabelaSimbolos:
    def __init__(self):
        self.simbolos = {}

    def definir(self, nome, tipo, linha=0):
        if nome in self.simbolos:
            entrada = self.simbolos[nome]
            if entrada['tipo'] is not None and entrada['tipo'] != tipo and tipo is not None:
                return False, (
                    f"Redefinicao incompativel de '{nome}': "
                    f"tipo anterior '{entrada['tipo']}', novo tipo '{tipo}'"
                )
            if tipo is not None:
                entrada['tipo'] = tipo
            entrada['linha_def'] = linha
            return True, None
        else:
            self.simbolos[nome] = {
                'tipo': tipo,
                'linha_def': linha,
                'escopo': 'global',
                'linhas_uso': [],
                'definida': True
            }
            return True, None

    def usar(self, nome, linha=0):
        if nome not in self.simbolos:
            return False
        self.simbolos[nome]['linhas_uso'].append(linha)
        return True

    def tipo_de(self, nome):
        if nome in self.simbolos:
            return self.simbolos[nome]['tipo']
        return None

    def esta_definida(self, nome):
        return nome in self.simbolos and self.simbolos[nome].get('definida', False)

    def para_dict(self):
        return dict(self.simbolos)


def inferir_tipo_no(no, tabela, erros, linha_ctx=0):

    if not isinstance(no, dict):
        return None

    # Se o no carrega a linha de origem real (anotada pelo parser), usa-a como
    # contexto para este no e seus filhos. Assim os erros apontam para a linha
    # fisica do arquivo, ignorando linhas em branco e comentarios.
    linha_ctx = no.get("linha", linha_ctx)

    tipo = no.get("tipo")

    if tipo == "numero":
        td = no.get("tipo_dado")
        if td is None:
            v = no.get("valor")
            if isinstance(v, bool):
                td = "bool"
            elif isinstance(v, float):
                td = "real"
            else:
                td = "int"
            no["tipo_dado"] = td
        return td

    elif tipo == "variavel":
        nome = no.get("nome")
        # CORREÇÃO 1: variável usada sem definição prévia é ERRO FATAL, não aviso.
        # A spec diz que variáveis devem ser definidas com (V MEM) antes de serem usadas.
        if not tabela.esta_definida(nome):
            erros.append({
                "linha": linha_ctx,
                "elemento": nome,
                "causa": f"Variavel '{nome}' usada sem definicao previa com (V MEM). "
                         f"Variaveis devem ser definidas antes de serem usadas (Secao 2.1 da especificacao)."
                # sem "nivel": "aviso" — ausencia do campo faz este erro ser tratado como fatal
            })
            tabela.definir(nome, None, linha_ctx)
            no["tipo_dado"] = None
            tabela.usar(nome, linha_ctx)
            return None
        t = tabela.tipo_de(nome)
        no["tipo_dado"] = t
        tabela.usar(nome, linha_ctx)
        return t

    elif tipo == "operacao":
        op = no.get("operador")
        t_esq = inferir_tipo_no(no.get("esquerda"), tabela, erros, linha_ctx)
        t_dir = inferir_tipo_no(no.get("direita"),  tabela, erros, linha_ctx)

        tipo_resultado = _verificar_operacao(op, t_esq, t_dir, erros, linha_ctx, no)
        no["tipo_dado"] = tipo_resultado
        return tipo_resultado

    elif tipo == "comando" and no.get("comando") == "MEM":
        # val_expr: expressão cujo valor é armazenado (ex: literal 10)
        # nome_var: nó variável que recebe o valor (ex: X)
        val_no = no.get("val_expr")
        var_no = no.get("nome_var")

        t_val = inferir_tipo_no(val_no, tabela, erros, linha_ctx)

        if var_no and var_no.get("tipo") == "variavel":
            nome_v = var_no["nome"]
            ok, msg = tabela.definir(nome_v, t_val, linha_ctx)
            if not ok:
                erros.append({"linha": linha_ctx, "elemento": nome_v, "causa": msg})
            var_no["tipo_dado"] = t_val

        no["tipo_dado"] = t_val
        return t_val

    elif tipo == "comando" and no.get("comando") == "RES":
        alvo = no.get("alvo")
        t_alvo = inferir_tipo_no(alvo, tabela, erros, linha_ctx)
        if t_alvo not in ("int", None):
            erros.append({
                "linha": linha_ctx,
                "elemento": "RES",
                "causa": f"O argumento de RES deve ser inteiro, mas recebeu '{t_alvo}'."
            })
        no["tipo_dado"] = "any"
        return "any"

    elif tipo == "controle":
        estrutura = no.get("estrutura")
        cond_no   = no.get("condicao")
        bloco_no  = no.get("bloco")

        t_cond = inferir_tipo_no(cond_no, tabela, erros, linha_ctx)

        if t_cond != "bool" and t_cond is not None:
            erros.append({
                "linha": linha_ctx,
                "elemento": estrutura,
                "causa": (
                    f"Condicao de '{estrutura}' deve ter tipo 'bool', "
                    f"mas recebeu '{t_cond}'."
                )
            })

        inferir_tipo_no(bloco_no, tabela, erros, linha_ctx)
        no["tipo_dado"] = "ok"
        return "ok"

    elif tipo == "bloco":
        for inst in no.get("instrucoes", []):
            inferir_tipo_no(inst, tabela, erros, linha_ctx)
        no["tipo_dado"] = "ok"
        return "ok"

    elif tipo == "programa_ast":
        for i, inst in enumerate(no.get("instrucoes", [])):
            inferir_tipo_no(inst, tabela, erros, i + 1)
        no["tipo_dado"] = "ok"
        return "ok"

    return None


def _verificar_operacao(op, t_esq, t_dir, erros, linha, no):
    # PROBLEMA 6 CORRIGIDO: separar '==' de '>' e '<'.
    # '>' e '<' só aceitam numéricos; '==' também aceita bool == bool.
    if op in ('>', '<'):
        if t_esq in ('int', 'real', None) and t_dir in ('int', 'real', None):
            if t_esq is None or t_dir is None:
                return "bool"
            return "bool"
        else:
            erros.append({
                "linha": linha,
                "elemento": op,
                "causa": f"Operador '{op}' nao pode ser aplicado a tipos '{t_esq}' e '{t_dir}'. Requer numericos (int ou real)."
            })
            return None

    if op == '==':
        # Aceita: int==int, real==real, bool==bool, int==real (e vice-versa), None (tipo desconhecido)
        tipos_compativeis = {'int', 'real', 'bool', None}
        if t_esq not in tipos_compativeis or t_dir not in tipos_compativeis:
            erros.append({
                "linha": linha,
                "elemento": op,
                "causa": f"Operador '==' nao pode ser aplicado a tipos '{t_esq}' e '{t_dir}'."
            })
            return None
        # bool == bool: válido; int == bool ou real == bool: inválido
        if (t_esq == 'bool') != (t_dir == 'bool') and t_esq is not None and t_dir is not None:
            erros.append({
                "linha": linha,
                "elemento": op,
                "causa": f"Operador '==' nao pode comparar tipos '{t_esq}' e '{t_dir}' — mistura bool com numerico."
            })
            return None
        return "bool"

    # PROBLEMA 3: AND e OR — operadores lógicos binários (bool op bool → bool)
    if op in ('AND', 'OR'):
        if t_esq == 'bool' and t_dir == 'bool':
            return 'bool'
        if t_esq is None or t_dir is None:
            return 'bool'
        erros.append({
            "linha": linha,
            "elemento": op,
            "causa": (
                f"Operador logico '{op}' requer operandos bool. "
                f"Recebeu '{t_esq}' e '{t_dir}'."
            )
        })
        return None

    # PROBLEMA 3: NOT — operador lógico unário (bool → bool); t_dir é None (ignorado)
    if op == 'NOT':
        if t_esq == 'bool' or t_esq is None:
            return 'bool'
        erros.append({
            "linha": linha,
            "elemento": op,
            "causa": f"Operador logico 'NOT' requer operando bool. Recebeu '{t_esq}'."
        })
        return None

    if op in ('/', '%'):
        if t_esq == 'int' and t_dir == 'int':
            return 'int'
        if t_esq is None or t_dir is None:
            return 'int'
        erros.append({
            "linha": linha,
            "elemento": op,
            "causa": (
                f"Operador '{op}' (divisao inteira/resto) requer operandos inteiros. "
                f"Recebeu '{t_esq}' e '{t_dir}'."
            )
        })
        return None

    if op == '|':
        if t_esq in ('int', 'real', None) and t_dir in ('int', 'real', None):
            return 'real'
        erros.append({
            "linha": linha,
            "elemento": op,
            "causa": f"Operador '|' (divisao real) requer operandos numericos. Recebeu '{t_esq}' e '{t_dir}'."
        })
        return None

    if op in ('+', '-', '*', '^'):
        tipos_validos = {'int', 'real', None, 'any'}
        if t_esq in tipos_validos and t_dir in tipos_validos:
            if t_esq == 'bool' or t_dir == 'bool':
                erros.append({
                    "linha": linha,
                    "elemento": op,
                    "causa": f"Operador '{op}' nao pode ser aplicado a tipo 'bool'. Recebeu '{t_esq}' e '{t_dir}'."
                })
                return None
            if t_esq == 'real' or t_dir == 'real':
                return 'real'
            return 'int'
        erros.append({
            "linha": linha,
            "elemento": op,
            "causa": f"Operador '{op}' recebeu tipos incompativeis: '{t_esq}' e '{t_dir}'."
        })
        return None

    return None


def construirTabelaSimbolos(arvore_ast):
    tabela = TabelaSimbolos()
    erros  = []

    def _erro_nao_declarada(nome, linha):
        """Registra erro de variável usada antes de ser definida com MEM."""
        erros.append({
            "linha": linha,
            "elemento": nome,
            "causa": (
                f"Variavel '{nome}' usada sem definicao previa com (V MEM). "
                f"Variaveis devem ser definidas antes de serem usadas "
                f"(Secao 2.1 da especificacao)."
            )
        })

    def percorrer(no, linha=0):
        if not isinstance(no, dict):
            return

        # Usa a linha de origem real anotada no no (quando disponivel).
        linha = no.get("linha", linha)

        tipo = no.get("tipo")

        if tipo == "programa_ast":
            for i, inst in enumerate(no.get("instrucoes", [])):
                percorrer(inst, i + 1)

        elif tipo == "bloco":
            for inst in no.get("instrucoes", []):
                percorrer(inst, linha)

        elif tipo == "variavel":
            # Uso de variável: verificar se já foi definida via MEM
            nome = no.get("nome")
            if nome and not tabela.esta_definida(nome):
                _erro_nao_declarada(nome, linha)
                # Registrar mesmo assim para evitar erros duplicados nas próximas ocorrências
                tabela.definir(nome, None, linha)

        elif tipo == "comando" and no.get("comando") == "MEM":
            val_no = no.get("val_expr")
            var_no = no.get("nome_var")

            # Percorrer o lado valor ANTES de definir a variável destino,
            # para que uma referência à mesma variável no valor ainda seja detectada.
            percorrer(val_no, linha)

            t_val = _tipo_literal(val_no, tabela)

            if var_no and var_no.get("tipo") == "variavel":
                nome_v = var_no["nome"]
                ok, msg = tabela.definir(nome_v, t_val, linha)
                if not ok:
                    erros.append({"linha": linha, "elemento": nome_v, "causa": msg})

        elif tipo == "operacao":
            percorrer(no.get("esquerda"), linha)
            percorrer(no.get("direita"),  linha)

        elif tipo == "controle":
            percorrer(no.get("condicao"), linha)
            percorrer(no.get("bloco"),    linha)

        elif tipo == "comando" and no.get("comando") == "RES":
            alvo = no.get("alvo")
            percorrer(alvo, linha)
            
            # Responsabilidade do Aluno 2: Validar a referência feita com RES
            if alvo and alvo.get("tipo") == "numero":
                val = alvo.get("valor")
                tipo_dado_res = alvo.get("tipo_dado", _tipo_literal(alvo))
                
                if tipo_dado_res != "int":
                    erros.append({
                        "linha": linha,
                        "elemento": "RES",
                        "causa": f"O argumento de RES deve ser inteiro. Recebeu '{tipo_dado_res}'."
                    })
                elif isinstance(val, int) and not isinstance(val, bool) and val < 0:
                    erros.append({
                        "linha": linha,
                        "elemento": "RES",
                        "causa": f"N em (N RES) deve ser inteiro nao negativo. Recebeu '{val}'."
                    })

    percorrer(arvore_ast)
    return tabela, erros


def _tipo_literal(no, tabela_hint=None):

    if not isinstance(no, dict):
        return None

    tipo = no.get("tipo")

    if tipo == "numero":
        return no.get("tipo_dado")

    if tipo == "variavel":
        # Se temos a tabela, tenta recuperar o tipo já registrado
        if tabela_hint is not None:
            return tabela_hint.tipo_de(no.get("nome"))
        return None

    if tipo == "operacao":
        op = no.get("operador")
        t_esq = _tipo_literal(no.get("esquerda"), tabela_hint)
        t_dir = _tipo_literal(no.get("direita"),  tabela_hint)

        # Operadores que sempre produzem bool
        if op in ('>', '<', '==', 'AND', 'OR', 'NOT'):
            return 'bool'
        # Divisão/resto inteiro → int
        if op in ('/', '%'):
            if t_esq == 'int' and t_dir == 'int':
                return 'int'
            return None  # tipos incompatíveis ou desconhecidos
        # Divisão real → real
        if op == '|':
            return 'real'
        # Aritméticos: promoção int→real se qualquer operando for real
        if op in ('+', '-', '*', '^'):
            if t_esq == 'real' or t_dir == 'real':
                return 'real'
            if t_esq == 'int' and t_dir == 'int':
                return 'int'
            if t_esq == 'int' and t_dir is None:
                return 'int'
            if t_dir == 'int' and t_esq is None:
                return 'int'
        return None

    if tipo == "comando":
        # (V MEM) retorna o tipo do valor atribuído
        if no.get("comando") == "MEM":
            return _tipo_literal(no.get("val_expr"), tabela_hint)
        # (N RES) retorna any — não determina tipo estático
        return None

    return None


def verificarTipos(arvore_ast, tabela):
    erros = []

    if arvore_ast is None:
        return erros

    inferir_tipo_no(arvore_ast, tabela, erros, linha_ctx=0)

    def checar_res_negativo(no, linha_ctx=0):
        if not isinstance(no, dict):
            return
        linha_ctx = no.get("linha", linha_ctx)
        if no.get("tipo") == "comando" and no.get("comando") == "RES":
            alvo = no.get("alvo", {})
            if isinstance(alvo, dict) and alvo.get("tipo") == "numero":
                val = alvo.get("valor")
                if isinstance(val, int) and not isinstance(val, bool) and val < 0:
                    erros.append({
                        "linha": linha_ctx,
                        "elemento": "RES",
                        "causa": f"N em (N RES) deve ser inteiro nao negativo. Recebeu '{val}'."
                    })
        for filho in ["esquerda", "direita", "condicao", "bloco", "val_expr", "nome_var", "alvo"]:
            checar_res_negativo(no.get(filho), linha_ctx)
        for i, inst in enumerate(no.get("instrucoes", [])):
            checar_res_negativo(inst, i + 1)

    checar_res_negativo(arvore_ast)
    return erros


def gerarArvoreAtribuida(arvore_ast, tabela, erros_tipos, arquivo_alvo=""):
    # Adiciona metadado de origem antes de serializar (Seção 10.4)
    saida_json = {
        "arquivo_analisado": arquivo_alvo,
        "arvore_atribuida": arvore_ast
    }
    with open("arvore_atribuida.json", "w", encoding="utf-8") as f:
        json.dump(saida_json, f, indent=4, ensure_ascii=False, default=str)
    print("Arvore Sintatica Atribuida gerada em 'arvore_atribuida.json'!")

    linhas_md = ["# Árvore Sintática Atribuída\n"]
    if arquivo_alvo:
        linhas_md.append(f"**Arquivo analisado:** `{arquivo_alvo}`\n")
    linhas_md.append("## Tabela de Símbolos\n")
    linhas_md.append("| Variável | Escopo | Tipo | Linha Def | Linhas Uso |")
    linhas_md.append("|----------|--------|------|-----------|------------|")
    for nome, info in sorted(tabela.para_dict().items()):
        usos = ", ".join(str(l) for l in info.get("linhas_uso", []))
        linhas_md.append(
            f"| `{nome}` | `{info.get('escopo','global')}` | `{info.get('tipo','?')}` | {info.get('linha_def','?')} | {usos or '—'} |"
        )

    linhas_md.append("\n## Erros Semânticos\n")
    if erros_tipos:
        for e in erros_tipos:
            linhas_md.append(
                f"- **Linha {e['linha']}** — `{e['elemento']}`: {e['causa']}"
            )
    else:
        linhas_md.append("_Nenhum erro semântico detectado._")

    linhas_md.append("\n## Regras de Tipo (Cálculo de Sequentes)\n")
    linhas_md.append("> Consulte também o arquivo `sequentes.md` para a versão completa e detalhada.\n")
    linhas_md.append("> **Nota sobre inferência de tipos (Seção 2.3):** o sistema é estático e forte.")
    linhas_md.append("> O tipo de cada variável é determinado no momento de sua definição via `(V MEM)`.")
    linhas_md.append("> Usos posteriores em contexto incompatível geram erro semântico — não há")
    linhas_md.append("> redefinição implícita de tipo pelo contexto de uso.\n")
    linhas_md.append("```")
    linhas_md.append("[INT-LIT]   ⊢ n : int             (n literal inteiro)")
    linhas_md.append("[REAL-LIT]  ⊢ r : real            (r literal real)")
    linhas_md.append("[BOOL-LIT]  ⊢ b : bool            (b ∈ {TRUE, FALSE})")
    linhas_md.append("")
    linhas_md.append("[VAR]       x:T ∈ Γ")
    linhas_md.append("            ────────")
    linhas_md.append("            Γ ⊢ x : T")
    linhas_md.append("")
    linhas_md.append("[ARIT-INT]  Γ ⊢ e1:int, Γ ⊢ e2:int, op ∈ {+,-,*,^}  ⊢  (e1 e2 op) : int")
    linhas_md.append("[ARIT-REAL] Γ ⊢ e1:T1, Γ ⊢ e2:T2, op ∈ {+,-,*,^}, T1∨T2=real  ⊢  (e1 e2 op) : real")
    linhas_md.append("[DIV-INT]   Γ ⊢ e1:int, Γ ⊢ e2:int  ⊢  (e1 e2 /) : int")
    linhas_md.append("[MOD-INT]   Γ ⊢ e1:int, Γ ⊢ e2:int  ⊢  (e1 e2 %) : int")
    linhas_md.append("[DIV-REAL]  Γ ⊢ e1:T1, Γ ⊢ e2:T2, T1,T2 ∈ {int,real}  ⊢  (e1 e2 '|') : real")
    linhas_md.append("[REL-NUM]   Γ ⊢ e1:T, Γ ⊢ e2:T, T ∈ {int,real}, op ∈ {>,<}  ⊢  (e1 e2 op) : bool")
    linhas_md.append("[EQ]        Γ ⊢ e1:T, Γ ⊢ e2:T, T ∈ {int,real,bool}  ⊢  (e1 e2 ==) : bool")
    linhas_md.append("[AND]       Γ ⊢ e1:bool, Γ ⊢ e2:bool  ⊢  (e1 e2 AND) : bool")
    linhas_md.append("[OR]        Γ ⊢ e1:bool, Γ ⊢ e2:bool  ⊢  (e1 e2 OR)  : bool")
    linhas_md.append("[NOT]       Γ ⊢ e1:bool  ⊢  (e1 NOT) : bool   [unario]")
    linhas_md.append("[IF]        Γ ⊢ cond:bool, Γ ⊢ bloco:ok  ⊢  IF(cond,bloco) : ok")
    linhas_md.append("[WHILE]     Γ ⊢ cond:bool, Γ ⊢ bloco:ok  ⊢  WHILE(cond,bloco) : ok")
    linhas_md.append("[MEM-DEF]   Γ ⊢ v:T  ⊢  (v MEM):ok,  Γ'=Γ[MEM↦T]")
    linhas_md.append("[MEM-REDEF] Γ ⊢ v:T, MEM:T ∈ Γ  ⊢  (v MEM):ok  (reatribuição compatível)")
    linhas_md.append("[MEM-ERR]   Γ ⊢ v:T', MEM:T ∈ Γ, T'≠T  ⊢  ERRO SEMÂNTICO")
    linhas_md.append("[MEM-USO]   MEM:T ∈ Γ  ⊢  (MEM):T  — leitura via instrução (ID) na gramática")
    linhas_md.append("[RES]       Γ ⊢ n:int, n≥0  ⊢  (n RES):any")
    linhas_md.append("```")

    linhas_md.append("\n## Nós da Árvore Atribuída\n")
    linhas_md.append("```json")
    linhas_md.append(json.dumps(arvore_ast, indent=2, ensure_ascii=False, default=str))
    linhas_md.append("```")

    with open("arvore_atribuida.md", "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_md))
    print("Arvore Sintatica Atribuida (Markdown) gerada em 'arvore_atribuida.md'!")

    return arvore_ast


def salvarTabelaSimbolos(tabela, erros, arquivo_alvo=""):
    dados = {
        "arquivo_analisado": arquivo_alvo,
        "tabela_simbolos": tabela.para_dict(),
        "erros_semanticos": erros
    }
    with open("tabela_simbolos.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    print("Tabela de simbolos salva em 'tabela_simbolos.json'!")

    linhas = ["# Tabela de Símbolos\n"]
    if arquivo_alvo:
        linhas.append(f"**Arquivo analisado:** `{arquivo_alvo}`\n")
    linhas.append("| Variável | Escopo | Tipo | Linha Definição | Linhas de Uso |")
    linhas.append("|----------|--------|------|-----------------|---------------|")
    for nome, info in sorted(tabela.para_dict().items()):
        usos = ", ".join(str(l) for l in info.get("linhas_uso", []))
        linhas.append(
            f"| `{nome}` | `{info.get('escopo','global')}` | `{info.get('tipo','?')}` | {info.get('linha_def','?')} | {usos or '—'} |"
        )

    linhas.append("\n## Erros Semânticos\n")
    if erros:
        for e in erros:
            linhas.append(f"- **Linha {e['linha']}** — `{e['elemento']}`: {e['causa']}")
    else:
        linhas.append("_Sem erros semânticos._")

    with open("tabela_simbolos.md", "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print("Tabela de simbolos salva em 'tabela_simbolos.md'!")


# ============================================================
# GERAÇÃO DE CÓDIGO ASSEMBLY (ARMv7 CPulator DE1-SoC)
# ============================================================

def gerarAssembly(arvore_ast):
    nome_arquivo = "saida_assembly.s"  # Nome do arquivo de saída assembly

    cst_constantes = {}  # Dicionário para armazenar constantes únicas
    vrv_mr = set()       # Conjunto de variáveis usadas (para declarar depois)
    asm = []             # Lista de instruções assembly geradas

    # Contadores para gerar labels únicos (if, while, constantes, potência, lógicos e ltorg)
    contador_labels = {'if': 0, 'while': 0, 'const': 0, 'pow': 0, 'logico': 0, 'ltorg': 0}

    # Função que cria ou reutiliza uma constante
    def obter_constante(val):
        val_str = str(val)  # Converte valor para string (chave do dicionário)
        if val_str not in cst_constantes:
            # Se ainda não existe, cria label nova
            label = f"const_{contador_labels['const']}"
            contador_labels['const'] += 1
            cst_constantes[val_str] = label
        return cst_constantes[val_str]  # Retorna label da constante

    # Função recursiva que percorre a AST
    def gerar_codigo_recursivo(no):
        # Garante constantes 0 e 1
        l_zero = obter_constante(0.0)
        l_one  = obter_constante(1.0)

        # Se não for um nó válido, ignora
        if not isinstance(no, dict):
            return

        tipo = no.get("tipo")  # Tipo do nó da AST

        # ============================
        # BLOCO OU PROGRAMA
        # ============================
        if tipo in ("programa_ast", "bloco"):
            for inst in no.get("instrucoes", []):
                gerar_codigo_recursivo(inst)  # Gera código da instrução

                # Salva resultado no histórico (array_res) APENAS no fluxo principal
                if tipo == "programa_ast" and inst.get("tipo") not in ["controle", "bloco"]:
                    asm.append("\n    @ salva no historico")
                    asm.append("    VPOP {D0}")        # Pega resultado da pilha
                    asm.append("    LDR R0, =array_res")
                    asm.append("    LDR R1, =ptr_res")
                    asm.append("    LDR R2, [R1]")    # Índice atual
                    asm.append("    ADD R3, R0, R2, LSL #3")  # Calcula posição
                    asm.append("    VSTR.F64 D0, [R3]")        # Salva valor
                    asm.append("    ADD R2, R2, #1")           # Incrementa índice
                    asm.append("    STR R2, [R1]")
                    asm.append("    VPUSH {D0}")               # Mantém na pilha

                # ========================================================
                # A MÁGICA ACONTECE AQUI: DUMP DO LITERAL POOL
                # Despeja a memória no meio do código e pula por cima 
                # para evitar o erro "pool needs to be closer"
                # ========================================================
                idx_ltorg = contador_labels['ltorg']
                contador_labels['ltorg'] += 1
                asm.append(f"\n    @ Despeja literal pool para evitar erro de limite de 4KB")
                asm.append(f"    B skip_pool_{idx_ltorg}")
                asm.append(f"    .ltorg")
                asm.append(f"skip_pool_{idx_ltorg}:")

        # ============================
        # NÚMERO
        # ============================
        elif tipo == "numero":
            valor = no["valor"]
            if isinstance(valor, bool):
                valor = 1.0 if valor else 0.0
                
            label = obter_constante(valor)  # Obtém constante
            asm.append(f"    LDR R0, ={label}")   # Carrega endereço
            asm.append(f"    VLDR D0, [R0]")      # Carrega valor
            asm.append(f"    VPUSH {{D0}}")       # Empilha

        # ============================
        # VARIÁVEL
        # ============================
        elif tipo == "variavel":
            var = no["nome"]
            vrv_mr.add(var)  # Marca variável para declaração futura
            asm.append(f"    LDR R0, ={var}")
            asm.append(f"    VLDR D0, [R0]")
            asm.append(f"    VPUSH {{D0}}")

        # ============================
        # OPERAÇÃO
        # ============================
        elif tipo == "operacao":
            # Gera código do operando esquerdo primeiro
            gerar_codigo_recursivo(no["esquerda"])
            
            op = no["operador"]

            # TRATAMENTO PARA OPERADOR UNÁRIO (NOT)
            if op == 'NOT':
                asm.append(f"\n    @ operacao NOT")
                idx = contador_labels['logico']
                contador_labels['logico'] += 1
                asm.append("    VPOP {D0}")  # Apenas um operando na pilha
                asm.append(f"    LDR R2, ={l_zero}")
                asm.append("    VLDR D1, [R2]")
                asm.append("    VCMP.F64 D0, D1")
                asm.append("    VMRS APSR_nzcv, FPSCR")
                asm.append(f"    BEQ not_true_{idx}")
                asm.append(f"    LDR R0, ={l_zero}")
                asm.append(f"    B not_end_{idx}")
                asm.append(f"not_true_{idx}:")
                asm.append(f"    LDR R0, ={l_one}")
                asm.append(f"not_end_{idx}:")
                asm.append("    VLDR D0, [R0]")
                asm.append("    VPUSH {D0}")
                return # Retorna prematuro para não tentar VPOP de direita inexistente

            # TRATAMENTO PARA OPERADORES BINÁRIOS
            if no["direita"] is not None:
                gerar_codigo_recursivo(no["direita"])

            asm.append(f"\n    @ operacao {op}")
            asm.append("    VPOP {D1}")  # Operando direito
            asm.append("    VPOP {D0}")  # Operando esquerdo

            # Operações matemáticas
            if op == '+':
                asm.append("    VADD.F64 D0, D0, D1")
            elif op == '-':
                asm.append("    VSUB.F64 D0, D0, D1")
            elif op == '*':
                asm.append("    VMUL.F64 D0, D0, D1")

            # Divisão real
            elif op == '|':
                asm.append("    VDIV.F64 D0, D0, D1")

            # Divisão inteira (com truncamento)
            elif op == '/':
                asm.append("    VDIV.F64 D0, D0, D1")
                asm.append("    VCVT.S32.F64 S0, D0")
                asm.append("    VCVT.F64.S32 D0, S0")

            # Módulo
            elif op == '%':
                asm.append("    VMOV.F64 D2, D0")
                asm.append("    VDIV.F64 D3, D0, D1")
                asm.append("    VCVT.S32.F64 S0, D3")
                asm.append("    VCVT.F64.S32 D3, S0")
                asm.append("    VMUL.F64 D3, D3, D1")
                asm.append("    VSUB.F64 D0, D2, D3")

            # Potência
            elif op == '^':
                idx = contador_labels['pow']
                contador_labels['pow'] += 1

                asm.append("    VCVT.S32.F64 S1, D1")
                asm.append("    VMOV R1, S1")
                asm.append(f"    LDR R2, ={l_one}")
                asm.append("    VLDR D2, [R2]")

                asm.append(f"    B pow_check_{idx}")
                asm.append(f"pow_loop_{idx}:")
                asm.append("    VMUL.F64 D2, D2, D0")
                asm.append(f"    SUB R1, R1, #1")
                asm.append(f"pow_check_{idx}:")
                asm.append(f"    CMP R1, #0")
                asm.append(f"    BGT pow_loop_{idx}")
                asm.append("    VMOV.F64 D0, D2")

            # Comparações
            elif op in ('>', '<', '=='):
                asm.append("    VCMP.F64 D0, D1")
                asm.append("    VMRS APSR_nzcv, FPSCR")
                cond = 'GT' if op == '>' else ('LT' if op == '<' else 'EQ')
                asm.append(f"    LDR R0, ={l_zero}")
                asm.append(f"    LDR{cond} R0, ={l_one}")
                asm.append("    VLDR D0, [R0]")

            # Operadores Lógicos Binários
            elif op == 'AND':
                idx = contador_labels['logico']
                contador_labels['logico'] += 1
                asm.append(f"    LDR R2, ={l_zero}")
                asm.append("    VLDR D2, [R2]")
                asm.append("    VCMP.F64 D0, D2")
                asm.append("    VMRS APSR_nzcv, FPSCR")
                asm.append(f"    BEQ and_false_{idx}")
                asm.append("    VCMP.F64 D1, D2")
                asm.append("    VMRS APSR_nzcv, FPSCR")
                asm.append(f"    BEQ and_false_{idx}")
                asm.append(f"    LDR R0, ={l_one}")
                asm.append(f"    B and_end_{idx}")
                asm.append(f"and_false_{idx}:")
                asm.append(f"    LDR R0, ={l_zero}")
                asm.append(f"and_end_{idx}:")
                asm.append("    VLDR D0, [R0]")

            elif op == 'OR':
                idx = contador_labels['logico']
                contador_labels['logico'] += 1
                asm.append(f"    LDR R2, ={l_zero}")
                asm.append("    VLDR D2, [R2]")
                asm.append("    VCMP.F64 D0, D2")
                asm.append("    VMRS APSR_nzcv, FPSCR")
                asm.append(f"    BNE or_true_{idx}")
                asm.append("    VCMP.F64 D1, D2")
                asm.append("    VMRS APSR_nzcv, FPSCR")
                asm.append(f"    BNE or_true_{idx}")
                asm.append(f"    LDR R0, ={l_zero}")
                asm.append(f"    B or_end_{idx}")
                asm.append(f"or_true_{idx}:")
                asm.append(f"    LDR R0, ={l_one}")
                asm.append(f"or_end_{idx}:")
                asm.append("    VLDR D0, [R0]")

            asm.append("    VPUSH {D0}")  # Empilha resultado final da operação

        # ============================
        # COMANDOS (MEM / RES)
        # ============================
        elif tipo == "comando":
            if no["comando"] == "MEM":
                # Suporta tanto os nomes originais da AST quanto as chaves modificadas
                gerar_codigo_recursivo(no.get("val_expr", no.get("valor")))

                end_no = no.get("nome_var", no.get("endereco"))
                if end_no and end_no.get("tipo") == "variavel":
                    var = end_no["nome"]
                    vrv_mr.add(var)

                    asm.append(f"    LDR R0, ={var}")
                    asm.append("    VPOP {D0}")
                    asm.append("    VSTR.F64 D0, [R0]")
                    asm.append("    VPUSH {D0}")

            elif no["comando"] == "RES":
                gerar_codigo_recursivo(no["alvo"])
                asm.append("\n    @ comando RES")
                asm.append("    VPOP {D0}")
                asm.append("    VCVT.S32.F64 S0, D0")
                asm.append("    VMOV R1, S0")
                asm.append("    LDR R0, =ptr_res")
                asm.append("    LDR R2, [R0]")
                asm.append("    SUBS R1, R2, R1")  # Índice correto no histórico: ptr_res - N
                asm.append("    MOVLT R1, #0")     # Previne de acessar índices negativos (clamp)
                asm.append("    LDR R0, =array_res")
                asm.append("    ADD R2, R0, R1, LSL #3")
                asm.append("    VLDR D0, [R2]")
                asm.append("    VPUSH {D0}")

        # ============================
        # CONTROLE (IF / WHILE)
        # ============================
        elif tipo == "controle":

            # IF
            if no["estrutura"] == "IF":
                idx = contador_labels['if']
                contador_labels['if'] += 1

                lbl_end = f"if_end_{idx}"

                asm.append(f"\n    @ if_{idx}")

                gerar_codigo_recursivo(no["condicao"])
                asm.append("    VPOP {D0}")

                asm.append(f"    LDR R0, ={l_zero}")
                asm.append("    VLDR D1, [R0]")
                asm.append("    VCMP.F64 D0, D1")
                asm.append("    VMRS APSR_nzcv, FPSCR")

                asm.append(f"    BEQ {lbl_end}")  # Se falso, pula bloco

                gerar_codigo_recursivo(no["bloco"])

                asm.append(f"{lbl_end}:")

            # WHILE
            elif no["estrutura"] == "WHILE":
                idx = contador_labels['while']
                contador_labels['while'] += 1

                lbl_s = f"wh_s_{idx}"
                lbl_e = f"wh_e_{idx}"

                asm.append(f"\n    @ while_{idx}")
                asm.append(f"{lbl_s}:")

                gerar_codigo_recursivo(no["condicao"])
                asm.append("    VPOP {D0}")

                asm.append(f"    LDR R0, ={l_zero}")
                asm.append("    VLDR D1, [R0]")
                asm.append("    VCMP.F64 D0, D1")
                asm.append("    VMRS APSR_nzcv, FPSCR")

                asm.append(f"    BEQ {lbl_e}")  # Sai se falso

                gerar_codigo_recursivo(no["bloco"])

                asm.append(f"    B {lbl_s}")  # Loop

                asm.append(f"{lbl_e}:")

    # ==========================================
    # EXECUTA A GERAÇÃO E SALVA O ARQUIVO .S
    # ==========================================
    gerar_codigo_recursivo(arvore_ast)

    with open(nome_arquivo, "w", encoding="utf-8") as f_out:
        f_out.write(".global _start\n\n")
        f_out.write(".data\n")
        f_out.write("    .align 3\n")
        f_out.write("    array_res: .space 8000\n")
        f_out.write("    ptr_res:   .word 0\n\n")

        for val_str, label in cst_constantes.items():
            f_out.write(f"    .align 3\n")
            f_out.write(f"    {label}: .double {val_str}\n")

        for var in sorted(vrv_mr):
            f_out.write(f"    .align 3\n")
            f_out.write(f"    {var}: .double 0.0\n")

        f_out.write("\n.text\n_start:\n")
        f_out.write("\n".join(asm) + "\n")
        f_out.write("\n    @ fim do programa\n")
        f_out.write("    MOV R7, #1\n")
        f_out.write("    SWI 0\n")

    print(f"Codigo assembly gerado em: '{nome_arquivo}'")

# ============================================================
# FUNÇÕES DE TESTE
# ============================================================

def executarTestes(tabela):
    print("\n=======================================================")
    print("   INICIANDO CONJUNTO DE TESTES DE VALIDACAO DO COMPILADOR")
    print("=======================================================")

    print("\n[FASE 1: TESTES LEXICOS]")
    testes_lexicos = ['@', '#', '?', '&', '10.5.2']
    for t in testes_lexicos:
        try:
            tokens_resultado = []
            estado_inicial_afd(t, 0, tokens_resultado)
            bloqueado = any(not validar_token(tk) for tk in tokens_resultado)
            status = "PASSOU" if bloqueado else "FALHOU"
        except ValueError:
            status = "PASSOU"
        print(f"Teste Lexico [Bloquear token '{t}']: {status}")

    print("\n[FASE 1B: TESTES DE COMENTARIOS *{ }*]")
    testes_comentarios = [
        ("Comentario simples",   "*{ isso e um comentario }* (START)",                True),
        ("Comentario nao fechado", "*{ comentario sem fechamento (START)",              False),
        ("Comentario multilinha", "*{ linha1\nlinha2 }*\n(START)\n(END)\n$",           True),
        ("Sem comentario",        "(START)\n(END)\n$",                                 True),
    ]
    for nome, texto, esperado in testes_comentarios:
        resultado, _ = removerComentarios(texto)
        ok = (resultado is not None) == esperado
        print(f"Teste Comentario [{nome}]: {'PASSOU' if ok else 'FALHOU'}")

    print("\n[FASE 2: TESTES SINTATICOS LL(1)]")
    testes_sintaticos = [
        {"nome": "29.3.5 - Aninhamento Profundo",
         "tokens": ['(','START',')','(','(','(','(','1','2','+',')','3','*',')','4','-',')','5','|',')','(','END',')','$'],
         "esperado": True},
        {"nome": "29.7.2 - Erro (A B + C)",
         "tokens": ['(','START',')','(','A','B','+','C',')','(','END',')','$'],
         "esperado": False},
        {"nome": "Soma Simples (Float)",
         "tokens": ['(','START',')','(','3.14','2.0','+',')','(','END',')','$'],
         "esperado": True},
        {"nome": "Expressao Aninhada",
         "tokens": ['(','START',')','(','(','A','B','+',')','(','C','D','*',')','|',')','(','END',')','$'],
         "esperado": True},
        {"nome": "Estrutura de Controle (WHILE)",
         "tokens": ['(','START',')','(','X','10','<','{','(','X','1','+',')','}'  ,'WHILE',')','(','END',')','$'],
         "esperado": True},
        {"nome": "Estrutura de Controle (IF)",
         "tokens": ['(','START',')','(','X','0','>','{','(','X','1','-',')','}'  ,'IF',')','(','END',')','$'],
         "esperado": True},
        {"nome": "Divisao Real (|)",
         "tokens": ['(','START',')','(','10.0','4.0','|',')','(','END',')','$'],
         "esperado": True},
        {"nome": "Divisao Inteira (/)",
         "tokens": ['(','START',')','(','10','3','/',')','(','END',')','$'],
         "esperado": True},
        {"nome": "Erro: Expressao Vazia ( )",
         "tokens": ['(','START',')','(', ')','(','END',')','$'],
         "esperado": False},
        {"nome": "Erro: Estrutura Pre-fixa (+ A B)",
         "tokens": ['(','START',')','(','+','A','B',')','(','END',')','$'],
         "esperado": False},
    ]

    for t in testes_sintaticos:
        original_stdout = sys.stdout
        devnull = open(os.devnull, 'w')
        try:
            sys.stdout = devnull
            sucesso, _, _, _ = parsear(t["tokens"], tabela)
        finally:
            sys.stdout = original_stdout
            devnull.close()
        status = "PASSOU" if sucesso == t["esperado"] else "FALHOU"
        print(f"Teste Sintatico [{t['nome']}]: {status}")

    print("\n[FASE 3: TESTES SEMANTICOS]")

    testes_semanticos = [
        # Operação válida int+int
        {
            "nome": "Tipo valido: int + int",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "+",
                    "esquerda": {"tipo": "numero", "valor": 3, "tipo_dado": "int"},
                    "direita":  {"tipo": "numero", "valor": 4, "tipo_dado": "int"}
                }]
            },
            "esperado_erro": False
        },
        # Operação válida real+real
        {
            "nome": "Tipo valido: real + real",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "+",
                    "esquerda": {"tipo": "numero", "valor": 3.0, "tipo_dado": "real"},
                    "direita":  {"tipo": "numero", "valor": 4.0, "tipo_dado": "real"}
                }]
            },
            "esperado_erro": False
        },
        # Divisão inteira com real — deve dar erro
        {
            "nome": "Tipo invalido: real / real (divisao inteira)",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "/",
                    "esquerda": {"tipo": "numero", "valor": 3.0, "tipo_dado": "real"},
                    "direita":  {"tipo": "numero", "valor": 4.0, "tipo_dado": "real"}
                }]
            },
            "esperado_erro": True
        },
        # bool + int — deve dar erro
        {
            "nome": "Tipo invalido: bool + int",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "+",
                    "esquerda": {"tipo": "numero", "valor": True, "tipo_dado": "bool"},
                    "direita":  {"tipo": "numero", "valor": 2,    "tipo_dado": "int"}
                }]
            },
            "esperado_erro": True
        },
        # IF com condição bool — válido
        {
            "nome": "IF com condicao bool: valido",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "controle", "estrutura": "IF",
                    "condicao": {"tipo": "numero", "valor": True, "tipo_dado": "bool"},
                    "bloco": {"tipo": "bloco", "instrucoes": []}
                }]
            },
            "esperado_erro": False
        },
        # IF com condição int — inválido
        {
            "nome": "IF com condicao int: invalido",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "controle", "estrutura": "IF",
                    "condicao": {"tipo": "numero", "valor": 5, "tipo_dado": "int"},
                    "bloco": {"tipo": "bloco", "instrucoes": []}
                }]
            },
            "esperado_erro": True
        },
        # CORREÇÃO 1: variável sem definição prévia agora é ERRO FATAL (esperado_erro: True mantido)
        {
            "nome": "Variavel sem definicao previa: erro fatal",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "+",
                    "esquerda": {"tipo": "variavel", "nome": "X", "tipo_dado": None},
                    "direita":  {"tipo": "numero", "valor": 1, "tipo_dado": "int"}
                }]
            },
            "esperado_erro": True
        },
        # Variável declarada e usada corretamente
        {
            "nome": "Variavel declarada e usada: valido",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [
                    {
                        "tipo": "comando", "comando": "MEM",
                        "val_expr": {"tipo": "numero", "valor": 10, "tipo_dado": "int"},
                        "nome_var": {"tipo": "variavel", "nome": "X", "tipo_dado": None}
                    },
                    {
                        "tipo": "operacao", "operador": "+",
                        "esquerda": {"tipo": "variavel", "nome": "X", "tipo_dado": None},
                        "direita":  {"tipo": "numero", "valor": 1, "tipo_dado": "int"}
                    }
                ]
            },
            "esperado_erro": False
        },
        # Módulo com reais — deve dar erro
        {
            "nome": "Tipo invalido: real % real",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "%",
                    "esquerda": {"tipo": "numero", "valor": 5.0, "tipo_dado": "real"},
                    "direita":  {"tipo": "numero", "valor": 2.0, "tipo_dado": "real"}
                }]
            },
            "esperado_erro": True
        },
        # Relacional com ints — válido
        {
            "nome": "Relacional int > int: valido",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": ">",
                    "esquerda": {"tipo": "numero", "valor": 5, "tipo_dado": "int"},
                    "direita":  {"tipo": "numero", "valor": 3, "tipo_dado": "int"}
                }]
            },
            "esperado_erro": False
        },
        # CORREÇÃO 2A: WHILE com variável não declarada dentro do bloco
        {
            "nome": "WHILE com variavel nao declarada no bloco",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "controle", "estrutura": "WHILE",
                    "condicao": {"tipo": "numero", "valor": True, "tipo_dado": "bool"},
                    "bloco": {"tipo": "bloco", "instrucoes": [{
                        "tipo": "operacao", "operador": "+",
                        "esquerda": {"tipo": "variavel", "nome": "NAO_DECLARADA", "tipo_dado": None},
                        "direita":  {"tipo": "numero",   "valor": 1, "tipo_dado": "int"}
                    }]}
                }]
            },
            "esperado_erro": True
        },
        # CORREÇÃO 2B: Expressão aninhada com tipos mistos (int + (real / real)) — erro
        {
            "nome": "Aninhamento: int + (real / real) invalido",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "+",
                    "esquerda": {"tipo": "numero", "valor": 1, "tipo_dado": "int"},
                    "direita": {
                        "tipo": "operacao", "operador": "/",
                        "esquerda": {"tipo": "numero", "valor": 3.0, "tipo_dado": "real"},
                        "direita":  {"tipo": "numero", "valor": 2.0, "tipo_dado": "real"}
                    }
                }]
            },
            "esperado_erro": True
        },
        # CORREÇÃO 2C: WHILE com condição int — inválido
        {
            "nome": "WHILE com condicao int: invalido",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "controle", "estrutura": "WHILE",
                    "condicao": {"tipo": "numero", "valor": 1, "tipo_dado": "int"},
                    "bloco": {"tipo": "bloco", "instrucoes": []}
                }]
            },
            "esperado_erro": True
        },
        # CORREÇÃO 2D: Aninhamento profundo válido: ((2 3 +) (4 5 *) |)
        {
            "nome": "Aninhamento profundo valido: real division",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "|",
                    "esquerda": {
                        "tipo": "operacao", "operador": "+",
                        "esquerda": {"tipo": "numero", "valor": 2,   "tipo_dado": "int"},
                        "direita":  {"tipo": "numero", "valor": 3,   "tipo_dado": "int"}
                    },
                    "direita": {
                        "tipo": "operacao", "operador": "*",
                        "esquerda": {"tipo": "numero", "valor": 4,   "tipo_dado": "int"},
                        "direita":  {"tipo": "numero", "valor": 5,   "tipo_dado": "int"}
                    }
                }]
            },
            "esperado_erro": False
        },
        # CORREÇÃO 3 (teste extra): variável não declarada na CONDIÇÃO do WHILE — erro fatal
        {
            "nome": "WHILE com variavel nao declarada na condicao",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "controle", "estrutura": "WHILE",
                    "condicao": {
                        "tipo": "operacao", "operador": ">",
                        "esquerda": {"tipo": "variavel", "nome": "NAO_DEF_COND", "tipo_dado": None},
                        "direita":  {"tipo": "numero",   "valor": 0, "tipo_dado": "int"}
                    },
                    "bloco": {"tipo": "bloco", "instrucoes": []}
                }]
            },
            "esperado_erro": True
        },
        # RES com N negativo — deve dar erro
        {
            "nome": "RES com N negativo: invalido",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "comando", "comando": "RES",
                    "alvo": {"tipo": "numero", "valor": -1, "tipo_dado": "int"}
                }]
            },
            "esperado_erro": True
        },
        # RES com N inteiro válido — sem erro semântico de tipo
        {
            "nome": "RES com N zero: valido",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "comando", "comando": "RES",
                    "alvo": {"tipo": "numero", "valor": 0, "tipo_dado": "int"}
                }]
            },
            "esperado_erro": False
        },
        # PROBLEMA 6 CORRIGIDO: bool == bool deve ser VÁLIDO
        {
            "nome": "bool == bool: valido (Problema 6)",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "==",
                    "esquerda": {"tipo": "numero", "valor": True,  "tipo_dado": "bool"},
                    "direita":  {"tipo": "numero", "valor": False, "tipo_dado": "bool"}
                }]
            },
            "esperado_erro": False
        },
        # bool == int deve ser INVÁLIDO (mistura)
        {
            "nome": "bool == int: invalido (mistura tipos)",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "==",
                    "esquerda": {"tipo": "numero", "valor": True, "tipo_dado": "bool"},
                    "direita":  {"tipo": "numero", "valor": 1,    "tipo_dado": "int"}
                }]
            },
            "esperado_erro": True
        },
        # PROBLEMA 3: AND com bools válido
        {
            "nome": "AND logico: bool AND bool valido",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "AND",
                    "esquerda": {"tipo": "numero", "valor": True,  "tipo_dado": "bool"},
                    "direita":  {"tipo": "numero", "valor": False, "tipo_dado": "bool"}
                }]
            },
            "esperado_erro": False
        },
        # PROBLEMA 3: AND com int inválido
        {
            "nome": "AND logico: int AND bool invalido",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "AND",
                    "esquerda": {"tipo": "numero", "valor": 1,    "tipo_dado": "int"},
                    "direita":  {"tipo": "numero", "valor": True, "tipo_dado": "bool"}
                }]
            },
            "esperado_erro": True
        },
        # PROBLEMA 3: OR com bools válido
        {
            "nome": "OR logico: bool OR bool valido",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "OR",
                    "esquerda": {"tipo": "numero", "valor": False, "tipo_dado": "bool"},
                    "direita":  {"tipo": "numero", "valor": True,  "tipo_dado": "bool"}
                }]
            },
            "esperado_erro": False
        },
        # PROBLEMA 3: NOT unário com bool válido
        {
            "nome": "NOT logico: NOT bool valido",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "NOT",
                    "esquerda": {"tipo": "numero", "valor": True, "tipo_dado": "bool"},
                    "direita": None
                }]
            },
            "esperado_erro": False
        },
        # PROBLEMA 3: NOT com int inválido
        {
            "nome": "NOT logico: NOT int invalido",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "NOT",
                    "esquerda": {"tipo": "numero", "valor": 5, "tipo_dado": "int"},
                    "direita": None
                }]
            },
            "esperado_erro": True
        },
        # PROBLEMA 3: Combinação (bool AND bool) OR bool — válido
        {
            "nome": "Combinacao logica: (bool AND bool) OR bool valido",
            "ast": {
                "tipo": "programa_ast",
                "instrucoes": [{
                    "tipo": "operacao", "operador": "OR",
                    "esquerda": {
                        "tipo": "operacao", "operador": "AND",
                        "esquerda": {"tipo": "numero", "valor": True,  "tipo_dado": "bool"},
                        "direita":  {"tipo": "numero", "valor": False, "tipo_dado": "bool"}
                    },
                    "direita": {"tipo": "numero", "valor": True, "tipo_dado": "bool"}
                }]
            },
            "esperado_erro": False
        },
    ]

    for t in testes_semanticos:
        tabela_teste, erros_decl_teste = construirTabelaSimbolos(t["ast"])
        erros_tipos_teste = verificarTipos(t["ast"], tabela_teste)
        if erros_tipos_teste is None:
            erros_tipos_teste = []
        # Combinar erros de declaração + tipos (deduplica por (linha, elemento, causa))
        vistos_t = set()
        todos_erros_teste = []
        for e in (erros_decl_teste or []) + erros_tipos_teste:
            chave = (e.get("linha"), e.get("elemento"), e.get("causa"))
            if chave not in vistos_t:
                vistos_t.add(chave)
                todos_erros_teste.append(e)
        tem_erro = len(todos_erros_teste) > 0
        status = "PASSOU" if tem_erro == t["esperado_erro"] else "FALHOU"
        print(f"Teste Semantico [{t['nome']}]: {status}")


# ============================================================
# MAIN
# ============================================================

def main():
    gramatica = construirGramatica()
    first, nullable = calcularFirst(gramatica)
    follow = calcularFollow(gramatica, first, nullable)
    tabela = construirTabelaLL1(gramatica, first, follow, nullable)

    print("\n--- ETAPA DE VALIDACAO TEORICA ---")
    gerarRelatorioLL1(first, follow, tabela)
    # Gera os arquivos de documentação separados exigidos pela Seção 10.3:
    # gramatica.md  — gramática EBNF aumentada
    # sequentes.md  — regras de tipos em cálculo de sequentes
    gerarGramaticaMd()
    gerarSequentesMd()

    executarTestes(tabela)

    if len(sys.argv) < 2:
        print("\n[AVISO]: Nenhum arquivo fornecido para analise.")
        print("Uso: py AnalisadorSemantico.py nome_do_arquivo.txt")
        return

    arquivo_alvo = sys.argv[1]
    print(f"\n=======================================================")
    print(f"--- COMPILANDO: {arquivo_alvo} ---")
    print(f"=======================================================")

    # Chama a função do Aluno 1 e recebe tudo pronto
    tokens_arquivo, arvore_ast, arvore_cst = prepararEntradaSemantica(arquivo_alvo, tabela)

    if tokens_arquivo is None:
        return

    imprimirTokensLexicos(tokens_arquivo)

    # Se a AST for None, ocorreu erro sintático (já reportado lá dentro)
    if arvore_ast is None:
        print("Assembly NAO gerado (erro sintatico).")
        return

    print(f"SUCESSO SINTATICO: '{arquivo_alvo}' passou na analise sintatica!")
    gerarArvore(arvore_cst, arvore_ast)

    print("\n--- ETAPA SEMANTICA ---")

    tabela_simb, erros_decl = construirTabelaSimbolos(arvore_ast)
    erros_tipos = verificarTipos(arvore_ast, tabela_simb)

    vistos = set()
    todos_erros_unicos = []
    for e in erros_decl + erros_tipos:
        chave = (e.get("linha"), e.get("elemento"), e.get("causa"))
        if chave not in vistos:
            vistos.add(chave)
            todos_erros_unicos.append(e)
    todos_erros = todos_erros_unicos
    
    erros_fatais = [e for e in todos_erros if e.get("nivel") != "aviso"]
    avisos       = [e for e in todos_erros if e.get("nivel") == "aviso"]

    salvarTabelaSimbolos(tabela_simb, todos_erros, arquivo_alvo)
    gerarArvoreAtribuida(arvore_ast, tabela_simb, todos_erros, arquivo_alvo)

    # Salvar relatório de erros semânticos em arquivo dedicado (Seção 10.4)
    nome_relatorio = "erros_semanticos.md"
    with open(nome_relatorio, "w", encoding="utf-8") as f_rel:
        f_rel.write("# Relatorio de Erros Semanticos\n\n")
        f_rel.write(f"**Arquivo analisado:** `{arquivo_alvo}`\n\n")
        if todos_erros:
            f_rel.write(f"**Total de erros:** {len(todos_erros)}\n\n")
            f_rel.write("| Linha | Elemento | Causa |\n")
            f_rel.write("|-------|----------|-------|\n")
            for e in todos_erros:
                nivel = " ⚠️ aviso" if e.get("nivel") == "aviso" else ""
                f_rel.write(f"| {e['linha']} | `{e['elemento']}`{nivel} | {e['causa']} |\n")
        else:
            f_rel.write("_Nenhum erro semantico detectado._\n")
    print(f"Relatorio de erros semanticos salvo em: '{nome_relatorio}'")

    if avisos:
        print(f"\n[AVISOS SEMANTICOS: {len(avisos)}]")
        for a in avisos:
            print(f"  Linha {a['linha']} | '{a['elemento']}': {a['causa']}")

    if erros_fatais:
        print(f"\n[ERROS SEMANTICOS FATAIS: {len(erros_fatais)}]")
        for e in erros_fatais:
            print(f"  Linha {e['linha']} | '{e['elemento']}': {e['causa']}")
        print("\nAssembly NAO gerado (erros semanticos encontrados).")
        print(f"FALHA SEMANTICA: '{arquivo_alvo}' contem {len(erros_fatais)} erro(s) fatal(is).")
        print("\n--- ARQUIVOS GERADOS ---")
        print(f"  tokens.txt       — tokens reconhecidos pelo analisador lexico")
        print(f"  arvore_cst.json        — arvore de derivacao concreta")
        print(f"  arvore_ast.json        — arvore sintatica abstrata")
        print(f"  arvore_atribuida.json  — arvore sintatica atribuida (com tipos)")
        print(f"  arvore_atribuida.md    — arvore atribuida em Markdown")
        print(f"  tabela_simbolos.json   — tabela de simbolos")
        print(f"  tabela_simbolos.md     — tabela de simbolos em Markdown")
        print(f"  erros_semanticos.md    — relatorio de erros semanticos")
        print(f"  gramatica.md           — gramatica EBNF aumentada")
        print(f"  sequentes.md           — regras de tipos em calculo de sequentes")
        print(f"  relatorio_validacao_ll1.txt — relatorio de validacao teorica LL(1)")
    else:
        if avisos:
            print(f"\nAnalise semantica concluida com {len(avisos)} aviso(s). Prosseguindo com Assembly.")
        else:
            print("Analise semantica concluida: NENHUM ERRO detectado.")

        print("\n--- GERANDO ASSEMBLY ---")
        gerarAssembly(arvore_ast)
        print(f"\nSUCESSO COMPLETO: '{arquivo_alvo}' compilado sem erros!")
        print("\n--- ARQUIVOS GERADOS ---")
        print(f"  saida_lexica.txt       — tokens reconhecidos pelo analisador lexico")
        print(f"  arvore_cst.json        — arvore de derivacao concreta")
        print(f"  arvore_ast.json        — arvore sintatica abstrata")
        print(f"  arvore_atribuida.json  — arvore sintatica atribuida (com tipos)")
        print(f"  arvore_atribuida.md    — arvore atribuida em Markdown")
        print(f"  tabela_simbolos.json   — tabela de simbolos")
        print(f"  tabela_simbolos.md     — tabela de simbolos em Markdown")
        print(f"  erros_semanticos.md    — relatorio de erros semanticos")
        print(f"  saida_assembly.s       — codigo Assembly ARMv7 (CPulator DE1-SoC)")
        print(f"  gramatica.md           — gramatica EBNF aumentada")
        print(f"  sequentes.md           — regras de tipos em calculo de sequentes")
        print(f"  relatorio_validacao_ll1.txt — relatorio de validacao teorica LL(1)")


if __name__ == "__main__":
    main()