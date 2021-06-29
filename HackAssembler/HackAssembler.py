
import os

address = '.../projects/HackAssembler/Pong.asm' 

class Parser:
    def __init__(self, address):
        with open(address, 'r') as f:
            content = f.readlines()
        newDoc = []
        for line in content:
            if not line.startswith('//'):
                if line == '\n':
                    continue
                else:
                    newDoc.append(line.partition('//')[0].strip())
        self.file = newDoc
        self.step = 0
        self.command = ''

    def hasMoreCommands(self):
        isMore = self.step
        try:
            self.file[isMore]
            return True
        except IndexError:
            return False

    def advance(self):
        try:
            if self.hasMoreCommands() == True:
                self.command = self.file[self.step]
                self.step += 1
                return
            else:
                return
        except:
            raise StopIteration
            return

    def commandType(self):
        compare = self.command
        if compare.startswith('@'):
            return 'A_COMMAND'
        elif compare.startswith('('):
            return 'L_COMMAND'
        elif ('=' in compare) or (';' in compare):
            return 'C_COMMAND'

    def symbol(self):
        compare = self.commandType()
        if compare == 'C_COMMAND':
            return
        else:
            if compare == 'A_COMMAND':
                if isinstance(self.command[1:2], int):
                    return self.command.strip('@R')
                else:
                    return self.command.strip('@')
            elif compare == 'L_COMMAND':
                return self.command.strip('()')

    def dest(self):
        if self.commandType() == 'C_COMMAND':
            compare = self.command
            if '=' in compare:
                return compare.split('=')[0]
            elif ';' in compare:
                return compare.split(';')[0]
        else:
            return

    def comp(self):
        if self.commandType() == 'C_COMMAND':
            compare = self.command
            if '=' in compare:
                return compare.split('=')[1]
            elif ';' in compare:
                return compare.split(';')[1]
        else:
            return

    def jump(self):
        if self.commandType() == 'C_COMMAND':
            compare = self.command
            if ';' in compare:
                return compare.split(';')[1]
        else:
            return

    def __str__(self):
        return str(self.file)

class Code(Parser):
    def __init__(self, address):
        super().__init__(address)

    def destBits(self):
        compType = self.command
        if ';' in compType:
            return '000'
        else:
            compare = self.dest()
            if compare != None:
                if compare == '0':
                    return '000'
                elif compare == 'M':
                    return '001'
                elif compare == 'D':
                    return '010'
                elif compare == 'MD':
                    return '011'
                elif compare == 'A':
                    return '100'
                elif compare == 'AM':
                    return '101'
                elif compare == 'AD':
                    return '110'
                elif compare == 'AMD':
                    return '111'

    def compBits(self):
        compType = self.command
        if '=' in compType:
            compare = self.comp()
            if 'M' in compare:
                if compare == 'M':
                    return '1110000'
                elif compare == '!M':
                    return '1110001'
                elif compare == '-M':
                    return '1110011'
                elif compare == 'M+1':
                    return '1110111'
                elif compare == 'M-1':
                    return '1110010'
                elif compare == 'D+M':
                    return '1000010'
                elif compare == 'D-M':
                    return '1010011'
                elif compare == 'M-D':
                    return '1000111'
                elif compare == 'D&M':
                    return '1000000'
                elif compare == 'D|M':
                    return '1010101'
            else:
                if compare == '0':
                    return '0101010'
                elif compare == '1':
                    return '0111111'
                elif compare == '-1':
                    return '0111010'
                elif compare == 'D':
                    return '0001100'
                elif compare == 'A':
                    return '0110000'
                elif compare == '!D':
                    return '0001101'
                elif compare == '!A':
                    return '0110001'
                elif compare == '-D':
                    return '0001111'
                elif compare == '-A':
                    return '0110011'
                elif compare == 'D+1':
                    return '0011111'
                elif compare == 'A+1':
                    return '0110111'
                elif compare == 'D-1':
                    return '0001110'
                elif compare == 'A-1':
                    return '0110010'
                elif compare == 'D+A':
                    return '0000010'
                elif compare == 'D-A':
                    return '0010011'
                elif compare == 'A-D':
                    return '0000111'
                elif compare == 'D&A':
                    return '0000000'
                elif compare == 'D|M':
                    return '0010101'
        elif ';' in compType:
            compare = self.dest()
            if 'M' in compare:
                if compare == 'M':
                    return '1110000'
            else:
                if compare == '0':
                    return '0101010'
                elif compare == '1':
                    return '0111111'
                elif compare == '-1':
                    return '0111010'
                elif compare == 'D':
                    return '0001100'
                elif compare == 'A':
                    return '0110000'

    def jumpBits(self):
        compare = self.jump()
        if compare != None:
            if compare == 'JGT':
                return '001'
            elif compare == 'JEQ':
                return '010'
            elif compare == 'JGE':
                return '011'
            elif compare == 'JLT':
                return '100'
            elif compare == 'JNE':
                return '101'
            elif compare == 'JLE':
                return '110'
            elif compare == 'JMP':
                return '111'
        if compare == None:
            return '000'

