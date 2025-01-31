import numpy as np
from scipy.stats import spearmanr
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import csv

compile_success_rust = {
    "anthropic/claude-3-5-haiku": 76.2,
    "anthropic/claude-3.5-sonnet": 79.0,
    "deepseek/deepseek-chat": 83.9,
    "google/gemini-flash-1.5": 55.4,
    "meta-llama/llama-3.1-70b-instruct": 34.3,
    "microsoft/phi-4": 17.1,
    "mistralai/codestral-2501": 68.6,
    "mistralai/codestral-mamba": 42.9,
    "openai/gpt-4o-2024-11-20": 73.8,
    "openai/gpt-4o-mini": 55.4,
    "openai/o1-mini-2024-09-12": 71.2,
    "qwen/qvq-72b-preview": 21.3,
    "qwen/qwen-2.5-coder-32b-instruct": 56.7,
    "qwen/qwq-32b-preview": 37.7,
    "x-ai/grok-2-1212": 68.6,
}

problem_success_rust = {
    "anthropic/claude-3-5-haiku": 17.4,
    "anthropic/claude-3.5-sonnet": 33.8,
    "deepseek/deepseek-chat": 32.6,
    "google/gemini-flash-1.5": 15.3,
    "meta-llama/llama-3.1-70b-instruct": 10.0,
    "microsoft/phi-4": 1.4,
    "mistralai/codestral-2501": 8.6,
    "mistralai/codestral-mamba": 2.9,
    "openai/gpt-4o-2024-11-20": 33.9,
    "openai/gpt-4o-mini": 14.2,
    "openai/o1-mini-2024-09-12": 34.0,
    "qwen/qvq-72b-preview": 3.3,
    "qwen/qwen-2.5-coder-32b-instruct": 16.0,
    "qwen/qwq-32b-preview": 11.0,
    "x-ai/grok-2-1212": 24.3,
}

compile_success_python = {
    "anthropic/claude-3-5-haiku": 85.4,
    "anthropic/claude-3.5-sonnet": 91.7,
    "deepseek/deepseek-chat": 93.6,
    "google/gemini-flash-1.5": 91.3,
    "meta-llama/llama-3.1-70b-instruct": 98.6,
    "microsoft/phi-4": 100.0,
    "mistralai/codestral-2501": 100.0,
    "mistralai/codestral-mamba": 100.0,
    "openai/gpt-4o-2024-11-20": 98.9,
    "openai/gpt-4o-mini": 99.6,
    "openai/o1-mini-2024-09-12": 98.0,
    "qwen/qvq-72b-preview": 100.0,
    "qwen/qwen-2.5-coder-32b-instruct": 95.6,
    "qwen/qwq-32b-preview": 93.2,
    "x-ai/grok-2-1212": 100.0,
}

problem_success_python = {
    "anthropic/claude-3-5-haiku": 31.9,
    "anthropic/claude-3.5-sonnet": 54.2,
    "deepseek/deepseek-chat": 41.0,
    "google/gemini-flash-1.5": 23.4,
    "meta-llama/llama-3.1-70b-instruct": 17.1,
    "microsoft/phi-4": 22.9,
    "mistralai/codestral-2501": 25.7,
    "mistralai/codestral-mamba": 5.7,
    "openai/gpt-4o-2024-11-20": 17.2,
    "openai/gpt-4o-mini": 19.9,
    "openai/o1-mini-2024-09-12": 72.7,
    "qwen/qvq-72b-preview": 24.2,
    "qwen/qwen-2.5-coder-32b-instruct": 30.8,
    "qwen/qwq-32b-preview": 32.8,
    "x-ai/grok-2-1212": 35.3,
}


compile_success_ocaml = {
    "anthropic/claude-3-5-haiku": 45.7,
    "anthropic/claude-3.5-sonnet": 58.6,
    "deepseek/deepseek-chat": 52.1,
    "google/gemini-flash-1.5": 28.6,
    "meta-llama/llama-3.1-70b-instruct": 21.4,
    "microsoft/phi-4": 8.6,
    "mistralai/codestral-2501": 32.1,
    "mistralai/codestral-mamba": 14.3,
    "openai/gpt-4o-2024-11-20": 52.9,
    "openai/gpt-4o-mini": 36.4,
    "openai/o1-mini-2024-09-12": 55.7,
    "qwen/qvq-72b-preview": 23.3,
    "qwen/qwen-2.5-coder-32b-instruct": 27.1,
    "qwen/qwq-32b-preview": 16.1,
}

problem_success_ocaml = {
    "anthropic/claude-3-5-haiku": 11.4,
    "anthropic/claude-3.5-sonnet": 21.4,
    "deepseek/deepseek-chat": 12.9,
    "google/gemini-flash-1.5": 2.9,
    "meta-llama/llama-3.1-70b-instruct": 5.7,
    "microsoft/phi-4": 0.0,
    "mistralai/codestral-2501": 4.3,
    "mistralai/codestral-mamba": 0.0,
    "openai/gpt-4o-2024-11-20": 20.0,
    "openai/gpt-4o-mini": 7.9,
    "openai/o1-mini-2024-09-12": 37.1,
    "qwen/qvq-72b-preview": 0.0,
    "qwen/qwen-2.5-coder-32b-instruct": 6.4,
    "qwen/qwq-32b-preview": 8.1,
}

compile_success_haskell = {
    "anthropic/claude-3-5-haiku": 35.2,
    "anthropic/claude-3.5-sonnet": 50.3,
    "deepseek/deepseek-chat": 48.3,
    "google/gemini-flash-1.5": 16.3,
    "meta-llama/llama-3.1-70b-instruct": 14.3,
    "microsoft/phi-4": 11.4,
    "mistralai/codestral-2501": 33.6,
    "mistralai/codestral-mamba": 7.1,
    "openai/gpt-4o-2024-11-20": 54.3,
    "openai/gpt-4o-mini": 30.5,
    "openai/o1-mini-2024-09-12": 53.8,
    "qwen/qvq-72b-preview": 0.0,
    "qwen/qwen-2.5-coder-32b-instruct": 23.0,
    "qwen/qwq-32b-preview": 14.6,
    "x-ai/grok-2-1212": 32.4,
}

problem_success_haskell = {
    "anthropic/claude-3-5-haiku": 9.3,
    "anthropic/claude-3.5-sonnet": 22.3,
    "deepseek/deepseek-chat": 13.0,
    "google/gemini-flash-1.5": 6.9,
    "meta-llama/llama-3.1-70b-instruct": 4.3,
    "microsoft/phi-4": 5.7,
    "mistralai/codestral-2501": 8.6,
    "mistralai/codestral-mamba": 2.9,
    "openai/gpt-4o-2024-11-20": 24.5,
    "openai/gpt-4o-mini": 11.0,
    "openai/o1-mini-2024-09-12": 32.6,
    "qwen/qvq-72b-preview": 0.0,
    "qwen/qwen-2.5-coder-32b-instruct": 7.5,
    "qwen/qwq-32b-preview": 6.6,
    "x-ai/grok-2-1212": 10.3,
}

compile_success_cpp = {
    "anthropic/claude-3-5-haiku": 81.7,
    "anthropic/claude-3.5-sonnet": 80.7,
    "deepseek/deepseek-chat": 83.1,
    "google/gemini-flash-1.5": 74.6,
    "meta-llama/llama-3.1-70b-instruct": 64.3,
    "microsoft/phi-4": 47.1,
    "mistralai/codestral-2501": 79.3,
    "mistralai/codestral-mamba": 60.0,
    "openai/gpt-4o-2024-11-20": 82.9,
    "openai/gpt-4o-mini": 63.2,
    "openai/o1-mini-2024-09-12": 95.7,
    "qwen/qwen-2.5-coder-32b-instruct": 77.1,
    "qwen/qwq-32b-preview": 62.8,
}

