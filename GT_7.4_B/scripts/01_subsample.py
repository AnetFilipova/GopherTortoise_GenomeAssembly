#! /usr/bin/env python3

"""

Selects a subset of FASTQ files which are the output files of Oxford Nanopore sequencing for
mapping against the Gopherus flavomarginatus reference genome.
Generates two text files containing the selected FASTQ file paths
which are used by 02_align_reads.py for mapping.

Two subsets are created:
    - Small subset: first 13 files (~10% of data)
    - Large subset: all 135 files (100% of data)
"""

import os

import re

from genome_mapping_utils import validate_file, extract_sample_name


# Define paths
FASTQ_DIR = "/hosted/biosc/SchwartzLab/Nanopore/GopherTortoise/GT_7.4_B/fastq_pass"
OUTPUT_DIR = "/scratch/amf0120/GT_7.4_B"


def get_sorted_fastq_files(fastq_dir):
    """
    Get all FASTQ files from the fastq_pass directory and sort
    them numerically by file number using regex.

    Parameters
    ----------
    fastq_dir : str
        Path to the directory containing FASTQ files.

    Returns
    -------
    list
        Numerically sorted list of full paths to all FASTQ files.

    Raises
    ------
    ValueError
        If no FASTQ files are found in the directory.

    Examples
    --------
    >>> files = get_sorted_fastq_files("/hosted/biosc/.../fastq_pass")
    >>> print(files[0])
    '/hosted/biosc/.../FBE04231_pass_2ab3b2a5_6a393744_0.fastq.gz'
    """
    all_files = os.listdir(fastq_dir)

    # Use regex to filter for .fastq.gz files only
    fastq_files = [f for f in all_files if re.search(r'\.fastq\.gz$', f)]

    if not fastq_files:
        raise ValueError(f"No FASTQ files found in: {fastq_dir}")

    # Use regex to extract file number and sort numerically
    def extract_file_number(filename):
        match = re.search(r'_(\d+)\.fastq\.gz$', filename)
        if match:
            return int(match.group(1))
        return 0

    fastq_files.sort(key=extract_file_number)

    return [os.path.join(fastq_dir, f) for f in fastq_files]


def write_file_list(file_list, output_path):
    """
    Write a list of FASTQ file paths to a text file, one path per line.

    Parameters
    ----------
    file_list : list
        List of full paths to the selected FASTQ files.
    output_path : str
        Path to the output text file.

    Returns
    -------
    None

    Examples
    --------
    >>> write_file_list(small_files, "/scratch/amf0120/GT_7.4_B/small_subset_files.txt")
    Written 13 files to /scratch/amf0120/GT_7.4_B/small_subset_files.txt
    """
    with open(output_path, 'w') as f:
        for filepath in file_list:
            f.write(filepath + '\n')
    print(f"Written {len(file_list)} files to {output_path}")


def main():
    """
    Select small and large subsets of FASTQ files and write
    their paths to text files for use by 02_align_reads.py.
    """
    print("Starting FASTQ subsetting for GT_7.4_B")

    # Get all sorted FASTQ files
    all_files = get_sorted_fastq_files(FASTQ_DIR)
    print(f"Found {len(all_files)} FASTQ files in total")

    # Extract sample name and validate first file
    sample_name = extract_sample_name(all_files[0])
    print(f"Sample name: {sample_name}")
    validate_file(all_files[0])

    # Select subsets
    small_subset = all_files[:SMALL_SUBSET_SIZE]
    large_subset = all_files[:LARGE_SUBSET_SIZE]
    print(f"Small subset: {len(small_subset)} files selected")
    print(f"Large subset: {len(large_subset)} files selected")

    # Write file lists
    write_file_list(small_subset, os.path.join(OUTPUT_DIR, "small_subset_files.txt"))
    write_file_list(large_subset, os.path.join(OUTPUT_DIR, "large_subset_files.txt"))

    print("Subsetting complete!")


if __name__ == '__main__':
    main()
