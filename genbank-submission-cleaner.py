#!/usr/bin/env python

import argparse
import re
import textwrap
from collections import defaultdict
from pathlib import Path
from Bio import SeqIO

parser = argparse.ArgumentParser(
    description="Remove contaminants flagged during GenBank's submission process.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    add_help=False,
)
parser.add_argument(
    "genbank_report", type=Path, help="GenBank's contamination record file."
)
parser.add_argument("input_genome", type=Path, help="Genome to be cleaned.")
parser.add_argument(
    "clean_genome_output",
    type=Path,
    help="Directory where the cleaned genome will be written to.",
)
parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
args = parser.parse_args()


input_genome_basename = args.input_genome.name

if not args.clean_genome_output.is_dir():
    args.clean_genome_output.mkdir()

output_genome_path = args.clean_genome_output.joinpath(input_genome_basename)

contaminant_intervals = defaultdict(list)

with open(args.genbank_report) as fin:
    skip_line = True
    for line in fin:
        if skip_line:
            continue
        if line.startswith("Sequence name,"):
            skip_line = False
        elif len(line) > 1:
            line = line.strip().split()
            contig = line[0]
            for interval in line[2].split(","):
                interval = interval.split("..")
                # Convert 1-based index into 0-based index
                interval = tuple(map(lambda x: int(x) - 1, interval))
                contaminant_intervals[contig].append(interval)

with open(args.input_genome) as fin, open(output_genome_path, "w") as fout:
    for record in SeqIO.parse(fin, "fasta"):
        if record.description in contaminant_intervals:
            sequence = str(record.seq)
            for interval in contaminant_intervals[record.description]:
                sequence = (
                    sequence[0 : interval[0]]
                    + "#" * (interval[1] - interval[0] + 1)
                    + sequence[interval[1] + 1 :]
                )
            sequence = re.split("#+", sequence)
            keep_substrings = [i for i in range(len(sequence)) if len(sequence[i]) >= 200]
            if len(keep_substrings) > 1:
                for substrings_counter, substring_index in enumerate(keep_substrings, start=1):
                    subsequence_name = record.description.split()
                    subsequence_name[0] = f"{subsequence_name[0]}_{substrings_counter}"
                    subsequence_name = "".join(subsequence_name)
                    fout.write(f">{subsequence_name}\n")
                    fout.write(f"{textwrap.fill(sequence[substring_index], 70)}\n")
            else:
                fout.write(f">{record.description}\n")
                fout.write(f"{textwrap.fill(sequence[keep_substrings[0]], 70)}\n")
        else:
            fout.write(f">{record.description}\n")
            fout.write(f"{textwrap.fill(str(record.seq), 70)}\n")

