# https://docs.python.org/3/library/dis.html#python-bytecode-instructions

import dis

# cache compiled files so we dont have to compile them again and again and again
_compiledFiles = {}

# gets the CPython bytecode of a given python file
# if noCache is True then the file will be compiled again and the cached entry replaced
def getBytecodeOfFile(pathToFile: str, noCache=False):
    # check cache and use it if its there
    if (pathToFile in _compiledFiles.keys()) and (not noCache):
        return dis.get_instructions(_compiledFiles[pathToFile])

    # this is why the cache is used because this will be very *very* slow
    fileDump = ""
    with open(pathToFile, "r") as mainFile:
        for line in mainFile.readlines():
            fileDump += line

    # cant imagine this will be particularly fast either
    codeObject = compile(fileDump, pathToFile, "exec")

    # now the slow stuff is out of the way we can cache the compiled object
    _compiledFiles[pathToFile] = codeObject

    # got everything in terms of the code object so now we can get the instructions and were done
    b = dis.get_instructions(codeObject, show_caches=True)
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

        # 1 argument
        case "COPY":
            # shl   r15, 3
            # add   r15, rsp
            # push [r15]
            return [0x49, 0xC1, 0xE7, 0x03,
                    0x49, 0x01, 0xE7,
                    0x41, 0xFF, 0x37]

        # 1 argument
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

        case "UNARY_NEGATIVE":
            #TODO this
            return []

        case "UNARY_NOT":
            #TODO this
            return []

        case "UNARY_INVERT":
            #TODO this
            return []

        case "GET_ITER":
            #TODO this
            return []

        case "GET_YIELD_FROM_ITER":
            #TODO this
            return []

        case "TO_BOOL":
            #TODO this
            return []

        case "BINARY_OP":
            #TODO this
            return []

        case "STORE_SUBSCR":
            #TODO this
            return []

        case "DELETE_SUBSCR":
            #TODO this
            return []

        case "BINARY_SLICE":
            #TODO this
            return []

        case "STORE_SLICE":
            #TODO this
            return []

        # 1 argument
        case "GET_AWAITABLE":
            #TODO this
            return []

        case "GET_AITER":
            #TODO this
            return []

        case "GET_ANEXT":
            #TODO this
            return []

        case "END_ASYNC_FOR":
            #TODO this
            return []

        case "CLEANUP_THROW":
            #TODO this
            return []

        # 1 argument
        case "SET_ADD":
            #TODO this
            return []

        # 1 argument
        case "LIST_APPEND":
            #TODO this
            return []

        # 1 argument
        case "MAP_ADD":
            #TODO this
            return []

        case "RETURN_VALUE":
            #TODO this
            return []

        case "YIELD_VALUE":
            #TODO this
            return []

        case "SETUP_ANNOTATIONS":
            #TODO this
            return []

        case "POP_EXCEPT":
            #TODO this
            return []

        case "RERAISE":
            #TODO this
            return []

        case "PUSH_EXC_INFO":
            #TODO this
            return []

        case "CHECK_EXC_MATCH":
            #TODO this
            return []

        case "CHECK_EG_MATCH":
            #TODO this
            return []

        case "WITH_EXCEPT_START":
            #TODO this
            return []

        case "LOAD_COMMON_CONSTANT":
            #TODO this
            return []

        case "LOAD_BUILD_CLASS":
            #TODO this
            return []

        case "GET_LEN":
            #TODO this
            return []

        case "MATCH_MAPPING":
            #TODO this
            return []

        case "MATCH_SEQUENCE":
            #TODO this
            return []

        case "MATCH_KEYS":
            #TODO this
            return []

        # 1 argument
        case "STORE_NAME":
            #TODO this
            return []

        # 1 argument
        case "DELETE_NAME":
            #TODO this
            return []

        # 1 argument
        case "UNPACK_SEQUENCE":
            #TODO this
            return []

        # 1 argument
        case "UNPACK_EX":
            #TODO this
            return []

        # 1 argument
        case "STORE_ATTR":
            #TODO this
            return []

        # 1 argument
        case "DELETE_ATTR":
            #TODO this
            return []

        # 1 argument
        case "STORE_GLOBAL":
            #TODO this
            return []

        # 1 argument
        case "DELETE_GLOBAL":
            #TODO this
            return []

        # 1 argument
        case "LOAD_CONST":
            #TODO this
            return []

        # 1 argument
        case "LOAD_SMALL_INT":
            #TODO this
            return []

        # 1 argument
        case "LOAD_NAME":
            #TODO this
            return []

        case "LOAD_LOCALS":
            #TODO this
            return []

        # 1 argument
        case "LOAD_FROM_DICT_OR_GLOBALS":
            #TODO this
            return []

        case "BUILD_TEMPLATE":
            #TODO this
            return []

        # 1 argument
        case "BUILD_INTERPOLATION":
            #TODO this
            return []

        # 1 argument
        case "BUILD_TUPLE":
            #TODO this
            return []

        # 1 argument
        case "BUILD_LIST":
            #TODO this
            return []

        # 1 argument
        case "BUILD_SET":
            #TODO this
            return []

        # 1 argument
        case "BUILD_MAP":
            #TODO this
            return []

        # 1 argument
        case "BUILD_STRING":
            #TODO this
            return []

        # 1 argument
        case "LIST_EXTEND":
            #TODO this
            return []

        # 1 argument
        case "SET_UPDATE":
            #TODO this
            return []

        # 1 argument
        case "DICT_UPDATE":
            #TODO this
            return []

        # 1 argument
        case "DICT_MERGE":
            #TODO this
            return []

        # 1 argument
        case "LOAD_ATTR":
            #TODO this
            return []

        # 1 argument
        case "LOAD_SUPER_ATTR":
            #TODO this
            return []

        # 1 argument
        case "COMPARE_OP":
            #TODO this
            return []

        # 1 argument
        case "IS_OP":
            #TODO this
            return []

        # 1 argument
        case "CONTAINS_OP":
            #TODO this
            return []

        # 1 argument
        case "IMPORT_NAME":
            #TODO this
            return []

        # 1 argument
        case "IMPORT_FROM":
            #TODO this
            return []

        # 1 argument
        case "JUMP_FORWARD":
            #TODO this
            return []

        # 1 argument
        case "JUMP_BACKWARD":
            #TODO this
            return []

        # 1 argument
        case "JUMP_BACKWARD_NO_INTERRUPT":
            #TODO this
            return []

        # 1 argument
        case "POP_JUMP_IF_TRUE":
            #TODO this
            return []

        # 1 argument
        case "POP_JUMP_IF_FALSE":
            #TODO this
            return []

        # 1 argument
        case "POP_JUMP_IF_NOT_NONE":
            #TODO this
            return []

        # 1 argument
        case "POP_JUMP_IF_NONE":
            #TODO this
            return []

        # 1 argument
        case "FOR_ITER":
            #TODO this
            return []

        # 1 argument
        case "LOAD_GLOBAL":
            #TODO this
            return []

        # 1 argument
        case "LOAD_FAST":
            #TODO this
            return []

        # 1 argument
        case "LOAD_FAST_BORROW":
            #TODO this
            return []

        # 1 argument
        case "LOAD_FAST_LOAD_FAST":
            #TODO this
            return []

        # 1 argument
        case "LOAD_FAST_BORROW_LOAD_FAST_BORROW":
            #TODO this
            return []

        # 1 argument
        case "LOAD_FAST_CHECK":
            #TODO this
            return []

        # 1 argument
        case "LOAD_FAST_AND_CLEAR":
            #TODO this
            return []

        # 1 argument
        case "STORE_FAST":
            #TODO this
            return []

        # 1 argument
        case "STORE_FAST_STORE_FAST":
            #TODO this
            return []

        # 1 argument
        case "STORE_FAST_LOAD_FAST":
            #TODO this
            return []

        # 1 argument
        case "DELETE_FAST":
            #TODO this
            return []

        # 1 argument
        case "MAKE_CELL":
            #TODO this
            return []

        # 1 argument
        case "LOAD_DEREF":
            #TODO this
            return []

        # 1 argument
        case "LOAD_FROM_DICT_OR_DEREF":
            #TODO this
            return []

        # 1 argument
        case "STORE_DEREF":
            #TODO this
            return []

        # 1 argument
        case "DELETE_DEREF":
            #TODO this
            return []

        # 1 argument
        case "COPY_FREE_VARS":
            #TODO this
            return []

        # 1 argument
        case "RAISE_VARARGS":
            #TODO this
            return []

        # 1 argument
        case "CALL":
            #TODO this
            return []

        # 1 argument
        case "CALL_KW":
            #TODO this
            return []

        # 1 argument
        case "CALL_FUNCTION_EX":
            #TODO this
            return []

        case "PUSH_NULL":
            #TODO this
            return []

        case "MAKE_FUNCTION":
            #TODO this
            return []

        # 1 argument
        case "SET_FUNCTION_ATTRIBUTE":
            #TODO this
            return []

        # 1 argument
        case "BUILD_SLICE":
            #TODO this
            return []

        # 1 argument
        case "EXTENDED_ARG":
            #TODO this
            return []

        # 1 argument
        case "CONVERT_VALUE":
            #TODO this
            return []

        case "FORMAT_SIMPLE":
            #TODO this
            return []

        case "FORMAT_WITH_SPEC":
            #TODO this
            return []

        # 1 argument
        case "MATCH_CLASS":
            #TODO this
            return []

        # 1 argument
        case "RESUME":
            return [0x90]

        case "RETURN_GENERATOR":
            #TODO this
            return []

        # 1 argument
        case "SEND":
            #TODO this
            return []

        case "HAVE_ARGUMENT":
            #TODO this
            return []

        case "CALL_INTRINSIC_1":
            #TODO this
            return []

        case "CALL_INTRINSIC_2":
            #TODO this
            return []

        case "LOAD_SPECIAL":
            #TODO this
            return []



        case _:
            print(f"Unknown instruction {instruction.opname}")
            return []
