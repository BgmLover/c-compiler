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
	bne $temp2,$zero,label1
	j label2
label1:
