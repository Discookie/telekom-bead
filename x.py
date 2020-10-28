import argparse
from os import path, remove, rmdir
import subprocess
import sys
import json
import shutil
import time
from typing import Any, Dict, List, Optional, Union

from preprocess.find_chars import find_chars
from preprocess.preprocess import preprocess


def _build(difficulty: Union[int, bool], thread_count: int, is_silent: bool, build_files: Optional[List[str]] = None) -> bool:
    try:
        with open("meta/build.json", "r") as f:
            build_params = json.load(f)
    except:
        print("meta/build.json does not exist", file=sys.stderr)
        return False

    if difficulty is True:
        difficulty = build_params.get("release-opt", 9)
    elif difficulty is False:
        difficulty = build_params.get("debug-opt", 6)

    files_to_build: List[Dict[str, Any]]
    
    if build_files is None:
        files_to_build = build_params.get("files", [])
    else:
        files_to_build = [file for file in build_params.get("files", []) if file["path"] in build_files]

    file_sizes: Dict[str, int] = {}

    for file in files_to_build:
        if "path" not in file:
            print("Malformed JSON", file=sys.stderr)
            return False

        # Step 0: Read file
        try:
            with open("src/" + file["path"], "r") as f:
                step_0 = f.read()
        except:
            print(f'File {file["path"]} does not exist', file=sys.stderr)
            return False
            
        if not is_silent:
            print("Processing file", file["path"], file=sys.stderr)


        step_0_size = len(step_0)

        # Step 1: Find chars
        step_1_vars = file.get("variables", [])
        step_1_aliases = file.get("aliases", {})
        step_1_excluded = file.get("excluded", [])

        try:
            step_1_size, step_1_list, _ = find_chars(
                step_0, step_1_vars, step_1_aliases, step_1_excluded,
                difficulty, thread_count, silent=is_silent
            )
        except Exception as e:
            print("Step 1 failed: crash", file=sys.stderr)
            print(e, file=sys.stderr)
            return False

        if len(step_1_list) == 0:
            print("Step 1 failed: no combinations", file=sys.stderr)
            return False

        step_1 = step_0
        for src, tgt in step_1_list[0]:
            step_1 = step_1.replace(src, tgt)
            
        if not is_silent:
            print("Step 1 complete", file=sys.stderr)

        # Step 2: Preprocess and template code
        with open("preprocess/template.py", "rb") as f:
            step_2_template = f.read()

        step_2_compressed_code = preprocess(step_1, step_1_list[0])

        step_2 = step_2_template.replace(b"{{code}}", step_2_compressed_code)
        step_2_size = len(step_2)
            
        if not is_silent:
            print("Step 2 complete", file=sys.stderr)

        # Note that the file is overwritten
        with open("build/" + file["path"], "wb") as f:
            f.write(step_2)

        file_sizes[file["path"]] = step_2_size

        if not is_silent:
            print(f'===', file=sys.stderr)
            print(f'File {file["path"]}:', file=sys.stderr)
            print(f'   {step_0_size} => {step_1_size} characters', file=sys.stderr)
            print(f'   Final size: {step_2_size}', file=sys.stderr)
            print(f'===', file=sys.stderr)

    if not is_silent:
        print("Cumulative size:", sum(file_sizes.values()), file=sys.stderr)

    return True

def _run(run_directory: str, run_files: Optional[List[str]] = None) -> bool:
    try:
        with open("meta/build.json", "r") as f:
            build_params = json.load(f)
    except:
        print("meta/build.json does not exist", file=sys.stderr)
        return False

    files_to_run: List[Dict[str, Any]]
    
    if run_files is None:
        files_to_run = build_params.get("files", [])
    else:
        files_to_run = [file for file in build_params.get("files", []) if file["path"] in run_files]

    processes: List[subprocess.Popen] = []

    for file in files_to_run:
        new_process = subprocess.Popen(["py", run_directory + "/" + file["path"]] + file.get("args", []))
        processes.append(new_process)

    process_codes = [process.wait() == 0 for process in processes]
        
    return all(process_codes)

def _clean(is_silent: bool) -> bool:
    try:
        with open("meta/build.json", "r") as f:
            build_params = json.load(f)
    except:
        print("meta/build.json does not exist", file=sys.stderr)
        return False

    try:
        if path.exists("build/"):
            shutil.rmtree("build/")
    except:
        return False

    return True

