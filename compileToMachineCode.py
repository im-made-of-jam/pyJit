# https://docs.python.org/3/library/dis.html#python-bytecode-instructions

import dis

# gets the CPython bytecode of a given python file
def getBytecodeOfFile(pathToFile: str):
    fileDump = ""
    with open(pathToFile, "r") as mainFile:
        for line in mainFile.readlines():
            fileDump += line

    a = compile(fileDump, pathToFile, "exec")

    b = dis.get_instructions(a, show_caches=True)
    return [c for c in b]

# turns one Python instrcution into x86-64 machine code
def getMachineCodeOfInstruction(instruction: dis.Instruction) -> list[int]:
    #! FOR FUTURE REFERENCE, ARGUMENTS GO FROM r15 -> r14 -> r13 AND SO ON
    #! ALL REGISTERS CAN BE CLOBBERED, IT IS A STACK MACHINE

    # everything on the main stack is either an int, float, or pointer, or some other data type that is always 64 bits
    # this simplifies everything greatly

    match instruction.opname:
        case "NOP":
            # nop
            return [0x90]

        case "POP_TOP" | "END_FOR":
            # add rsp, 8
            return [0x48, 0x83, 0xC4, 0x08]

        case "END_SEND":
            # pop   rax
            # pop   rcx
            # pop   rdx
            # push  rcx
            # push  rax
            return [0x58,
                    0x59,
                    0x5A,
                    0x51,
                    0x50]

        case "COPY":
            # shl   r15, 3
            # add   r15, rsp
            # push [r15]
            return [0x49, 0xC1, 0xE7, 0x03,
                    0x49, 0x01, 0xE7,
                    0x41, 0xFF, 0x37]

        case "SWAP":
            # shl   r15,  3
            # add   r15,  rsp
            # pop   r14
            # push [r15]
            # mov  [r15], r14
            return [0x49, 0xC1, 0xE7, 0x03,
                    0x49, 0x01, 0xE7,
                    0x41, 0x5E,
                    0X41, 0XFF, 0X37,
                    0X4D, 0X89, 0X37]

        case "CACHE":
            # nop
            return [0x90]

        case _:
            return []
