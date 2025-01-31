import asyncio
import random
import time
import os
import json
import aiofiles
from problem_attempt import attempt_problem
from problem_loader import load_aoc_problems, Problem, load_problems
from collections import Counter

t0 = time.time()


def get_counter_from_file(filename: str):
    result = Counter()
    try:
        with open(filename, "r") as file:
            for line in file:
                try:
                    entry = json.loads(line.strip())
                    # Extract the required fields, using None if a field is missing
                    tuple_entry = (
                        entry.get("model"),
                        entry.get("problem_id"),
                        entry.get("programming_language"),
                    )
                    result[tuple_entry] += 1
                except json.JSONDecodeError:
                    # Skip malformed JSON lines
                    continue

        return result

    except FileNotFoundError:
        raise FileNotFoundError(f"The file {filename} was not found.")


async def process_one_problem(
    model: str,
    language: str,
    problem: Problem,
    writing_filename: str,
    provider: str,
    semaphore: asyncio.Semaphore,
    idx = 0,
    **kwargs,
):
    async with semaphore:
        time.sleep(7)
        print(f"Processing {model} {language} {problem.problem_id}, idx = {idx}, time = {time.time() - t0}")
        problem_attempt = await attempt_problem(model, language, problem, provider, **kwargs)
        if problem_attempt.success:
            async with aiofiles.open(writing_filename, mode="a") as file:
                json_line = json.dumps(problem_attempt.to_writable_dict()) + "\n"
                await file.write(json_line)
                print(f"Success {model} {language} {problem.problem_id}")
        time.sleep(0.1)


async def main():
    programming_languages = ["python", "cpp", "haskell", "rust", "ocaml", "go"]
    programming_languages = ["groovy", "rust", "julia", "haskell", "cpp", "python", "go"]
    models = [
        #"openai/gpt-4o-mini",
        #"meta-llama/llama-3.1-405b-instruct",
        #"google/gemma-2-27b-it",
        #"google/gemma-2-9b-it",
        #"google/gemini-2.0-flash-exp:free",
        #"qwen/qwen-2.5-coder-32b-instruct",
        #"meta-llama/llama-3.1-405b-instruct",
        #"meta-llama/llama-3.1-70b-instruct",
        #"meta-llama/llama-3.3-70b-instruct",
        #"deepseek/deepseek-r1",
        #"google/gemini-2.0-flash-thinking-exp:free",
       #"deepseek/deepseek-r1",
       "deepseek/deepseek-r1",
        #"google/gemini-flash-1.5",
        #"anthropic/claude-3.5-sonnet",
        "anthropic/claude-3.5-sonnet",
       # "meta-llama/llama-3.1-70b-instruct",
       # "mistralai/codestral-mamba",
         #"deepseek/deepseek-chat",
         #"google/gemini-2.0-flash-thinking-exp:free",
        # "agent_deepseek/deepseek-chat",
        #"openai/gpt-4o-2024-11-20",
        #"openai/gpt-4o-2024-11-20",
        #"anthropic/claude-3-5-haiku",
        #"deepseek/deepseek-r1-distill-qwen-32b",
        #"mistralai/codestral-2501",
        "openai/o1-mini-2024-09-12",
        #"openai/o1-preview",
        "openai/o1",
        #"deepseek/deepseek-r1-distill-llama-70b",
        #"x-ai/grok-2-1212",
        #"microsoft/phi-4",
    ]
    #models = ["deepseek-r1:32b"]
    _models = [
        #"gemini-1.5-pro",
        "gemini-exp-1206",
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-thinking-exp-01-21",
    ]
    writing_filename = "results/merged.jsonl"
    #writing_filename = "results/2025-01-21b.jsonl"
    #writing_filename = "results/2025-01-25.jsonl"
    writing_filename = "results/2025-01-29.jsonl"
    writing_filename = "results/2025-01-29b.jsonl"
    writing_filename = "results/2025-01-30.jsonl"
    writing_filename = "results/2025-01-30-2.jsonl"
    provider = "open-router" # llama-cpp, ollama, gemini
    #provider = "gemini"
    #provider = "ollama"

    max_problems = 55
    max_concurrent_tasks = 18
    min_frequency = 3

    avoid_duplicate_problems = True
    if avoid_duplicate_problems and os.path.exists(writing_filename):
        existing_problems = get_counter_from_file(writing_filename)
    else:
        existing_problems = Counter()

    semaphore = asyncio.Semaphore(max_concurrent_tasks)
    # Load aoc problems, or other problems
    problems = await load_problems()
    #problems = await load_aoc_problems()
    problems = problems[:max_problems]
    skip_problem_ids = set(['9','1','2','24','25'])
    skip_problem_ids = set([str(i) for i in range(1, 11)] + ["12"] + [str(i) for i in range(13, 16)] + [str(i) for i in range(18, 29)])
    skip_problem_ids = set([str(i) for i in range(1, 28)])

    tasks = []
    idx = 0
    max_tasks = 120
    for problem in problems:
        for language in programming_languages:
            for model in models:
                if existing_problems[(model, problem.problem_id, language)] >= min_frequency or problem.problem_id in skip_problem_ids or idx > max_tasks:
                    print(f"Skipping {model} {language} {problem.problem_id}")
                    continue
                idx += 1
                tasks.append(
                    process_one_problem(
                        model, language, problem, writing_filename, provider, semaphore, idx = idx, temperature=0.6
                    )
                )

    random.shuffle(tasks)
    print(f"Total tasks: {len(tasks)}")
    tasks = tasks[:515]
    print(f"Total tasks: {len(tasks)}")
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    t0 = time.time()
    asyncio.run(main())
    print(f"Total time: {time.time() - t0}")
