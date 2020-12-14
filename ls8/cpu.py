"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100
RET = 0b00010001
CALL = 0b01010000
FL = 6
SC = 7
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # flags for greater less and equal
        self.E = 0b00000001
        self.G = 0b00000010
        self.L = 0b00000100
        self.flags = {"e": False, "g": False, "l": False}
        #set array of 8 zeroes
        self.reg = [0] * 8
        #set array of 256 zeroes
        self.ram = [0] * 256
        #declaring special register for stack pointer
        self.reg[7] = len(self.ram) - 1
        self.reg[FL] = 0b00000000
        #program counter
        self.pc = 0
        #boolian for stopping the program and starting it.
        self.halted = False
        #Stack Counter
        self.sc = 0

        #return the element stored in the address of ram
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, val):
        #overwrite the value at the index provided
        self.ram[address] = val

    def load(self, filename):
        """Load a program into memory."""
        #address counter
        address = 0
        #passes the filename into the open function to be evaluated
        with open(filename) as fp:
            #for each line in the page
            for line in fp:
                #split the comment by # into a list
                comment_split = line.split("#")
                #removes any unnecisary spaces
                num = comment_split[0].strip()

                #if the number is a string
                if num == '':  # ignore blanks
                    continue
                #convert the value into an integer
                val = int(num, 2)
                self.ram_write(address, val)
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""# XXX:
        #if the operation is ADD
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')



    def run(self):
        """Run the CPU."""

        while not self.halted:

            #set variable to the value at the program counter in ram
            instruction_to_execute = self.ram_read(self.pc)

            #setting operands to the next two indexes in ram to the one being exicuted
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            #pass the current instruction and the next two lines through execute_instruction
            self.execute_instruction(instruction_to_execute, operand_a, operand_b)
            #print(self.pc)
            ##TODO##
            ##JMP JNE JEQ
    def execute_instruction(self, instruction, operand_a, operand_b):
        #if the insctruction is HLT stop the program and increase the counter

        if instruction == HLT:
            self.halted = True
            self.pc += 1
        #if sets flags for each different possible outcome
        #FL bits: 00000LGE
        elif instruction == CMP:
            #print(f'cmp operands: {self.reg[operand_a], self.reg[operand_b]}')

            if self.reg[operand_a] == self.reg[operand_b]:
                self.flags["e"] = True

            elif self.reg[operand_a] > self.reg[operand_b]:
                self.flags["g"] = True

            else:
                self.flags["l"] = True

            self.pc +=3

        #set pc to disired register
        elif instruction == JMP:

            self.pc = self.reg[operand_a]

        #set pc to desired register if the  equal flag is set to true
        elif instruction == JEQ:
            #print("jeq hit")
            if self.flags["e"] == True:
                #print("JEQ is true")
                self.pc = self.reg[operand_a]
                self.flags['e'] = False
            else:
                self.pc +=2

        #set pc to desired register if the equal flag is set to false
        elif instruction == JNE:
            if self.flags["e"] == False:
                #print("JNE is True")
                self.pc = self.reg[operand_a]
            else:
                self.pc +=2
        #if the instcruction is LDI set the value at self.reg[operand_a] equal to the second operand
        elif instruction == POP:

            val = self.ram[self.reg[SC] + 1]
            self.reg[SC] +=1
            self.reg[operand_a] = val
            self.pc +=2

        elif instruction == PUSH:
            self.ram[self.reg[SC]] = self.reg[operand_a]

            self.reg[SC] -= 1
            self.pc += 2

        elif instruction == LDI:
            self.reg[operand_a] = operand_b
            #print(self.reg[operand_a])
            self.pc += 3
        elif instruction == CALL:
            self.reg[operand_a]
        elif instruction == RET:
            pass
        #if the instrucstion is PRN then print the value in the provided register and move to the next command
        elif instruction == PRN:
            print(self.reg[operand_a])
            self.pc += 2
        #if the instruction is MUL set the value in the register[operand_a] equal to the prduct of the two registers provided
        elif instruction == MUL:
            print('mult hit')
            self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
            self.pc += 3
