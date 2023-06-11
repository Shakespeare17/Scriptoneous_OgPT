import re
import sys

def extract_code_blocks(filename):
    with open(filename, 'r') as file:
        content = file.read()

    code_blocks = re.findall(r'```([\s\S]+?)```', content, re.MULTILINE)
    return code_blocks

# Check if file(s) and verbosity flag are provided as arguments
if len(sys.argv) > 1:
    verbose = False
    output_file = None

    if "--verbose" in sys.argv:
        verbose = True
        sys.argv.remove("--verbose")

    if len(sys.argv) > 1:
        output_file = sys.argv[-1]
        sys.argv = sys.argv[:-1]

    for arg in sys.argv[1:]:
        code_blocks = extract_code_blocks(arg)

        if verbose:
            for code_block in code_blocks:
                print(code_block)

        if output_file:
            with open(output_file, 'a') as file:
                file.write('\n\n'.join(code_blocks) + '\n\n')
else:
    # Prompt the user for file(s) interactively
    file_input = input("Enter the path to the Markdown file(s), separated by spaces: ")
    files = file_input.split()

    verbose_input = input("Output to standard output as well? (y/n): ")
    verbose = True if verbose_input.lower() == 'y' else False

    output_file = input("Enter the path to the output file: ")

    for file in files:
        code_blocks = extract_code_blocks(file)

        if verbose:
            for code_block in code_blocks:
                print(code_block)

        if output_file:
            with open(output_file, 'a') as file:
                file.write('\n\n'.join(code_blocks) + '\n\n')