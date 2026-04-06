#! /usr/bin/env python3

"""

Compares alignment results from the small and large subsets mapped
against the Gopherus flavomarginatus reference genome. Runs samtools
stats on both BAM files, extracts key metrics using regex, and writes
a comparison summary to a text file.

"""

import os
import sys
from genome_mapping_utils import run_command, validate_file, parse_samtools_stats


# Define paths
BAM_FILES = {
    "small": "/scratch/amf0120/GT_7.4_B/Mapped_reads/small_subset/FBE04231_small.bam",
    "large": "/scratch/amf0120/GT_7.4_B/Mapped_reads/large_subset/FBE04231_large.bam"
}
SUMMARY_FILE = "/scratch/amf0120/GT_7.4_B/results/alignment_summary.txt"


def get_stats(bam_file):
    """
    Run samtools stats on a BAM file and parse the output.

    Parameters
    ----------
    bam_file : str
        Path to the sorted and indexed BAM file.

    Returns
    -------
    dict
        Dictionary of alignment metrics.

    Examples
    --------
    >>> stats = get_stats("/scratch/amf0120/GT_7.4_B/Mapped_reads/small_subset/FBE04231_small.bam")
    >>> print(stats["mapping_rate"])
    '99.62%'
    """
    validate_file(bam_file)
    print(f"Running samtools stats on {os.path.basename(bam_file)}...")
    stats_output = run_command(f"samtools stats {bam_file}")
    return parse_samtools_stats(stats_output)


def write_summary(small_stats, large_stats, output_path):
    """
    Write a formatted comparison of small and large subset alignment
    statistics to a text file.

    Parameters
    ----------
    small_stats : dict
        Alignment metrics for the small subset.
    large_stats : dict
        Alignment metrics for the large subset.
    output_path : str
        Path to the output summary text file.

    Returns
    -------
    None

    Examples
    --------
    >>> write_summary(small_stats, large_stats, "/scratch/amf0120/GT_7.4_B/results/alignment_summary.txt")
    Summary written to /scratch/amf0120/GT_7.4_B/results/alignment_summary.txt
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("Alignment Summary: Small vs Large Subset\n")
        f.write("Sample: FBE04231 (Gopherus polyphemus - GT_7.4_B)\n")
        f.write("Reference: Gopherus flavomarginatus\n")
        f.write("=" * 60 + "\n")
        f.write(f"{'Metric':<20} {'Small (13 files)':<20} {'Large (135 files)':<20}\n")
        f.write("-" * 60 + "\n")

        metrics = [
            ("Total reads",  "total_reads"),
            ("Mapped reads", "mapped_reads"),
            ("Mapping rate", "mapping_rate"),
            ("Mean length",  "mean_length"),
            ("Error rate",   "error_rate"),
        ]

        for label, key in metrics:
            small_val = small_stats.get(key, "N/A")
            large_val = large_stats.get(key, "N/A")
            f.write(f"{label:<20} {small_val:<20} {large_val:<20}\n")

        f.write("=" * 60 + "\n")

    print(f"Summary written to {output_path}")


def main():
    """
    Run samtools stats on BAM files and write a comparison
    summary to a text file. Optionally specify a single subset.
    
    Usage:
        python3 03_summarize_results.py          # runs both subsets
        python3 03_summarize_results.py small    # runs small subset only
        python3 03_summarize_results.py large    # runs large subset only
    """
    print("Starting alignment summary...")

    # Check if a specific subset was requested
    if len(sys.argv) == 2 and sys.argv[1] in ["small", "large"]:
        requested = [sys.argv[1]]
    else:
        requested = ["small", "large"]

    # Check which BAM files are available
    available = {}
    for subset in requested:
        bam_file = BAM_FILES[subset]
        if os.path.exists(bam_file):
            available[subset] = bam_file
        else:
            print(f"Warning: {subset} subset BAM file not found, skipping...")

    if not available:
        print("No BAM files found. Please run 02_align_reads.py first.")
        sys.exit(1)

    # Get stats for available subsets
    stats = {}
    for subset, bam_file in available.items():
        print(f"Processing {subset} subset...")
        stats[subset] = get_stats(bam_file)

    # Write summary
    write_summary(stats.get("small", {}), stats.get("large", {}), SUMMARY_FILE)

    # Print summary to screen
    print("\n")
    with open(SUMMARY_FILE, 'r') as f:
        print(f.read())


if __name__ == '__main__':
    main()
