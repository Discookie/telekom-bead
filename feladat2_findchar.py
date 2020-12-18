import gzip
import zlib
import base64
import itertools
import operator
import time
import multiprocessing as mp
import queue

code = '''
import json,sys
with open(sys.argv[1])as file:json_object=json.load(file)
idx,combined_var=1,{(*sorted(obj3["points"]),):[obj3["capacity"],1]for obj3 in json_object["links"]}
for obj1 in json_object["simulation"]["demands"]:obj1["running"]=0
for tick in range(1,1+json_object["simulation"]["duration"]):
 for obj1 in json_object["simulation"]["demands"]:
  if obj1["start-time"]is tick:
   for obj2 in json_object["possible-circuits"]:
    if obj1["end-points"]==[obj2[0],obj2[-1]]and all([combined_var[(*sorted(obj3),)]>=[obj1["demand"],1]for obj3 in zip(obj2,obj2[1:])]):
     obj1["running"]=obj2
     for obj2 in zip(obj2,obj2[1:]):combined_var[(*sorted(obj2),)][1]=0
     break
   print(f'{idx}. igény foglalás: {"<->".join(obj1["end-points"])} st:{tick} - siker{"es"if obj1["running"]else"telen"}');idx=1+idx
  if obj1["running"]and obj1["end-time"]is tick:
   for linkid in zip(obj1["running"],obj1["running"][1:]):combined_var[(*sorted(linkid),)][1]=1
   print(f'{idx}. igény felszabadítás: {"<->".join(obj1["end-points"])} st:{tick}');idx=1+idx
'''[1:-1]

def thread(queue, start, length, thread_id, code, used_chars):
    import zlib
    import base64
    import itertools
    best_result = 99999
    best_combinations = []
    disallow = [(0, 1), (0, 2), (1, 2), (1, 3), (0, 4), (1, 4), (2, 4), (0, 5), (1, 5), (2, 5), (4, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6)]
    iteration = -start

    for chars in itertools.product(used_chars, repeat=7):
        iteration += 1
        if (iteration <= 0): continue
        if (iteration > length): break

        if iteration % 500 == 0:
            queue.put({"type": "status", "iter": iteration, "len": length, "id": thread_id})

        if not all([chars[l] != chars[r] for l, r in disallow]): continue
        json_object, obj1, obj2, obj3, tick, idx, combined_var = chars
        linkid, file = obj3, json_object
        new_code = code.replace("json_object", json_object).replace("obj1", obj1).replace("obj2",obj2).replace("obj3",obj3).replace("linkid",linkid).replace("file",file).replace("tick",tick).replace("idx",idx).replace("combined_var",combined_var)
        result = len(base64.b85encode(zlib.compress(str.encode(new_code), 9)))

        if (result == best_result):
            best_combinations += [(json_object, obj1, obj2, obj3, linkid, file, tick, idx, combined_var)]
        elif result < best_result:
            best_result = result
            best_combinations = [(json_object, obj1, obj2, obj3, linkid, file, tick, idx, combined_var)]
    queue.put({"type": "result", "result": best_result, "combinations": best_combinations})


if __name__ == '__main__':
    mp.set_start_method('spawn')
    queue = mp.Queue()
    chars = {x: 0 for x in map(chr,range(97,123))}
    for c in code.replace("json_object", "").replace("obj1", "").replace("obj2","").replace("obj3","").replace("linkid","").replace("file","").replace("tick","").replace("idx","").replace("combined_var",""):
        if c in chars: chars[c] += 1
    
    dict_size = 12
    chars_sorted = sorted([k for k, v in sorted(chars.items(), key=operator.itemgetter(1), reverse=True)][:12])
    print("Used alphabet:", chars_sorted)

    it_count = len(chars_sorted) ** 7
    thread_count = 12

    start_time = time.perf_counter()
    last_time = int(start_time)

    for i in range(thread_count):
        this_idx = it_count * i // thread_count
        next_idx = it_count * (i+1) // thread_count
        t = mp.Process(target=thread, args=(queue, this_idx, next_idx - this_idx, i, code, chars_sorted))
        t.start()

    best_result = 99999
    best_combinations = []
    received_results = 0
    received_iterations = [0] * thread_count

    print("Iteration count:", it_count)

    while received_results < thread_count:
        msg = queue.get()
        if msg["type"] == "status":
            received_iterations[msg["id"]] = msg["iter"]
            if sum(received_iterations) % 10000 == 0:
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

    print("Best result:", best_result, "with", len(best_combinations), "combinations, some:", best_combinations[:50])
    print("Used alphabet:", chars_sorted)
    print("Example combination:")
    print("'''")

    json_object, obj1, obj2, obj3, linkid, file, tick, idx, combined_var = best_combinations[0]
    print(code.replace("json_object", json_object).replace("obj1", obj1).replace("obj2",obj2).replace("obj3",obj3).replace("linkid",linkid).replace("file",file).replace("tick",tick).replace("idx",idx).replace("combined_var",combined_var))
    print("'''")
    print("Using characters", best_combinations[0])
    print("Compressed length:", best_result)

