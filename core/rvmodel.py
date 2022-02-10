
from bitstring import Bits

class Register():
    def __init__(self):
        self.index = None
        self.names = []
        self.value = None

class GPRs():
    def __init__(self):
        self.gprs = []

        for index in range(32):
            self.gprs.append(index)

    def __str__(self):
        pass

class Memory():
    def __init__(self):
        pass
    def __str__(self):
        pass

class RVModel():
    def __init__(self):
        self.gpr    = GPRs()
        self.memory = Memory()

    def execute(self, asm):
        # asm: hex string
        pass
    def __str__(self):
        pass

if __name__ == "__main__":
    rvmodel = RVModel()
