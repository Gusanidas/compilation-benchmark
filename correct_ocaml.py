from problem_attempt_result import compare_outputs
from problem_loader import load_aoc_problems, Problem, load_problems
import json
import asyncio

source_filename = "results/2025-01-25.jsonl"
writing_filename = "results/2025-01-25b.jsonl"

source_filename = "results/merged.jsonl"
writing_filename = "results/mergedb.jsonl"

#source_filename = "results/2025-01-29b.jsonl"
#writing_filename = "results/2025-01-29bb.jsonl"

aoc_problems = asyncio.run(load_aoc_problems())
aoc_problems_dict = {problem.problem_id: problem for problem in aoc_problems}
misc_problems = asyncio.run(load_problems())
misc_problems_dict = {problem.problem_id: problem for problem in misc_problems}
to_write = []
count = 0

with open(source_filename, "r") as reading_file:
    for line in reading_file.readlines():
        problem_attempt = json.loads(line)
        problem_id = problem_attempt["problem_id"]
        if problem_id in aoc_problems_dict and problem_attempt["programming_language"] in ["ocaml", "ada","julia", "rust"] and problem_attempt["compilation_success"] and problem_attempt["problem_correct"] != True and problem_attempt["output"] and len(problem_attempt["output"])>1:
            problem = aoc_problems_dict[problem_id]
            count += 1



print(count)