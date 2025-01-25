import argparse
import asyncio
import random
import time
import os
import json
import aiofiles
from src.problem_attempt import attempt_problem
from src.problem_loader import load_aoc_problems, Problem, load_problems

def parse_arguments():
    parser = argparse.ArgumentParser(description="Compilation Benchmark")
    parser.add_argument('--max_problems', type=int, default=55, help='Maximum number of problems to process')
    parser.add_argument('--max_concurrent_tasks', type=int, default=20, help='Maximum number of concurrent tasks, reduce this parameter to avoid rate limiting')
    parser.add_argument('-o', '--output_file', type=str, default="results/test_merged.jsonl", help='Output file name')
    parser.add_argument('--provider', type=str, choices=['open-router', 'llama-cpp', 'ollama'], default="open-router", help='Provider name')
    parser.add_argument('--rerun_problems', action='store_true', help='If set, will rerun all problems, otherwise will skip problems that are already in the output file')
    parser.add_argument('-t', '--temperature', type=float, default=1.0, help='Temperature factor to use for the LM text generation')
    return parser.parse_args()

def get_set_from_file(filename: str):
    result = set()
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
                    result.add(tuple_entry)
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
    **kwargs,
):
    async with semaphore:
        print(f"Processing {model} {language} {problem.problem_id}")
        time.sleep(0.1)
        problem_attempt = await attempt_problem(model, language, problem, provider, **kwargs)
        if problem_attempt.success:
            async with aiofiles.open(writing_filename, mode="a") as file:
                json_line = json.dumps(problem_attempt.to_writable_dict()) + "\n"
                await file.write(json_line)
                print(f"Success {model} {language} {problem.problem_id}")
        time.sleep(0.3)


async def main():
    # programming_languages = ["python", "cpp", "haskell", "rust", "ocaml", "go"]
    programming_languages = ["python", "cpp", "haskell", "rust", "ocaml", "go"]
    models = [
        # "openai/gpt-4o-mini",
        # "qwen/qwen-2.5-coder-32b-instruct",
        # "google/gemini-flash-1.5",
        # "anthropic/claude-3.5-sonnet",
        # "meta-llama/llama-3.1-70b-instruct",
        # "mistralai/codestral-mamba",
        # "deepseek/deepseek-chat",
        # "openai/gpt-4o-2024-11-20",
        # "anthropic/claude-3-5-haiku",
        "microsoft/phi-4",
        # "qwen/qvq-72b-preview",
        # "x-ai/grok-2-1212",
    ]

    args = parse_arguments()

    max_problems = args.max_problems
    max_concurrent_tasks = args.max_concurrent_tasks
    output_file = args.output_file
    provider = args.provider
    rerun_problems = args.rerun_problems
    temperature = args.temperature

    if (not rerun_problems) and os.path.exists(output_file):
        existing_problems = get_set_from_file(output_file)
    else:
        existing_problems = set()

    semaphore = asyncio.Semaphore(max_concurrent_tasks)
    # Load aoc problems, or other problems
    problems = await load_problems()
    #problems = await load_aoc_problems()
    problems = problems[:max_problems]

    tasks = []
    for problem in problems:
        for language in programming_languages:
            for model in models:
                if (model, problem.problem_id, language) in existing_problems:
                    print(f"Skipping {model} {language} {problem.problem_id}")
                    continue
                tasks.append(
                    process_one_problem(
                        model, language, problem, output_file, provider, semaphore, temperature=temperature,
                    )
                )

    random.shuffle(tasks)
    print(f"Total tasks: {len(tasks)}")
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
