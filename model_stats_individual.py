from collections import defaultdict
from scipy.special import comb
import json
from functools import lru_cache
import csv

# Create nested defaultdict with programming_language -> model -> problem_id structure
stats_first = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0, 0, 0, 0])))
filename = "results/aoc_merged.jsonl"
filename = "results/merged.jsonl"
filename = "results/mergedb.jsonl"
#filename = "results/merged2.jsonl"
#filename = "results/2025-01-20b.jsonl"
#filename = "results/2025-01-25.jsonl"
#filename = "results/2025-01-25b.jsonl"
#filename = "results/2025-01-29.jsonl"
#filename = "results/2025-01-29bb.jsonl"
#filename = "results/2025-01-30.jsonl"
problem_file = "problems.jsonl"

# Process the data
with open(filename, "r") as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        model = data["model"]
        problem_id = data["problem_id"]
        programming_language = data["programming_language"]
        
        # Update statistics with new structure
        stats = stats_first[programming_language][model][problem_id]
        stats[0] += 1  # Total attempts
        if data["compilation_success"]:
            stats[1] += 1  # Compilation successes
        if data["runtime_success"]:
            stats[2] += 1  # Runtime successes
        if data["problem_correct"]:
            stats[3] += 1  # Correct solutions

output_file = "model_stats.csv"
headers = ["model", "lang", "problem_id", "total_attempts", "compilation_successes", 
           "runtime_successes", "correct_solutions"]

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    
    # Iterate through the nested dictionary structure
    for lang in stats_first:
        for model in stats_first[lang]:
            for problem_id in stats_first[lang][model]:
                stats = stats_first[lang][model][problem_id]
                row = [model, lang, problem_id] + stats
                writer.writerow(row)

print(f"Statistics have been written to {output_file}")

# Print statistics
print("\nDetailed Statistics:")
print("-" * 120)
# Adjusted column widths and spacing
print(f"{'Language':<12} {'Model':<45} {'Total':>8} {'Compile %':>12} {'Runtime %':>12} {'Correct %':>12} {'Avg Attempts':>12}")
print("-" * 120)

solved_by_model = defaultdict(dict)

@lru_cache(maxsize=None)
def has_been_solved_by_model(model, problem_id):
    for lang in stats_first:
        if problem_id in stats_first[lang][model] and stats_first[lang][model][problem_id][3] > 0:
            return True
    return False

def has_compiled_filter(lang, model, problem_id):
    return stats_first[lang][model][problem_id][1] > 0

def has_compiled_in_language_filter(lang):
    return lambda _lang, model, problem_id: stats_first[lang][model][problem_id][1] > 0

def has_been_solved_filter(lang, model, problem_id):
    return has_been_solved_by_model(model, problem_id)

def identity_filter(lang, model, problem_id):
    return True

def filter_models(lang, model, problem_id):
    models = [
        #"anthropic/claude-3.5-sonnet",
       # "openai/o1-mini-2024-09-12",
               #"gemini-exp-1206",
        "openai/gpt-4o-2024-11-20",
        #"deepseek/deepseek-r1",
        #"deepseek/deepseek-r1-distill-llama-70b",
    ]
    langs = [
        "fortran",
        "rust",
        "julia",
        "d",
        "haskel"
    ]
    ids = [str(i) for i in range(1, 26)]
    return model in models and lang in langs and problem_id in ids

filter = has_compiled_in_language_filter("rust")
filter = identity_filter
filter = filter_models
models = set()
langs = set()
print_lines = dict()

# Calculate and print statistics for each combination
for lang in sorted(stats_first.keys()):
    langs.add(lang)
    for model in sorted(stats_first[lang].keys()):
        models.add(model)
        total_attempts = 0
        total_compile = 0
        total_runtime = 0
        total_correct = 0
        avg_attempts = 0

        
        # Sum up statistics across all problems for this language and model
        for problem_id, problem_stats in stats_first[lang][model].items():
            if not filter(lang, model, problem_id):
                continue
            print(f"{problem_id:<10} {lang:<12} {model:<45} {problem_id:>8} {problem_stats[0]:>12} {problem_stats[1]:>12} {problem_stats[2]:>12} {problem_stats[3]:>12}")
        