problem_success_cpp = {
    "anthropic/claude-3-5-haiku": 24.0,
    "anthropic/claude-3.5-sonnet": 53.1,
    "deepseek/deepseek-chat": 30.7,
    "google/gemini-flash-1.5": 25.5,
    "meta-llama/llama-3.1-70b-instruct": 14.3,
    "microsoft/phi-4": 14.3,
    "mistralai/codestral-2501": 21.4,
    "mistralai/codestral-mamba": 4.3,
    "openai/gpt-4o-2024-11-20": 36.2,
    "openai/gpt-4o-mini": 15.4,
    "openai/o1-mini-2024-09-12": 65.0,
    "qwen/qwen-2.5-coder-32b-instruct": 29.3,
    "qwen/qwq-32b-preview": 27.3,
}

compile_success_go = {
    "anthropic/claude-3-5-haiku": 95.7,
    "anthropic/claude-3.5-sonnet": 90.0,
    "deepseek/deepseek-chat": 93.6,
    "google/gemini-flash-1.5": 94.3,
    "meta-llama/llama-3.1-70b-instruct": 98.6,
    "microsoft/phi-4": 100.0,
    "mistralai/codestral-2501": 97.1,
    "mistralai/codestral-mamba": 95.7,
    "openai/gpt-4o-2024-11-20": 95.0,
    "openai/gpt-4o-mini": 97.1,
    "openai/o1-mini-2024-09-12": 98.6,
    "qwen/qvq-72b-preview": 100.0,
    "qwen/qwen-2.5-coder-32b-instruct": 95.0,
    "qwen/qwq-32b-preview": 98.4,
    "x-ai/grok-2-1212": 97.1,
}

problem_success_go = {
    "anthropic/claude-3-5-haiku": 27.1,
    "anthropic/claude-3.5-sonnet": 42.9,
    "deepseek/deepseek-chat": 32.1,
    "google/gemini-flash-1.5": 15.7,
    "meta-llama/llama-3.1-70b-instruct": 5.7,
    "microsoft/phi-4": 11.4,
    "mistralai/codestral-2501": 24.3,
    "mistralai/codestral-mamba": 5.7,
    "openai/gpt-4o-2024-11-20": 37.9,
    "openai/gpt-4o-mini": 20.0,
    "openai/o1-mini-2024-09-12": 65.7,
    "qwen/qvq-72b-preview": 7.9,
    "qwen/qwen-2.5-coder-32b-instruct": 23.6,
    "qwen/qwq-32b-preview": 14.3,
    "x-ai/grok-2-1212": 31.4,
}

