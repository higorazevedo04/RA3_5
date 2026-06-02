.global _start

.data
    .align 3
    array_res: .space 8000
    ptr_res:   .word 0

    .align 3
    const_0: .double 0.0
    .align 3
    const_1: .double 1.0
    .align 3
    const_2: .double 20
    .align 3
    const_3: .double 10
    .align 3
    const_4: .double 5.5
    .align 3
    const_5: .double 2.0
    .align 3
    const_6: .double 5
    .align 3
    const_7: .double 0
    .align 3
    const_8: .double 1
    .align 3
    const_9: .double 2
    .align 3
    A: .double 0.0
    .align 3
    ALERTA: .double 0.0
    .align 3
    ANTERIOR: .double 0.0
    .align 3
    B: .double 0.0
    .align 3
    CONTADOR: .double 0.0
    .align 3
    DESLIGADO: .double 0.0
    .align 3
    DIV_INT: .double 0.0
    .align 3
    DIV_REAL: .double 0.0
    .align 3
    E_LOG: .double 0.0
    .align 3
    GRANDE: .double 0.0
    .align 3
    IGUAL: .double 0.0
    .align 3
    LIGADO: .double 0.0
    .align 3
    MOD_INT: .double 0.0
    .align 3
    MULT: .double 0.0
    .align 3
    OU_LOG: .double 0.0
    .align 3
    PEQUENO: .double 0.0
    .align 3
    POW: .double 0.0
    .align 3
    RAIO: .double 0.0
    .align 3
    RESULTADO_FINAL: .double 0.0
    .align 3
    SOMA: .double 0.0
    .align 3
    SUB: .double 0.0

.text
_start:
    LDR R0, =const_2
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =A
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_0
    .ltorg
skip_pool_0:
    LDR R0, =const_3
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =B
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_1
    .ltorg
skip_pool_1:
    LDR R0, =const_4
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =RAIO
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_2
    .ltorg
skip_pool_2:
    LDR R0, =const_1
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =LIGADO
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_3
    .ltorg
skip_pool_3:
    LDR R0, =A
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =B
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao +
    VPOP {D1}
    VPOP {D0}
    VADD.F64 D0, D0, D1
    VPUSH {D0}
    LDR R0, =SOMA
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_4
    .ltorg
skip_pool_4:
    LDR R0, =A
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =B
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao -
    VPOP {D1}
    VPOP {D0}
    VSUB.F64 D0, D0, D1
    VPUSH {D0}
    LDR R0, =SUB
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_5
    .ltorg
skip_pool_5:
    LDR R0, =A
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =B
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao *
    VPOP {D1}
    VPOP {D0}
    VMUL.F64 D0, D0, D1
    VPUSH {D0}
    LDR R0, =MULT
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_6
    .ltorg
skip_pool_6:
    LDR R0, =A
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =B
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao /
    VPOP {D1}
    VPOP {D0}
    VDIV.F64 D0, D0, D1
    VCVT.S32.F64 S0, D0
    VCVT.F64.S32 D0, S0
    VPUSH {D0}
    LDR R0, =DIV_INT
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_7
    .ltorg
skip_pool_7:
    LDR R0, =A
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =B
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao %
    VPOP {D1}
    VPOP {D0}
    VMOV.F64 D2, D0
    VDIV.F64 D3, D0, D1
    VCVT.S32.F64 S0, D3
    VCVT.F64.S32 D3, S0
    VMUL.F64 D3, D3, D1
    VSUB.F64 D0, D2, D3
    VPUSH {D0}
    LDR R0, =MOD_INT
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_8
    .ltorg
skip_pool_8:
    LDR R0, =A
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =B
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao ^
    VPOP {D1}
    VPOP {D0}
    VCVT.S32.F64 S1, D1
    VMOV R1, S1
    LDR R2, =const_1
    VLDR D2, [R2]
    B pow_check_0
pow_loop_0:
    VMUL.F64 D2, D2, D0
    SUB R1, R1, #1
pow_check_0:
    CMP R1, #0
    BGT pow_loop_0
    VMOV.F64 D0, D2
    VPUSH {D0}
    LDR R0, =POW
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_9
    .ltorg
skip_pool_9:
    LDR R0, =RAIO
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_5
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao |
    VPOP {D1}
    VPOP {D0}
    VDIV.F64 D0, D0, D1
    VPUSH {D0}
    LDR R0, =DIV_REAL
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_10
    .ltorg
skip_pool_10:
    LDR R0, =A
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =B
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao >
    VPOP {D1}
    VPOP {D0}
    VCMP.F64 D0, D1
    VMRS APSR_nzcv, FPSCR
    LDR R0, =const_0
    LDRGT R0, =const_1
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =GRANDE
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_11
    .ltorg
skip_pool_11:
    LDR R0, =A
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =B
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao <
    VPOP {D1}
    VPOP {D0}
    VCMP.F64 D0, D1
    VMRS APSR_nzcv, FPSCR
    LDR R0, =const_0
    LDRLT R0, =const_1
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =PEQUENO
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_12
    .ltorg
