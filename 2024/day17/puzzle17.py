"""
Advent of Code 2024: Day 17
"""


def run_program(registers, program_inputs) -> list[int]:
    """
    Given starting register values and list of commands, run the program and 
    return the output.
    """

    register_a, register_b, register_c = registers

    def _unpack_combo_operand(operand):
        nonlocal register_a, register_b, register_c
        if operand in [0, 1, 2, 3]:
            return operand
        if operand == 4:
            return register_a
        if operand == 5:
            return register_b
        if operand == 6:
            return register_c
        if operand == 7:
            assert operand != operand

    def _adv(i, combo_op):
        nonlocal register_a
        combo_res = _unpack_combo_operand(combo_op)
        numerator = register_a
        denominator = 2**combo_res
        register_a = numerator // denominator
        return i + 2

    def _bxl(i, op):
        nonlocal register_b
        register_b = register_b ^ op
        return i + 2

    def _bst(i, combo_op):
        nonlocal register_b
        combo_res = _unpack_combo_operand(combo_op)
        register_b = combo_res % 8
        return i + 2

    def _jnz(i, op):
        nonlocal register_a
        if register_a != 0:
            return op
        return i + 2

    def _bxc(i, _):
        nonlocal register_b
        nonlocal register_c
        register_b = register_b ^ register_c
        return i + 2

    def _out(i, combo_op):
        nonlocal stdout
        combo_res = _unpack_combo_operand(combo_op)
        stdout.append(combo_res % 8)
        return i + 2

    def _bdv(i, combo_op):
        nonlocal register_a
        nonlocal register_b
        combo_res = _unpack_combo_operand(combo_op)
        numerator = register_a
        denominator = 2**combo_res
        register_b = numerator // denominator
        return i + 2

    def _cdv(i, combo_op):
        nonlocal register_a
        nonlocal register_c
        combo_res = _unpack_combo_operand(combo_op)
        numerator = register_a
        denominator = 2**combo_res
        register_c = numerator // denominator
        return i + 2

    # process instructions
    stdout = []
    instruction_ptr = 0

    opcode_to_fn = [_adv, _bxl, _bst, _jnz, _bxc, _out, _bdv, _cdv]

    while instruction_ptr < len(program_inputs):
        opcode = program_inputs[instruction_ptr]
        operand = program_inputs[instruction_ptr+1]

        fn = opcode_to_fn[opcode]
        instruction_ptr = fn(instruction_ptr, operand)

    return stdout


def part1(registers, program):
    """Run program and print output"""
    # store the registers as lists so we can access them
    program_inputs = [int(i) for i in program.split(': ')[1].split(',')]
    res = run_program(registers, program_inputs)
    print(','.join(str(i) for i in res))

    return 0


def part2(registers, program):
    """Work backwards from final output to find correct A register."""
    program_inputs = [int(i) for i in program.split(': ')[1].split(',')]
    init_b, init_c = registers[1], registers[2]

    # you start operating on the lowest three bits
    possible_a = [(0, -1)]
    partial_program = []
    while possible_a:
        a_temp, target_idx = possible_a.pop(0)
        for i in range(0, 8):
            a_new = a_temp + i
            attempt = run_program([a_new, init_b, init_c], program_inputs)
            if attempt == program_inputs[target_idx:]:
                partial_program = attempt
                if partial_program == program_inputs:
                    return a_new
                possible_a.append((a_new << 3, target_idx-1))

    return 0


if __name__ == '__main__':
    with open('advent_of_code/2024/day17/input.txt', 'r') as f:
        registers, program = f.read().split('\n\n')
    registers = registers.split('\n')

    register_a = int(registers[0].split(': ')[1])
    register_b = int(registers[1].split(': ')[1])
    register_c = int(registers[2].split(': ')[1])

    part1([register_a, register_b, register_c], program)
    correct_a = part2([register_a, register_b, register_c], program)
    print(f'Correct A register is: {correct_a}')

