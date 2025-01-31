from collections import defaultdict
from os import stat
from scipy.special import comb
import json
from functools import lru_cache
import csv

# Create nested defaultdict with programming_language -> model -> problem_id structure
stats_first = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0, 0, 0, 0])))
filename = "results/aoc_merged.jsonl"
filename = "results/merged.jsonl"
filename = "results/mergedb2.jsonl"
#filename = "results/merged2.jsonl"
#filename = "results/2025-01-20b.jsonl"
#filename = "results/2025-01-25.jsonl"
#filename = "results/2025-01-25b.jsonl"
#filename = "results/2025-01-29.jsonl"
#filename = "results/2025-01-29bb.jsonl"
#filename = "results/2025-01-30.jsonl"
filename = "results/2025-01-30-2.jsonl"
filename = "results/2025-01-31.jsonl"
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
        "openai/gpt-4o-2024-11-20",
       # "deepseek/deepseek-r1",
       # "deepseek/deepseek-r1-distill-llama-70b",
       # "anthropic/claude-3.5-sonnet",
       # "openai/o1-mini-2024-09-12",
       # "gemini-exp-1206",
        "x-ai/grok-2-1212",
                "qwen/qwen-2.5-coder-32b-instruct",
        "meta-llama/llama-3.1-405b-instruct",
        "google/gemini-flash-1.5",
    ]
    return model in models

filter = has_compiled_in_language_filter("rust")
filter = identity_filter
#filter = filter_models
models = set()
langs = set()
print_lines = dict()

# Calculate and print statistics for each combination
new_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0, 0, 0, 0])))
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
            new_stats[lang][model][problem_id] = problem_stats
            total_attempts += 1
            avg_attempts += problem_stats[0]
            total_compile += problem_stats[1]/problem_stats[0]
            total_runtime += problem_stats[2]/problem_stats[0]
            total_correct += problem_stats[3]/problem_stats[0]
        
        # Calculate percentages
        compile_pct = (total_compile / total_attempts * 100) if total_attempts > 0 else 0
        runtime_pct = (total_runtime / total_attempts * 100) if total_attempts > 0 else 0
        correct_pct = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        avg_attempts /= total_attempts if total_attempts > 0 else 1


        
        print_lines[(lang, model)] = f"{lang:<12} {model:<45} {total_attempts:>8d} {compile_pct:>11.1f}% {runtime_pct:>11.1f}% {correct_pct:>11.1f}% {avg_attempts:>11.1f}"
        # Print row with adjusted spacing and alignment
        #print(f"{lang:<12} {model:<45} {total_attempts:>8d} {compile_pct:>11.1f}% {runtime_pct:>11.1f}% {correct_pct:>11.1f}% {avg_attempts:>11.1f}")

#for model in sorted(models):
#    for lang in sorted(langs):
for lang in sorted(langs):
    for model in sorted(models):
        if (lang, model) in print_lines:
            print(print_lines[(lang, model)])

    print()
    print("-" * 120)
    print()



# Print summary statistics with consistent formatting
print("\nSummary Statistics:")
print("-" * 100)
print(f"{'Metric':<30} {'Value':>8}")
print("-" * 100)
print(f"{'Total Languages:':<30} {len(stats_first):>8d}")
print(f"{'Total Models:':<30} {len(set(model for lang in stats_first.values() for model in lang)):>8d}")
print(f"{'Total Unique Problems:':<30} {len(set(prob for lang in stats_first.values() for model in lang.values() for prob in model)):>8d}")

# Calculate overall success rate
total_attempts = sum(stats[0] for lang in stats_first.values() for model in lang.values() for stats in model.values())
total_correct = sum(stats[3] for lang in stats_first.values() for model in lang.values() for stats in model.values())
overall_success = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
print(f"{'Overall Success Rate:':<30} {overall_success:>7.1f}%")

# Print summary statistics
print("\nSummary Statistics:")
print("-" * 80)
print(f"{'Metric':<30} {'Value':<10}")
print("-" * 80)

total_languages = len(stats_first)
total_models = len({model for lang in stats_first.values() for model in lang})
total_problems = len({prob for lang in stats_first.values() 
                          for model in lang.values() 
                          for prob in model})

print(f"Total Languages:{'':<19} {total_languages}")
print(f"Total Models:{'':<22} {total_models}")
print(f"Total Unique Problems:{'':<15} {total_problems}")

# Calculate overall success rates
all_attempts = 0
all_correct = 0
for lang in stats_first.values():
    for model in lang.values():
        for stats in model.values():
            all_attempts += stats[0]
            all_correct += stats[3]

overall_success_rate = (all_correct / all_attempts * 100) if all_attempts > 0 else 0
print(f"Overall Success Rate:{'':<16} {overall_success_rate:.1f}%")

print("-------")

stats_first = new_stats
problem_stats = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))
for lang, lang_dict in stats_first.items():
    for model in lang_dict.values():
        for problem_id, stats in model.items():
            problem_stats[lang][problem_id][0] += stats[0]
            problem_stats[lang][problem_id][1] += stats[1]
            problem_stats[lang][problem_id][2] += stats[3]

problem_str = dict()
print("\nProblem Statistics:")
print("-" * 80)
print(f"{'Problem ID':<20} {'Attempts':>10} {'Correct':>10} {'Compile %':>10} {'Success %':>10}")
print("-" * 80)
for lang, model_values in problem_stats.items():
    print()
    print(f"Language: {lang}")
    print()
    for problem_id, (attempts, compiles, correct) in sorted(model_values.items()):
        success_rate = (correct / attempts * 100) if attempts > 0 else 0
        compile_rate = (compiles / attempts * 100) if attempts > 0 else 0
        problem_str[(lang, problem_id)] = f"{problem_id:<20} {attempts:>10d} {correct:>10d} {compile_rate:>10.1f}% -  {success_rate:>10.1f}%"
        print(f"{problem_id:<20} {attempts:>10d} {correct:>10d} {compile_rate:>10.1f}% -  {success_rate:>10.1f}%")
    print("-" * 80)
    print(f"{'Problem ID':<20} {'Attempts':>10} {'Correct':>10} {'Compile %':>10} {'Success %':>10}")


for problem_id in sorted(set(prob for lang in stats_first.values() for model in lang.values() for prob in model)):
    print(f"{'Lang':<10} {'Problem ID':<20} {'Attempts':>10} {'Correct':>10} {'Compile %':>10} {'Success %':>10}")
    for lang in sorted(stats_first.keys()):
        if (lang, problem_id) in problem_str:
            print(f"{lang:<10}:" + problem_str[(lang, problem_id)])
    print()
    print("-" * 80)
    print()