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
	slti $t0,t0,temp1
	nor $t0,t0,$zero
	bne $temp2,$zero,label1
	j label2
label1:
	subi $t0,$t0,1
	addi $fp,$fp,-18
	sw $t0,0($fp)
	addi $fp,$fp,18
	sw $t1,4($fp)
	addi $fp,$fp,18
	sw $t2,8($fp)
	addi $fp,$fp,18
	sw $t3,12($fp)
	addi $fp,$fp,18
	sw $t4,16($fp)
	addi $fp,$fp,18
	sw $t5,20($fp)
	addi $fp,$fp,18
	sw $t6,24($fp)
	addi $fp,$fp,18
	sw $t7,28($fp)
	addi $fp,$fp,18
	sw $t8,32($fp)
	addi $fp,$fp,18
	sw $t9,36($fp)
	addi $fp,$fp,18
	sw $s0,40($fp)
	addi $fp,$fp,18
	sw $s1,44($fp)
	addi $fp,$fp,18
	sw $s2,48($fp)
	addi $fp,$fp,18
	sw $s3,52($fp)
	addi $fp,$fp,18
	sw $s4,56($fp)
	addi $fp,$fp,18
	sw $s5,60($fp)
	addi $fp,$fp,18
	sw $s6,64($fp)
	addi $fp,$fp,18
	sw $s7,68($fp)
	addi $fp,$fp,18
	addi $fp,$fp,-22
	sw $t0,0($fp)
	addi $fp,$fp,22
	jal fact
	addi $temp4,$v0,0
	mul $t0,$t0,t0
label2:
main:
	li $t0,0
label3:
	slt $t0,$t0,temp7
	bne $temp8,$zero,label4
	j label5
label4:
	li $t0,temp7
	li $t0,temp7
	addi $t0,$t0,1
	j label3
label5:
