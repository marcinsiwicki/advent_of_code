"""
Advent of Code 2024: Day 9
"""
import time


def part1(fragmented_disk: str) -> int:
    """Return checksum of rearranged disk."""
    # break out first string into composite of open spaces and fileID
    converted_disk = []
    file_id = 0
    for i, c in enumerate(fragmented_disk):
        if i % 2 == 0: # is a file
            converted_disk += [file_id] * int(c)
            file_id += 1
        else:
            converted_disk += ['.'] * int(c)

    # now re-arrange the blocks
    i = 0
    j = len(converted_disk) - 1
    while i < j:
        # if left isn't empty
        if converted_disk[i] != '.':
            i += 1
        elif converted_disk[j] == '.':
            j -= 1
        # swap from right to left
        else: # l[i] == '.' and l[j] != '.'
            converted_disk[i] = converted_disk[j]
            converted_disk[j] = '.'
            i += 1
            j -= 1

    return sum(i * f_id for i, f_id in enumerate(converted_disk) if f_id != '.')


def part2(fragmented_disk: str) -> int:
    """Rearrange files reducing fragmentation."""
    converted_disk = []
    empty_blocks = []
    file_id = 0
    for i, c in enumerate(fragmented_disk):
        if i % 2 == 0: # is a file
            converted_disk.append({'id': file_id, 'size': int(c)})
            file_id += 1
        else:
            converted_disk.append({'id': '.', 'size': int(c)})
            empty_blocks.append({'idx': i, 'size': int(c)})

    right = len(converted_disk) - 1
    processed_ids = set()

    while right > -1:
        grp = converted_disk[right]
        if grp['id'] not in processed_ids and grp['id'] != '.':
            processed_ids.add(grp['id'])

            # find the first empty block large enough
            target_empty_block = None
            filled_empties = []
            for i, empty_block in enumerate(empty_blocks):
                if empty_block['size'] < 1:
                    filled_empties.append(i)
                if empty_block['idx'] > right:
                    break
                if empty_block['size'] >= grp['size']:
                    target_empty_block = empty_block
                    break

            if target_empty_block:
                # need to update the empty_block copy
                # need to update the actual copy in list of empty and new
                empty_idx = target_empty_block['idx']
                move_grp = converted_disk.pop(right)
                target_empty_block['size'] -= move_grp['size']
                converted_disk[empty_idx]['size'] -= move_grp['size']
                converted_disk.insert(empty_idx, move_grp)
                converted_disk.insert(right, {'id': '.', 'size': move_grp['size']})
                # since we inserted a new elem into the list, all subsequent
                # empty blocks need their index updated
                for empty_block in empty_blocks:
                    if empty_block['idx'] >= empty_idx:
                        empty_block['idx'] += 1

            for i in filled_empties[-1::-1]:
                empty_blocks.pop(i)

        right -= 1

    # compute checksums
    checksum = 0
    list_i = 0
    true_i = 0
    while list_i < len(converted_disk) - 1:
        e = converted_disk[list_i]
        if e['id'] != '.':
            for j in range(e['size']):
                checksum += e['id'] * (true_i + j)
        true_i += e['size']
        list_i += 1

    return checksum


def part2_optimized(fragmented_disk: str) -> int:
    """Use start/end points of each block to defrag."""
    converted_disk = []
    occupied_blocks = []
    empty_blocks = []
    file_id = 0
    true_idx = 0

    for i, c in enumerate(fragmented_disk):
        if i % 2 == 0: # is a file
            converted_disk += [file_id] * int(c)
            occupied_blocks.append([true_idx, true_idx + int(c) - 1])
            file_id += 1
        else:
            converted_disk += ['.'] * int(c)
            empty_blocks.append([true_idx, true_idx + int(c) - 1])
        true_idx += int(c)

    for file_block in occupied_blocks[-1::-1]:
        # find a valid empty block
        for empty_block in empty_blocks:
            if empty_block[0] > file_block[0]:
                break
            empty_size = empty_block[1] - empty_block[0] + 1
            file_block_size = file_block[1] - file_block[0] + 1
            if empty_size >= file_block_size:
                # move the file over
                e_start = empty_block[0]
                f_start, f_end = file_block[0], file_block[1]
                converted_disk[e_start:e_start+file_block_size] = converted_disk[f_start:f_end+1]
                converted_disk[f_start:f_end+1] = ['.'] * file_block_size
                empty_block[0] += file_block_size
                if empty_block[0] > empty_block[1]:
                    empty_blocks.remove(empty_block)
                break

    return sum(i * f_id for i, f_id in enumerate(converted_disk) if f_id != '.')


if __name__ == '__main__':
    with open('advent_of_code/2024/day09/input.txt', 'r') as f:
        disk_map = f.readlines()
    assert len(disk_map) == 1
    disk_map = disk_map[0].strip()

    s = time.time()
    print(f'Filesystem checksum: {part1(disk_map)} in {time.time() - s}')
    s = time.time()
    print(f'Defragged checksum: {part2(disk_map)} in {time.time() - s}')
    s = time.time()
    print(f'Defragged checksum (opt): {part2_optimized(disk_map)} in {time.time() - s}')
