"""
genome_mapping_utils.py

Utility functions for the Gopherus polyphemus (gopher tortoise)
genome mapping pipeline. It provides functions for running shell commands, validating input files, extracting sample
names, and parsing alignment statistics.
"""

import subprocess  # subprocess allows Python to run shell commands like minimap2 and samtools
import re          # re provides regular expression support for pattern matching in strings
import os          # os provides functions for interacting with the file system


def run_command(cmd):
    """
    Run a shell command from within Python and check for errors.

    Parameters
    ----------
    cmd : str
        The shell command to run.

    Returns
    -------
    str
        Standard output from the command.

    Raises
    ------
    RuntimeError
        If the command fails.

    Examples
    --------
    >>> output = run_command("samtools view -c sample.bam")
    >>> print(output)
    '871041'
    """
    print(f"Running command: {cmd}")
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed:\n{cmd}\nError:\n{result.stderr}")
    return result.stdout.strip()


def validate_file(filepath):
    """
    Check that a file exists and is not empty.

    Parameters
    ----------
    filepath : str
        Path to the file to validate.

    Returns
    -------
    bool
        True if the file exists and is not empty.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file is empty.

    Examples
    --------
    >>> validate_file("/scratch/amf0120/GT_7.4_B/Mapped_reads/small_subset/aligned.bam")
    True
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    if os.path.getsize(filepath) == 0:
        raise ValueError(f"File is empty: {filepath}")
    print(f"Validated file: {filepath}")
    return True


def extract_sample_name(filepath):
    """
    Extract the sample name from a FASTQ filename using regex.

    Parameters
    ----------
    filepath : str
        Path to the FASTQ file.

    Returns
    -------
    str
        The extracted sample name.

    Raises
    ------
    ValueError
        If the filename does not match the expected pattern.

    Examples
    --------
    >>> extract_sample_name("FBE04231_pass_2ab3b2a5_6a393744_0.fastq.gz")
    'FBE04231'
    """
    filename = os.path.basename(filepath)
    match = re.search(r"^([A-Z0-9]+)_pass", filename)
    if match:
        return match.group(1)
    else:
        raise ValueError(f"Could not extract sample name from: {filename}")


def parse_samtools_stats(stats_output):
    """
    Parse samtools stats output and extract key alignment metrics
    using regex.

    Parameters
    ----------
    stats_output : str
        Raw text output from samtools stats.

    Returns
    -------
    dict
        Dictionary containing total reads, mapped reads, mean length,
        error rate, and calculated mapping rate.

    Examples
    --------
    >>> stats = parse_samtools_stats(output)
    >>> print(stats["mapping_rate"])
    '94.31%'
    """
    metrics = {}
    patterns = {
        "total_reads"  : r"SN\s+raw total sequences:\s+(\d+)",
        "mapped_reads" : r"SN\s+reads mapped:\s+(\d+)",
        "total_bases"  : r"SN\s+total length:\s+(\d+)",
        "mean_length"  : r"SN\s+average length:\s+([\d.]+)",
        "error_rate"   : r"SN\s+error rate:\s+([\d.e+-]+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, stats_output)
        if match:
            metrics[key] = match.group(1)

    if "total_reads" in metrics and "mapped_reads" in metrics:
        total = int(metrics["total_reads"])
        mapped = int(metrics["mapped_reads"])
        if total > 0:
            metrics["mapping_rate"] = f"{(mapped / total * 100):.2f}%"

    return metrics
