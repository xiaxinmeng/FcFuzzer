def trace(frame, event, args):
    args.f_trace_opcodes = True
    if args == 'opcode':
        disassemble(frame.f_code, frame.f_lasti)
    return args