with open('model_stats.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)
        break

print(1/0)

def compute_correlation(dict1, dict2):
    """
    Compute correlation between values of two dictionaries for their common keys.

    Args:
        dict1 (dict): First dictionary with float/int values
        dict2 (dict): Second dictionary with float/int values

    Returns:
        float: Pearson correlation coefficient
        list: Common keys used in computation
    """
    # Find common keys
    common_keys = sorted(set(dict1.keys()) & set(dict2.keys()))

    if len(common_keys) < 2:
        raise ValueError("Need at least 2 common keys to compute correlation")

    # Extract values for common keys
    values1 = [dict1[key] for key in common_keys]
    values2 = [dict2[key] for key in common_keys]

    # Convert to numpy arrays
    array1 = np.array(values1)
    array2 = np.array(values2)

    # Compute correlation
    correlation = np.corrcoef(array1, array2)[0, 1]

    return correlation, common_keys


def compute_rank_correlation(dict1, dict2):
    """
    Compute Spearman rank correlation between values of two dictionaries for their common keys.

    Args:
        dict1 (dict): First dictionary with float/int values
        dict2 (dict): Second dictionary with float/int values

    Returns:
        float: Spearman rank correlation coefficient
        list: Common keys used in computation
    """
    # Find common keys
    common_keys = sorted(set(dict1.keys()) & set(dict2.keys()))

    if len(common_keys) < 2:
        raise ValueError("Need at least 2 common keys to compute correlation")

    # Extract values for common keys
    values1 = [dict1[key] for key in common_keys]
    values2 = [dict2[key] for key in common_keys]

    # Convert to numpy arrays
    array1 = np.array(values1)
    array2 = np.array(values2)

    # Compute Spearman rank correlation
    correlation, p_value = spearmanr(array1, array2)

    return correlation, common_keys


def print_correlation_table(variables, correlation_func):
    """
    Print a correlation table for a list of variables with dynamic column widths and return a correlation matrix.

    Args:
        variables: Dictionary of variable names and their values
        correlation_func: Function that takes two arrays and returns correlation

    Returns:
        pd.DataFrame: Correlation matrix
    """
    # Calculate maximum width needed for variable names
    max_name_width = max(len(name) for name in variables.keys())
    # Add padding for readability
    col_width = max(max_name_width + 2, 10)

    # Print header row with dynamic spacing
    header = " " * col_width  # Space for row labels
    for name in variables.keys():
        header += f"{name:>{col_width}}"
    print(header)

    # Print separator line with dynamic length
    print("-" * (col_width + col_width * len(variables)))

    # Initialize correlation matrix
    corr_matrix = pd.DataFrame(index=variables.keys(), columns=variables.keys())

    # Print each row with dynamic column widths
    for name1, values1 in variables.items():
        row = f"{name1:<{col_width}}"  # Left-align variable name with dynamic width
        for name2, values2 in variables.items():
            correlation, _ = correlation_func(values1, values2)
            row += f"{correlation:>{col_width}.3f}"  # Right-align with dynamic width
            corr_matrix.loc[name1, name2] = correlation
        print(row)

    return corr_matrix.astype(float)


comps = {
    "comp_cpp": compile_success_cpp,
    "comp_haskell": compile_success_haskell,
    "comp_ocaml": compile_success_ocaml,
    "comp_python": compile_success_python,
    "comp_rust": compile_success_rust,
    "comp_go": compile_success_go,
}

probs = {
    "prob_cpp": problem_success_cpp,
    "prob_haskell": problem_success_haskell,
    "prob_ocaml": problem_success_ocaml,
    "prob_python": problem_success_python,
    "prob_rust": problem_success_rust,
    "prob_go": problem_success_go,
}


def compute_avg(comps):
    avg_comp = defaultdict(lambda: [0, 0])
    for comp in comps:
        for key in comps[comp]:
            avg_comp[key][0] += comps[comp][key]
            avg_comp[key][1] += 1

    for key in avg_comp:
        avg_comp[key] = avg_comp[key][0] / avg_comp[key][1]

    return avg_comp


avg_comp = compute_avg(comps)
avg_prob = compute_avg(probs)

variables = {
    "comp_cpp": compile_success_cpp,
    "comp_haskell": compile_success_haskell,
    "comp_ocaml": compile_success_ocaml,
    "comp_python": compile_success_python,
    "comp_rust": compile_success_rust,
    "comp_go": compile_success_go,
    "avg_comp": avg_comp,
    "prob_cpp": problem_success_cpp,
    "prob_haskell": problem_success_haskell,
    "prob_ocaml": problem_success_ocaml,
    "prob_python": problem_success_python,
    "prob_rust": problem_success_rust,
    "prob_go": problem_success_go,
    "avg_prob": avg_prob,
}


print_correlation_table(comps, compute_correlation)
print("----")
print_correlation_table(probs, compute_correlation)

print_correlation_table(variables, compute_correlation)

print("----")
print("----")
print("----")
print("----")
corr_matrix = print_correlation_table(variables, compute_rank_correlation)
rhcc = {
    "compiles rust": compile_success_rust,
    "compiles haskell": compile_success_haskell,
    "compiles ocaml": compile_success_ocaml,
    "compiles cpp": compile_success_cpp,
    "correct rust": problem_success_rust,
    "correct haskell": problem_success_haskell,
    "correct ocaml": problem_success_ocaml,
    "correct cpp": problem_success_cpp,
}
corr_matrix = print_correlation_table(rhcc, compute_correlation)
# Find the min corr
vmin = corr_matrix.min().min()
vmax = 1


# Create the plot
plt.figure(figsize=(10, 8))
sns.heatmap(
    corr_matrix,
    annot=True,  # Show the correlation values
    cmap="RdBu",  # Red-Blue diverging colormap
    vmin=vmin,  # Fix the range from -1 to 1
    vmax=vmax,
    center=(vmin + vmax) / 2,
    square=True,  # Make the plot square-shaped
    fmt=".2f",
)  # Round the numbers to 2 decimal places

plt.title("Correlation Compilation and Problem Success")
plt.tight_layout()
plt.show()