def build(show_help: bool):
    parser = argparse.ArgumentParser(description="Build framework")
    parser.add_argument("build")
    parser.add_argument("--release", action='store_true')
    parser.add_argument("-o", "--opt-difficulty", type=int, default=0)
    parser.add_argument("-f", "--files", nargs="*", default=None)
    parser.add_argument("-c", "--threads", type=int, default=12)
    parser.add_argument("-q", "--silent", action='store_true')

    if show_help:
        parser.print_help()
        sys.exit(0)

    if sys.argv[0] == "x.py":
        args = sys.argv[1:]
    else:
        args = sys.argv
    args = parser.parse_args(args)

    difficulty = args.opt_difficulty if args.opt_difficulty > 0 else args.release

    start_time = time.perf_counter()

    result = _build(difficulty, args.threads, args.silent, args.files)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    if result:
        if not args.silent:
            print(f"Build completed in {elapsed_time:.0f}s", file=sys.stderr)
        sys.exit(0)
    else:
        if not args.silent:
            print(f"Build failed in {elapsed_time:.0f}s", file=sys.stderr)
        sys.exit(1)


def run(show_help: bool):
    parser = argparse.ArgumentParser(description="Build framework")
    parser.add_argument("run")
    parser.add_argument("--no-build", action='store_true')
    parser.add_argument("--no-rebuild", action='store_true')
    parser.add_argument("--release", action='store_true')
    parser.add_argument("-o", "--opt-difficulty", type=int, default=10)
    parser.add_argument("-f", "--files", nargs="*", default=None, help="Build only")
    parser.add_argument("-r", "--run-files", nargs="*", default=None, help="Run only")
    parser.add_argument("-c", "--threads", type=int, default=12)
    parser.add_argument("-q", "--silent", action='store_true')


    if show_help:
        parser.print_help()
        sys.exit(0)

    if sys.argv[0] == "x.py":
        args = sys.argv[1:]
    else:
        args = sys.argv
    args = parser.parse_args(args)

    difficulty = args.opt_difficulty if args.opt_difficulty > 0 else args.release

    if args.no_rebuild:
        result = _run("build", args.run_files)
    elif args.no_build:
        result = _run("src", args.run_files)
    else:
        start_time = time.perf_counter()

        result = _build(difficulty, args.threads, args.silent, args.files)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        if result:
            if not args.silent:
                print(f"Build completed in {elapsed_time:.0f}s", file=sys.stderr)
        else:
            if not args.silent:
                print(f"Build failed in {elapsed_time:.0f}s", file=sys.stderr)
            sys.exit(1)
            
        result = _run("build", args.run_files)

    if result:
        if not args.silent:
            print(f"Run completed", file=sys.stderr)
        sys.exit(0)
    else:
        if not args.silent:
            print(f"Run failed", file=sys.stderr)
        sys.exit(1)

def clean(show_help: bool):
    parser = argparse.ArgumentParser(description="Build framework")
    parser.add_argument("clean")
    parser.add_argument("-q", "--silent", action='store_true')

    if show_help:
        parser.print_help()
        sys.exit(0)

    if sys.argv[0] == "x.py":
        args = sys.argv[1:]
    else:
        args = sys.argv
    args = parser.parse_args(args)

    result = _clean(args.silent)
    
    if result:
        if not args.silent:
            print(f"Clean completed", file=sys.stderr)
        sys.exit(0)
    else:
        if not args.silent:
            print(f"Clean failed", file=sys.stderr)
        sys.exit(1)

def pack(show_help: bool):
    print("Unimplemented", file=sys.stderr)
    pass

def save(show_help: bool):
    print("Unimplemented", file=sys.stderr)
    pass

def main():
    parser = argparse.ArgumentParser(description="Build framework")
    parser.add_argument("subcommand", default="help", nargs="+", choices=["help", "build", "run", "clean", "pack", "save"])

    if sys.argv[0] == "x.py":
        sysargs = sys.argv[1:]
    else:
        sysargs = sys.argv

    args = parser.parse_args(sysargs)

    show_help = args.subcommand[0] == "help"
    if show_help and len(sysargs) > 1:
        subcommand = sysargs[1]
    else:
        subcommand = args.subcommand[0]

    if subcommand == "build": build(show_help)
    elif subcommand == "run": run(show_help)
    elif subcommand == "clean": clean(show_help)
    elif subcommand == "pack": pack(show_help)
    elif subcommand == "save": save(show_help)
    else: parser.print_help()

        

if __name__ == "__main__":
    main()