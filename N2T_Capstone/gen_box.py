# gen_box.py - writes Box.asm: waits for a key, draws the box,
# then draws the name and roll number with a 5x7 bitmap font and halts.
NAME, ROLL = "PIYUSH KHARE", "2501730244"
import sys
K, BOX_ROWS = (int(sys.argv[1]) if len(sys.argv) > 1 else 44), 28
W = K % 4 + 1  # box width in words: (K mod 4) + 1
FONT = {
 "P":["####.","#...#","#...#","####.","#....","#....","#...."],
 "I":["#####","..#..","..#..","..#..","..#..","..#..","#####"],
 "Y":["#...#","#...#",".#.#.","..#..","..#..","..#..","..#.."],
 "U":["#...#","#...#","#...#","#...#","#...#","#...#",".###."],
 "S":[".####","#....","#....",".###.","....#","....#","####."],
 "H":["#...#","#...#","#...#","#####","#...#","#...#","#...#"],
 "K":["#...#","#..#.","#.#..","##...","#.#..","#..#.","#...#"],
 "A":[".###.","#...#","#...#","#####","#...#","#...#","#...#"],
 "R":["####.","#...#","#...#","####.","#.#..","#..#.","#...#"],
 "E":["#####","#....","#....","####.","#....","#....","#####"],
 "0":[".###.","#...#","#..##","#.#.#","##..#","#...#",".###."],
 "1":["..#..",".##..","..#..","..#..","..#..","..#..",".###."],
 "2":[".###.","#...#","....#","...#.","..#..",".#...","#####"],
 "3":["####.","....#","....#",".###.","....#","....#","####."],
 "4":["...#.","..##.",".#.#.","#..#.","#####","...#.","...#."],
 "5":["#####","#....","####.","....#","....#","#...#",".###."],
 "7":["#####","....#","...#.","..#..",".#...",".#...",".#..."],
 " ":["....."]*7}
L = []
L += ["// Box.asm - Make the Computer Draw a Box",
 "// Student: Piyush Khare   Roll No.: 2501730244",
 "// Course: Nand to Tetris - I, K.R. Mangalam University",
 "// K = %d, start row = %d, width = 16 * ((%d mod 4) + 1) = %d px" % (K, K, K, 16 * W),
 "// First address = 16384 + 32 * %d = %d" % (K, 16384 + 32 * K),
 "// The screen stays white until a key is pressed. Then the box is",
 "// drawn, the name and roll number are written, and the CPU halts.",
 "(WAIT)","@KBD","D=M","@WAIT","D;JEQ",
 "@%d      // 16384 + 32 * %d" % (16384 + 32 * K, K),"D=A","@addr","M=D",
 "@%d" % BOX_ROWS,"D=A","@n","M=D","(ROW)","@addr","A=M","M=-1"] + ["A=A+1","M=-1"] * (W - 1) + [
 "@addr","D=M","@32","D=D+A","@addr","M=D","@n","M=M-1","D=M","@ROW","D;JGT",
 "// ---- text: each word holds 2 characters (8 pixels each) ----"]
def text(s, y0, w0):
    global L
    L.append("// \"%s\" at pixel row %d" % (s, y0))
    for r in range(7):
        for w in range((len(s) + 1) // 2):
            v = 0
            for c in (2 * w, 2 * w + 1):
                if c < len(s):
                    row = FONT[s[c]][r]
                    v |= sum(1 << x for x in range(5) if row[x] == "#") << (8 * (c % 2))
            if v == 0: continue
            addr = 16384 + 32 * (y0 + r) + w0 + w
            if v < 32768: L += ["@%d" % v, "D=A"]
            else: L += ["@%d" % (~v & 0x7FFF), "D=!A"]
            L += ["@%d" % addr, "M=D"]
text(NAME, 100, 5)
text(ROLL, 116, 5)
L += ["(END)", "@END", "0;JMP"]
open("Box.asm", "w").write("\n".join(L) + "\n")
