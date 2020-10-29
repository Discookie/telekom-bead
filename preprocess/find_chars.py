from typing import Dict, List, Tuple
import zlib
import base64
import itertools
import operator
import re
import time
import multiprocessing as mp

def find_chars_thread(
    queue: mp.Queue, start: int, length: int, thread_id: int, report_interval: int,
    code: str, used_chars: List[str], variables: List[str], aliases: Dict[str, str], excluded: List[Tuple[int, int]]
):
    import zlib
    import base64
    import itertools
    best_result = 1e9
    best_combinations = []
    iteration = -start

    # Substitute aliases first
    if aliases:
        alias_regex = re.compile("|".join(aliases.keys()))
        code = alias_regex.sub(lambda m: aliases[m.group(0)], code)

    # We can reuse the variable name regex
    char_regex = re.compile("|".join(variables))

    for chars in itertools.product(used_chars, repeat=len(variables)):
        iteration += 1
        if (iteration <= 0): continue
        if (iteration > length): break

        if iteration % report_interval == 0:
            queue.put({"type": "status", "iter": iteration, "len": length, "id": thread_id})

        if not all([chars[l] != chars[r] for l, r in excluded]): continue

        # Substitute new var names
        char_dict = dict(zip(variables, chars))
        new_code = char_regex.sub(lambda m: char_dict[m.group(0)], code)

        result = len(base64.b85encode(zlib.compress(str.encode(new_code), 9)))

        if (result == best_result):
            best_combinations += [chars]
        elif result < best_result:
            best_result = result
            best_combinations = [chars]
    queue.put({"type": "result", "result": best_result, "combinations": best_combinations})

def find_chars(
    code: str, variables: List[str], aliases: Dict[str, str], excluded: List[Tuple[int, int]],
    difficulty: int = 10, thread_count: int = 12,
    log_interval: int = 10000, report_interval: int = 500, silent: bool = False
) -> Tuple[int, List[List[Tuple[str, str]]], List[str]]:
    queue = mp.Queue()

    chars = {x: 0 for x in map(chr,range(97,123))}
    counted_code = code

    for var in variables:
        counted_code = counted_code.replace(var, "")

    for c in counted_code:
        if c in chars:
            chars[c] += 1

    if not variables:
        return len(code), [], []
    
    chars_sorted = sorted([k for k, v in sorted(chars.items(), key=operator.itemgetter(1), reverse=True)][:difficulty])

    if not silent:
        print("Used alphabet:", chars_sorted)

    it_count = len(chars_sorted) ** len(variables)

    start_time = time.perf_counter()
    last_time = int(start_time)

    for i in range(thread_count):
        this_idx = it_count * i // thread_count
        next_idx = it_count * (i+1) // thread_count
        t = mp.Process(target=find_chars_thread, args=(
            queue, this_idx, next_idx - this_idx, i, report_interval,
            code, chars_sorted, variables, aliases, excluded
        ))
        t.start()

    best_result = 1e9
    best_combinations = []
    received_results = 0
    received_iterations = [0] * thread_count

    if not silent:
        print("Iteration count:", it_count)

    while received_results < thread_count:
        msg = queue.get()
        if msg["type"] == "status":
            received_iterations[msg["id"]] = msg["iter"]
            if not silent and sum(received_iterations) % log_interval == 0:
                current_time = time.perf_counter()
                if int(current_time) - int(last_time) >= 1:
                    last_time = int(current_time)
                    elapsed_time = current_time - start_time
                    elapsed_percent = sum(received_iterations) * 100 / it_count
                    remaining_time = elapsed_time * (it_count - sum(received_iterations)) / sum(received_iterations)
                    print(f'Iteration {sum(received_iterations)} ({elapsed_percent:.2f}%, {elapsed_time:.0f}s, remaining:{remaining_time:.0f}s)')
        elif msg["type"] == "result":
            result = msg["result"]
            combinations = msg["combinations"]
            if (result == best_result):
                best_combinations += combinations
            elif result < best_result:
                best_result = result
                best_combinations = combinations
            received_results += 1

        
    
    alias_idx = {}
    for src, tgt in aliases.items():
        alias_idx[src] = variables.index(tgt)
    best_combinations = [[(var, short) for var, short in zip(variables, combination)] + [(var, combination[variables.index(tgt)]) for var, tgt in aliases.items()] for combination in best_combinations[:100]]

    return best_result, best_combinations, chars_sorted

def __init__():
    mp.set_start_method('spawn')

if __name__ == '__main__':
    code = '''
{{code}}
'''[1:-1]

    variables = ["vars"]
    aliases = {"vars2": "vars"}
    excluded = [] # [(3, 8)]

    best_result, best_combinations, alphabet = find_chars(code, variables, aliases, excluded)

    print("Best result:", best_result, "with", len(best_combinations), "combinations, some:", [tuple(b for _, b in x) for x in best_combinations][:50])
    print("Used alphabet:", alphabet)
    print("Example combination:")
    print("'''")

    new_code = code
    for src, tgt in best_combinations[0]:
        new_code = new_code.replace(src, tgt)
    print(new_code)

    print("'''")
    print("Using characters", best_combinations[0])
    print("Compressed length:", best_result)

