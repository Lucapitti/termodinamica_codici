def estrai_colonne(filepath, num_righe=20):
    with open(filepath, 'r') as f:
        righe = [riga.strip() for riga in f.readlines() if riga.strip()]

    # Suddividi in blocchi da 20 righe (una colonna per blocco)
    colonne = [righe[i:i+num_righe] for i in range(0, len(righe), num_righe)]

    # Rimuovi il simbolo iniziale "&" da ogni riga
    colonne = [[val.replace("&", "").strip() for val in colonna] for colonna in colonne]

    return colonne

def stampa_tabella_latex(colonne):
    latex = "\\begin{tabular}{" + "c" * len(colonne) + "}\n"
    for riga in zip(*colonne):  # raggruppa per righe
        latex += " & ".join(riga) + " \\\\\n"
    latex += "\\end{tabular}"
    return latex