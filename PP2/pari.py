even_file = "data/temp_cut_even.txt"
odd_file = "data/temp_cut_odd.txt"
input_file = "data/temp_acqua_cut.txt"

eps = 1e-8

n_even = n_odd = 0

with open(input_file, "r") as fin, \
     open(even_file, "w") as fev, \
     open(odd_file, "w") as fod:

    for line in fin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 1:
            continue
        try:
            x = float(parts[0])
        except ValueError:
            continue

        # estrai il primo decimale: es. 7.4 -> 4, 8.0 -> 0, 11.25 -> 2
        primo_decimale = int((abs(x) * 10 + eps)) % 10

        if primo_decimale % 2 == 0:
            fev.write(line + "\n")
            n_even += 1
        else:
            fod.write(line + "\n")
            n_odd += 1

print(f"Righe con primo decimale pari: {n_even} -> {even_file}")
print(f"Righe rimanenti: {n_odd} -> {odd_file}")