skip_pool_12:
    LDR R0, =A
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_2
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao ==
    VPOP {D1}
    VPOP {D0}
    VCMP.F64 D0, D1
    VMRS APSR_nzcv, FPSCR
    LDR R0, =const_0
    LDREQ R0, =const_1
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =IGUAL
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_13
    .ltorg
skip_pool_13:
    LDR R0, =LIGADO
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao NOT
    VPOP {D0}
    LDR R2, =const_0
    VLDR D1, [R2]
    VCMP.F64 D0, D1
    VMRS APSR_nzcv, FPSCR
    BEQ not_true_0
    LDR R0, =const_0
    B not_end_0
not_true_0:
    LDR R0, =const_1
not_end_0:
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =DESLIGADO
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_14
    .ltorg
skip_pool_14:
    LDR R0, =LIGADO
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =LIGADO
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao AND
    VPOP {D1}
    VPOP {D0}
    LDR R2, =const_0
    VLDR D2, [R2]
    VCMP.F64 D0, D2
    VMRS APSR_nzcv, FPSCR
    BEQ and_false_1
    VCMP.F64 D1, D2
    VMRS APSR_nzcv, FPSCR
    BEQ and_false_1
    LDR R0, =const_1
    B and_end_1
and_false_1:
    LDR R0, =const_0
and_end_1:
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =E_LOG
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_15
    .ltorg
skip_pool_15:
    LDR R0, =LIGADO
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =LIGADO
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao OR
    VPOP {D1}
    VPOP {D0}
    LDR R2, =const_0
    VLDR D2, [R2]
    VCMP.F64 D0, D2
    VMRS APSR_nzcv, FPSCR
    BNE or_true_2
    VCMP.F64 D1, D2
    VMRS APSR_nzcv, FPSCR
    BNE or_true_2
    LDR R0, =const_0
    B or_end_2
or_true_2:
    LDR R0, =const_1
or_end_2:
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =OU_LOG
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_16
    .ltorg
skip_pool_16:
    LDR R0, =const_6
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =CONTADOR
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_17
    .ltorg
skip_pool_17:

    @ while_0
wh_s_0:
    LDR R0, =CONTADOR
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_7
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao >
    VPOP {D1}
    VPOP {D0}
    VCMP.F64 D0, D1
    VMRS APSR_nzcv, FPSCR
    LDR R0, =const_0
    LDRGT R0, =const_1
    VLDR D0, [R0]
    VPUSH {D0}
    VPOP {D0}
    LDR R0, =const_0
    VLDR D1, [R0]
    VCMP.F64 D0, D1
    VMRS APSR_nzcv, FPSCR
    BEQ wh_e_0
    LDR R0, =CONTADOR
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_8
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao -
    VPOP {D1}
    VPOP {D0}
    VSUB.F64 D0, D0, D1
    VPUSH {D0}
    LDR R0, =CONTADOR
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_18
    .ltorg
skip_pool_18:

    @ if_0
    LDR R0, =CONTADOR
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_9
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao ==
    VPOP {D1}
    VPOP {D0}
    VCMP.F64 D0, D1
    VMRS APSR_nzcv, FPSCR
    LDR R0, =const_0
    LDREQ R0, =const_1
    VLDR D0, [R0]
    VPUSH {D0}
    VPOP {D0}
    LDR R0, =const_0
    VLDR D1, [R0]
    VCMP.F64 D0, D1
    VMRS APSR_nzcv, FPSCR
    BEQ if_end_0
    LDR R0, =const_1
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =ALERTA
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_19
    .ltorg
skip_pool_19:
if_end_0:

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_20
    .ltorg
skip_pool_20:
    B wh_s_0
wh_e_0:

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_21
    .ltorg
skip_pool_21:
    LDR R0, =const_8
    VLDR D0, [R0]
    VPUSH {D0}

    @ comando RES
    VPOP {D0}
    VCVT.S32.F64 S0, D0
    VMOV R1, S0
    LDR R0, =ptr_res
    LDR R2, [R0]
    SUBS R1, R2, R1
    MOVLT R1, #0
    LDR R0, =array_res
    ADD R2, R0, R1, LSL #3
    VLDR D0, [R2]
    VPUSH {D0}
    LDR R0, =ANTERIOR
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_22
    .ltorg
skip_pool_22:
    LDR R0, =A
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =B
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao *
    VPOP {D1}
    VPOP {D0}
    VMUL.F64 D0, D0, D1
    VPUSH {D0}
    LDR R0, =RESULTADO_FINAL
    VPOP {D0}
    VSTR.F64 D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ Despeja literal pool para evitar erro de limite de 4KB
    B skip_pool_23
    .ltorg
skip_pool_23:

    @ fim do programa
    MOV R7, #1
    SWI 0
