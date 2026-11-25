# assembler.py - Hack assembler (Nand to Tetris capstone, Part B)
# Usage: python assembler.py Box.asm   -> writes Box.hack
import sys

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101",
}
JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}


def clean(line):
    """Remove comments and all whitespace."""
    return line.split("//")[0].replace(" ", "").replace("\t", "").strip()


def assemble(lines):
    symbols = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
               "SCREEN": 16384, "KBD": 24576}
    for i in range(16):
        symbols["R" + str(i)] = i

    # Pass 1: record labels
    code = []
    for line in lines:
        line = clean(line)
        if not line:
            continue
        if line.startswith("("):
            symbols[line[1:-1]] = len(code)
        else:
            code.append(line)

    # Pass 2: translate
    next_var = 16
    out = []
    for line in code:
        if line.startswith("@"):
            value = line[1:]
            if value.isdigit():
                n = int(value)
            else:
                if value not in symbols:
                    symbols[value] = next_var
                    next_var += 1
                n = symbols[value]
            out.append(format(n, "016b"))
        else:
            dest, jump = "", ""
            comp = line
            if "=" in comp:
                dest, comp = comp.split("=")
            if ";" in comp:
                comp, jump = comp.split(";")
            d = ("1" if "A" in dest else "0") + \
                ("1" if "D" in dest else "0") + \
                ("1" if "M" in dest else "0")
            out.append("111" + COMP[comp] + d + JUMP[jump])
    return out


def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".asm"):
        print("Usage: python assembler.py File.asm")
        sys.exit(1)
    path = sys.argv[1]
    with open(path) as f:
        result = assemble(f.readlines())
    outpath = path[:-4] + ".hack"
    with open(outpath, "w") as f:
        f.write("\n".join(result) + "\n")
    print("Wrote", outpath, "-", len(result), "instructions")


if __name__ == "__main__":
    main()
