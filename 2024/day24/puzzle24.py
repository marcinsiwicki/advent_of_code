"""
Advent of Code 2024: Day 24

"""
import copy


N_BITS = 45


def _compute_gates(computed_gates, remaining_gates) -> dict:
    """Iterate through computations."""
    while remaining_gates:
        (in_wire1, op, in_wire2), outgate = remaining_gates.pop(0)
        can_compute = (in_wire1 in computed_gates) and (in_wire2 in computed_gates)
        if can_compute:
            iw1_val = computed_gates[in_wire1]
            iw2_val = computed_gates[in_wire2]
            if op == 'OR':
                computed_gates[outgate] = iw1_val | iw2_val
            elif op == 'XOR':
                computed_gates[outgate] = iw1_val ^ iw2_val
            elif op == 'AND':
                computed_gates[outgate] = iw1_val & iw2_val
        else:
            remaining_gates.append(tuple([(in_wire1, op, in_wire2), outgate]))

    return computed_gates


def part1(wires: list[tuple[str, int]], gates: list[tuple[tuple[str], tuple[str]]] ) -> int:
    """Given gates and starting wire values, compute until have all results and find int."""
    initial_gates = dict(wires)
    remaining_gates = gates.copy()

    computed_gates = _compute_gates(initial_gates, remaining_gates)

    z_vals = [(k, v) for k, v in computed_gates.items() if k.startswith('z')]
    z_vals = sorted(z_vals, key=lambda x: int(x[0].replace('z', '')), reverse=True)
    bit_rep = ''.join([str(z[1]) for z in z_vals])
    int_rep = int(bit_rep, 2)

    return int(int_rep)


def part2(gates) -> str:
    """
    Find the outgate swaps needed to have xbits and ybits equal zbits after computation.

    Start with setting lowest bits and stop when z != x + y. Then trace through gates
    to determine the swap. 
    
    Each Z is the result of a XOR(an, bn). One of an or bn needs to be XOR(xn, yn).
    The other needs to be the OR(cn,dn) where cn is the AND(an-1,bn-1). dn is the
    AND(xn-1,yn-1).
    """
    # we need to set starting wire values and observe the sum at the end of the gate logic 

    swaps = dict()
    # step through, setting lowest bit and observing when input is incorrect
    iter = 0
    while iter < N_BITS:
        remaining_gates = copy.deepcopy(gates)
        x_bits = []
        y_bits = []
        initial_gates = dict()

        # build input
        for i in range(N_BITS):
            if i <= iter:
                x_val, y_val = 1, 0
            else:
                x_val, y_val = 0, 0

            x_bits.insert(0, str(x_val))
            y_bits.insert(0, str(y_val))
            initial_gates[f'x{str(i).zfill(2)}'] = x_val
            initial_gates[f'y{str(i).zfill(2)}'] = y_val

        for instruction in remaining_gates:
            if instruction[-1] in swaps:
                instruction[-1] = swaps[instruction[-1]]

        computed_gates = _compute_gates(initial_gates, remaining_gates)
        x = int(''.join(x_bits), 2)
        y = int(''.join(y_bits), 2)

        z_vals = [(k, v) for k, v in computed_gates.items() if k.startswith('z')]
        z_vals = sorted(z_vals, key=lambda x: int(x[0].replace('z', '')), reverse=True)
        z = int(''.join([str(z[1]) for z in z_vals]), 2)

        if x + y == z:
            iter += 1
            continue
        else: # find the swap
            # z value needs to be the XOR of x_n and y_n output and the carry of previous calc
            # the carry is the OR of x_n-1 AND y_n-1 and the AND version of x_n-1 XOR
            xn, yn, zn = f'x{str(iter).zfill(2)}', f'y{str(iter).zfill(2)}',f'z{str(iter).zfill(2)}'
            xn_xor_yn = next(i for i in gates if (xn in i[0] and yn in i[0] and 'XOR' in i[0]))
            z_xor = next(i for i in gates if i[-1] == zn)
            candidate_swap = []
            if z_xor[0][1] != 'XOR': # z assignment is not XOR
                candidate_swap.append(zn)

                # find where the xn_xor_yn outgate is used
                xor_outgates = [i for i in gates if xn_xor_yn[-1] in i[0]]
                for instruction in xor_outgates:
                    if instruction[0][1] == 'XOR':
                        candidate_swap.append(instruction[-1])
                        swaps.update({candidate_swap[0]: candidate_swap[1],
                                      candidate_swap[1]: candidate_swap[0]})
            else:
                # need to validate the inputs into the XOR
                left, right = z_xor[0][0], z_xor[0][-1]
                left = next(i for i in gates if left in i[1])
                right = next(i for i in gates if right in i[1])

                # one of the inputs needs to be the xn^yn compute
                for instruction in [left, right]:
                    if instruction[0][1] == 'AND': # invalid
                        candidate_swap.append(instruction[-1])
                        candidate_swap.append(xn_xor_yn[-1]) # swap with correct xn^yn
                        swaps.update({candidate_swap[0]: candidate_swap[1],
                                      candidate_swap[1]: candidate_swap[0]})

    return ','.join(sorted(swaps.keys()))


if __name__ == '__main__':
    with open('advent_of_code/2024/day24/input.txt', 'r') as f:
        wires, gates = f.read().split('\n\n')

    wires = [tuple(l.split(': ')) for l in wires.split('\n')]
    wires = [tuple([l[0], int(l[1])]) for l in wires]
    gates = [l.split(' -> ') for l in gates.split('\n')]
    gates = [[l[0].split(' '), l[1]] for l in gates]

    print(f'Output of wires: {part1(wires, gates)}')
    print(f'Crossed wires: {part2(gates)}')
