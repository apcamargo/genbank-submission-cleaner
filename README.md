# genbank-submission-cleaner

This script removes contaminants flagged during GenBank's submission process.

```
usage: genbank-submission-cleaner.py [-h] genbank_report input_genome clean_genome_output

Remove contaminants flagged during GenBank's submission process.

positional arguments:
  genbank_report       GenBank's contamination record file.
  input_genome         Genome to be cleaned.
  clean_genome_output  Directory where the cleaned genome will be written to.

optional arguments:
  -h, --help           Show this help message and exit
```

It takes as input the contamined genome (`input_genome`) and the GenBank's contamination report (`genbank_report`), which should end with something like this:

```
(…)

Trim:
Sequence name, length, span(s), apparent source
contig_1	3795	3754..3795	adaptor:NGB00360.1
contig_2	2219	2197..2219	adaptor:NGB01096.1
contig_3	2039	2010..2039	adaptor:NGB01088.1
contig_4	2228	2210..2228	adaptor:NGB01088.1
contig_5	2024	1..20	adaptor:NGB01088.1
contig_6	3074	3049..3074	adaptor:NGB01096.1
```