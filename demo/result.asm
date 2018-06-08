
.data
_prompt: .asciiz "Enter an integer:"
_ret: .asciiz "\n"
.globl main
.text
read:
    li $v0,4
    la $a0,_prompt
    syscall
    li $v0,5
    syscall
    jr $ra

print:
    li $v0,1
    syscall
    li $v0,4
    la $a0,_ret
    syscall
    move $v0,$0
    jr $ra
	move $v0,$t1
	jr $ra
	j label2
label1:
	move $v0,$t2
	jr $ra
label2:
label3:
	j label5
label4:
	j label3
label5:
	move $v0,$t2
	jr $ra
