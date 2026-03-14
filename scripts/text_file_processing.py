input_file = r"C:\Users\aksha\Documents\makerCheckerAgent\source_documents\better-writer-handbook-and-tutorials.txt"
output_file = r"C:\Users\aksha\Documents\makerCheckerAgent\source_documents\better-writer-handbook-and-tutorials(proccessed).txt"

with (
    open(input_file, "r", encoding="utf-8") as infile,
    open(output_file, "w", encoding="utf-8") as outfile,
):
    for line in infile:
        if line.strip():  # only keep non-empty lines
            outfile.write(line)
