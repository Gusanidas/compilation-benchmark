from collections import defaultdict
from scipy.special import comb
import json

# Create nested defaultdict with programming_language -> model -> problem_id structure
stats_first = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0, 0, 0, 0])))
filename = "results/aoc_merged.jsonl"
#filename = "results/2025-01-17.jsonl"
#filename = "results/2025-01-12.jsonl"
#filename = "results/merged.jsonl"
#filename = "results/2025-01-20b.jsonl"
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

# Print statistics
print("\nDetailed Statistics:")
print("-" * 100)
# Adjusted column widths and spacing
print(f"{'Language':<12} {'Model':<35} {'Total':>8} {'Compile %':>12} {'Runtime %':>12} {'Correct %':>12}")
print("-" * 100)

# Calculate and print statistics for each combination
for lang in sorted(stats_first.keys()):
    for model in sorted(stats_first[lang].keys()):
        total_attempts = 0
        total_compile = 0
        total_runtime = 0
        total_correct = 0
        
        # Sum up statistics across all problems for this language and model
        for problem_stats in stats_first[lang][model].values():
            total_attempts += 1
            total_compile += problem_stats[1]/problem_stats[0]
            total_runtime += problem_stats[2]/problem_stats[0]
            total_correct += problem_stats[3]/problem_stats[0]
        
        # Calculate percentages
        compile_pct = (total_compile / total_attempts * 100) if total_attempts > 0 else 0
        runtime_pct = (total_runtime / total_attempts * 100) if total_attempts > 0 else 0
        correct_pct = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        
        # Print row with adjusted spacing and alignment
        print(f"{lang:<12} {model:<35} {total_attempts:>8d} {compile_pct:>11.1f}% {runtime_pct:>11.1f}% {correct_pct:>11.1f}%")
    print()
    print("-" * 100)
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

problem_stats = defaultdict(lambda: [0, 0])
for lang in stats_first.values():
    for model in lang.values():
        for problem_id, stats in model.items():
            problem_stats[problem_id][0] += stats[0]
            problem_stats[problem_id][1] += stats[3]

print("\nProblem Statistics:")
print("-" * 80)
print(f"{'Problem ID':<20} {'Attempts':>10} {'Correct':>10} {'Success %':>10}")
print("-" * 80)
for problem_id, (attempts, correct) in sorted(problem_stats.items()):
    success_rate = (correct / attempts * 100) if attempts > 0 else 0
    print(f"{problem_id:<20} {attempts:>10d} {correct:>10d} {success_rate:>10.1f}%")