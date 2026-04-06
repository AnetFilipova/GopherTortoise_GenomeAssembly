#! /usr/bin/env python3

"""

Reads the alignment summary file produced by 03_summarize_results.py,
calculates estimated genome coverage depth for each subset, and
generates a bar chart comparing coverage between the small and large
subsets of Gopherus polyphemus (GT_7.4_B).

"""

import re
import matplotlib.pyplot as plt

# Define paths
SUMMARY_FILE = "/scratch/amf0120/GT_7.4_B/results/alignment_summary.txt"
OUTPUT_FIGURE = "/scratch/amf0120/GT_7.4_B/results/coverage_comparison.png"

# Gopher tortoise genome size in bases (~2.4 GB)
GENOME_SIZE = 2400000000


def parse_summary(filepath):
    """
    Read the alignment summary file and extract total bases for
    each subset using regex.

    Parameters
    ----------
    filepath : str
        Path to the alignment summary text file.

    Returns
    -------
    dict
        Dictionary with total bases for small and large subsets.

    Examples
    --------
    >>> stats = parse_summary("/scratch/amf0120/GT_7.4_B/results/alignment_summary.txt")
    >>> print(stats["small"])
    916054490
    """
    stats = {}
    with open(filepath, 'r') as f:
        content = f.read()

    # Use regex to extract total bases for each subset
    match = re.search(r'Total bases\s+(\d+)\s+(\d+)', content)
    if match:
        stats["small"] = int(match.group(1))
        stats["large"] = int(match.group(2))

    return stats


def calculate_coverage(total_bases, genome_size):
    """
    Calculate estimated genome coverage depth.

    Coverage depth is calculated as total bases sequenced divided
    by the genome size. It represents how many times on average
    each base in the genome is covered by a read.

    Parameters
    ----------
    total_bases : int
        Total number of bases sequenced.
    genome_size : int
        Size of the reference genome in bases.

    Returns
    -------
    float
        Estimated coverage depth.

    Examples
    --------
    >>> calculate_coverage(916054490, 2400000000)
    0.38
    """
    return round(total_bases / genome_size, 2)


def plot_coverage(small_coverage, large_coverage, output_path):
    """
    Generate a bar chart comparing coverage depth between
    small and large subsets.

    Parameters
    ----------
    small_coverage : float
        Coverage depth for the small subset.
    large_coverage : float
        Coverage depth for the large subset.
    output_path : str
        Path to save the output figure.

    Returns
    -------
    None

    Examples
    --------
    >>> plot_coverage(0.38, 2.14, "/scratch/amf0120/GT_7.4_B/results/coverage_comparison.png")
    Figure saved to /scratch/amf0120/GT_7.4_B/results/coverage_comparison.png
    """
    subsets = ["Small (13 files)", "Large (135 files)"]
    coverage = [small_coverage, large_coverage]

    fig, ax = plt.subplots()
    bars = ax.bar(subsets, coverage, color=["steelblue", "darkorange"])

    # Add value labels on top of each bar
    for bar, val in zip(bars, coverage):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{val}x", ha="center", va="bottom", fontsize=12)

    ax.set_title("Estimated Genome Coverage Depth\nGopherus polyphemus (GT_7.4_B)")
    ax.set_xlabel("Subset")
    ax.set_ylabel("Coverage Depth (x)")

    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Figure saved to {output_path}")


def main():
    """
    Read alignment summary, calculate coverage depth for each
    subset and generate a coverage comparison bar chart.
    """
    print("Reading alignment summary...")
    stats = parse_summary(SUMMARY_FILE)

    if not stats:
        print("Could not parse total bases from summary file.")
        print("Please make sure 03_summarize_results.py has been run first.")
        return

    # Calculate coverage for each subset
    small_coverage = calculate_coverage(stats["small"], GENOME_SIZE)
    large_coverage = calculate_coverage(stats["large"], GENOME_SIZE)

    print(f"Small subset coverage: {small_coverage}x")
    print(f"Large subset coverage: {large_coverage}x")

    # Generate figure
    plot_coverage(small_coverage, large_coverage, OUTPUT_FIGURE)


if __name__ == '__main__':
    main()
