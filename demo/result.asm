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

fact:
	slti $t1,$t1,temp1
	nor $t1,$t1,$zero
	xori $t0,$t1,temp1
	nor $t0,$t0,$zero
	and $t1,$t0,$t1
	nor $t1,$t1$zero
	bne $t1,$zero,label1
