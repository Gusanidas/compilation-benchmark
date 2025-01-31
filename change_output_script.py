from problem_attempt_result import compare_outputs
from problem_loader import load_aoc_problems, Problem, load_problems
import json
import asyncio

source_filename = "results/2025-01-25.jsonl"
writing_filename = "results/2025-01-25b.jsonl"

source_filename = "results/mergedb.jsonl"
writing_filename = "results/mergedb2.jsonl"

source_filename = "results/2025-01-30-2.jsonl"
writing_filename = "results/2025-01-31.jsonl"


aoc_problems = asyncio.run(load_aoc_problems())
aoc_problems_dict = {problem.problem_id: problem for problem in aoc_problems}
misc_problems = asyncio.run(load_problems())
misc_problems_dict = {problem.problem_id: problem for problem in misc_problems}
to_write = []

with open(source_filename, "r") as reading_file:
    for i, line in enumerate(reading_file.readlines()):
        problem_attempt = json.loads(line)
        problem_id = problem_attempt["problem_id"]
        if problem_id in aoc_problems_dict:
            problem = aoc_problems_dict[problem_id]
        elif problem_id in misc_problems_dict:
            problem = misc_problems_dict[problem_id]
        else:
            print(f"Problem {problem_id} not found.")
            to_write.append(problem_attempt)
            continue
        output = problem_attempt["output"] 
        expected_output = problem.output
        if compare_outputs(output, expected_output):
            problem_attempt["problem_correct"] = True
        else:
            problem_attempt["problem_correct"] = False
        problem_attempt["id"] = i
        to_write.append(problem_attempt)


with open(writing_filename, "w") as writing_file:
    for line in to_write:
        writing_file.write(json.dumps(line) + "\n")