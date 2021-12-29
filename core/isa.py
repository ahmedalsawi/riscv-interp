from collections import namedtuple
import re

from bitstring import Bits

def reg_to_index_bin(s):
    num = None
    # TODO implement rest of ABI
    if s[0] in  ["x", "a"]:
        num = int(s[1:])
    return '{0:05b}'.format(num)

def bin_to_hex(b, size = 8):
    i = int(b, 2)
    h = f"{i:0{size}x}"
    return h

def int_to_bin(i, size = 0):
    ii = int(i) # convert from int string to int
    b = Bits(int=ii, length=size)
    return b.bin

class Field:
    def __init__(self, name, len, value = None):
        self.name = name
        self.len = len
        self.value = value
    def __len__(self):
        return self.len
    def __str__(self):
        return f"{self.name}[{len(self)}] {self.value}"

class Intruction():
    def __init__(self, name):
        self.name = name
        self.type = ""
        self.hex_instruct = None
        self.asm_instruct = None

    def __str__(self):
        fields = '\n'.join([str(f) for f in self.fields])
        return f"{self.type} : {self.name} {fields}"

    def assemble(self):
        raise NotImplementedError()

class RTypeIntruction(Intruction):
    def __init__(self, name, opcode = None,func3= None, funct7  = None):
        Intruction.__init__(self, name)
        
        self.type ="R-type"

        self.fields = [
            Field("opcode",7,opcode),
            Field("rd",5),
            Field("funct3",3, func3),
            Field("rs1",5),
            Field("rs2",5),
            Field("funct7",7, funct7)
        ]

    def assemble(self, asm_instruct):
        self.asm_instruct = asm_instruct
        m = re.match(f'{self.name} ([a-z0-9]+),([a-z0-9]+),([a-z0-9]+)', asm_instruct)
        if m:
            self.fields[1].value = reg_to_index_bin(m.groups()[0])
            self.fields[3].value = reg_to_index_bin(m.groups()[1])
            self.fields[4].value = reg_to_index_bin(m.groups()[2])
            i = ''.join(f.value for f in reversed(self.fields))
        
            self.hex_instruct = bin_to_hex(i, 8)
            return self
        else:
            return None

class ITypeIntruction(Intruction):
    def __init__(self, name, opcode = None,func3= None):
        Intruction.__init__(self, name)
        self.type ="I-type"

        self.fields = [
            Field("opcode",7,opcode),
            Field("rd",5),
            Field("funct3",3, func3),
            Field("rs1",5),
            Field("imm[11:0]",12),
        ]

    def assemble(self, asm_instruct):
        self.asm_instruct = asm_instruct
        m = re.match(f'{self.name} ([a-z0-9]+),([a-z0-9]+),(.*)', asm_instruct)
        if m:
            self.fields[1].value = reg_to_index_bin(m.groups()[0])
            self.fields[3].value = reg_to_index_bin(m.groups()[1])
            self.fields[4].value = int_to_bin(m.groups()[2],12) 
            i = ''.join(f.value for f in reversed(self.fields))
        
            self.hex_instruct = bin_to_hex(i, 8)
            return self
        else:
            return None

class STypeIntruction(Intruction):
    def __init__(self, name, opcode = None,func3= None):
        Intruction.__init__(self, name)
        self.type ="S-type"
        
        self.fields = [
            Field("opcode",7,opcode),
            Field("imm[4:0]",5),
            Field("funct3",3, func3),
            Field("rs1",5),
            Field("rs2",5),
            Field("imm[11:5]",7),
        ]

    def assemble(self, asm_instruct):
        self.asm_instruct = asm_instruct
        # op rs2, offset(rs1)
        m = re.match(f'{self.name} ([a-z0-9]+),(.+)\(([a-z0-9]+)\)', asm_instruct)
        if m:
            self.fields[4].value = reg_to_index_bin(m.groups()[0]) # rs2
            self.fields[3].value = reg_to_index_bin(m.groups()[2]) # rs1
            imm = int_to_bin(m.groups()[1],12)
            self.fields[1].value = imm[7:11] #imm[4:0]
            self.fields[5].value = imm[0:6] # imm[11:5]
            i = ''.join(f.value for f in reversed(self.fields))
        
            self.hex_instruct = bin_to_hex(i, 8)
            return self
        else:
            return None


class BTypeIntruction(Intruction):
    def __init__(self, name, opcode = None,func3= None):
        Intruction.__init__(self, name)
        self.type ="B-type"
        
        self.fields = [
            Field("opcode",7,opcode),
            Field("imm[4:1|11]",5),
            Field("funct3",3, func3),
            Field("rs1",5),
            Field("rs2",5),
            Field("imm[12|10:5]",7),
        ]

    def assemble(self, asm_instruct):
        self.asm_instruct = asm_instruct
        # op rs2, offset(rs1)
        m = re.match(f'{self.name} ([a-z0-9]+),([a-z0-9]+),(.*)', asm_instruct)
        if m:
            self.fields[3].value = reg_to_index_bin(m.groups()[0]) # rs1
            self.fields[4].value = reg_to_index_bin(m.groups()[1]) # rs2
            """
            From the spec:
            All branch instructions use the B-type instruction format. The 12-bit B-immediate encodes signed
            offsets in multiples of 2 bytes. The offset is sign-extended and added to the address of the branch
            instruction to give the target address. The conditional branch range is ±4 KiB.
            
            00 01 02 03 04 05 06 07 08 09 10 11 12 13 
            13 12 11 10 09 08 07 06 05 04 03 02 01 00
            """
            imm = int_to_bin(m.groups()[2],13)
            self.fields[1].value = imm[9:12] + imm[2] #imm[4:1] + imm[11]
            self.fields[5].value = imm[1] + imm[3:8] # imm[12] + imm[10:5]
            i = ''.join(f.value for f in reversed(self.fields))
        
            self.hex_instruct = bin_to_hex(i, 8)
            return self
        else:
            return None

rv_isa = [
    RTypeIntruction("add",  "0110011", "000", "0000000"),
    RTypeIntruction("or",   "0110011", "110", "0000000"),
    ITypeIntruction("andi", "0010011", "000"),
    STypeIntruction("sb",   "0100011", "000"),
    BTypeIntruction("beq",  "0100011", "000"),

]

if __name__ == "__main__":

    code = [
        "add a2,x3,x4",
        "or x1,x2,x4",
        "andi x1,x2,8",
        "sb x1,-20(x2)",
        "beq x1,x2,-20",
    ]
    for asm in code:
        found = False
        for insformat in rv_isa:
            inst = insformat.assemble(asm)
            if inst:
                found = True
                print(inst)
                break
        if found == False:
            print("Error: asm not found")
        