class SymbolTable(Code):
    def __init__(self, address):
        super().__init__(address)

    def Constructor(self):
        self.symbolTable = {'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6,
                            'R7':7, 'R8':8, 'R9':9, 'R10':10, 'R11':11, 'R12':12,
                            'R13':13, 'R14':14, 'R15':15, 'SCREEN':16384, 'KBD':24576,
                            'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4}
        return

    def addEntry(self, symb, addy):
        self.symbolTable[symb] = addy
        return

    def contains(self, symb):
        return symb in self.symbolTable

    def GetAddress(self, symb):
        return self.symbolTable.get(symb)

class HackAssembler(SymbolTable):
    def __init__(self, address):
        super().__init__(address)
        self.Constructor()
        self.holder = ''

    def firstPass(self):
        address = 0
        for idx in range(len(self.file)):
            self.advance()
            compare = self.symbol()
            if not self.contains(compare):
                if self.commandType() == 'L_COMMAND':
                    self.addEntry(compare, (address))
                    continue
                else:
                    address += 1
            elif self.contains(compare):
                address += 1
            else:
                continue
        return

    def cAssembler(self):
        concatenated = '111' + str(par.compBits()) + str(par.destBits()) + str(par.jumpBits())
        return concatenated

    def fullAssembler(self):
        self.firstPass()
        self.step = 0
        RAM = 16
        for idx in range(len(self.file)):
            try:
                self.advance()
                compare = self.commandType()
                if compare == 'A_COMMAND':
                    symbolStr = self.symbol()
                    try:
                        self.holder += '{0:016b}'.format(int(symbolStr)) + '\n'
                    except ValueError:
                        if not self.contains(symbolStr):
                            self.addEntry(symbolStr, RAM)
                            self.holder += '{0:016b}'.format(self.GetAddress(str(symbolStr))) + '\n'
                            RAM += 1
                        else:
                            self.holder += '{0:016b}'.format(self.GetAddress(str(symbolStr))) + '\n'
                elif compare == 'C_COMMAND':
                    self.holder += self.cAssembler() + '\n'

            except StopIteration:
                break
        write = address[:-3] + 'hack'
        with open(write, 'w') as out:
            out.write(par.holder)

        # os.system('open ' + write)    # Use with os import to create ''.txt doc.
        return

par = HackAssembler(address)
par.fullAssembler()


# User interface for receiving input for a given file.
#
# asmFile = input('Your assembler will now convert the file that you enter in the prompt:\n').strip()
# print('\n')
# while True:
#     try:
#         symbolTypeFile = input('Input "True" if you wish to include symbols. Otherwise select "False":\n')
#         if symbolTypeFile == 'True':
#             break
#         elif symbolTypeFile == 'False':
#             break
#         else:
#             raise TypeError
#     except TypeError:
#         print('This is not a valid Boolean input. Please try again.\n')
#         continue

# drive = asmFile
# drive = drive.lower()
# if symbolTypeFile == "False":
#     file = asmFile + 'L' + '.asm'
# else:
#     file = asmFile + '.asm'

# address = drive.strip() + '/'.strip() + file.strip()

# print('The file that you selected:')
# print(address)

