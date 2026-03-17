import tkinter as tk
from tkinter import scrolledtext, messagebox

# --- EXHAUSTIVE DATABASE FROM ALL 6 PDF PAGES ---
ir_db = [
    # ALKANES (Pages 1-2)
    {"g": "Alkane (-CH3)", "min": 2950, "max": 2970, "m": "Antisym str", "r": "Strong (s)"},
    {"g": "Alkane (-CH3)", "min": 2860, "max": 2880, "m": "Sym str", "r": "Strong (s)"},
    {"g": "Alkane (CH2)", "min": 2915, "max": 2935, "m": "Antisym str", "r": "Strong (s)"},
    {"g": "Alkane (CH2)", "min": 2845, "max": 2865, "m": "Sym str", "r": "Strong (s)"},
    {"g": "Alkane (CH)", "min": 2880, "max": 2900, "m": "Str", "r": "Weak (w), often masked"},
    {"g": "Alkane (CH3)", "min": 1370, "max": 1470, "m": "Antisym/Sym def", "r": "Medium (m)"},
    {"g": "Alkane (CH2)", "min": 720, "max": 730, "m": "Rocking", "r": "Weak (w) ~725 cm-1"},

    # ALKENES (Page 2)
    {"g": "Alkene (Terminal)", "min": 3075, "max": 3095, "m": "str CH2", "r": "Medium (m)"},
    {"g": "Alkene (Internal)", "min": 3010, "max": 3040, "m": "str CH", "r": "Medium (m)"},
    {"g": "Alkene (C=C)", "min": 1620, "max": 1680, "m": "C=C str", "r": "Variable (v)"},
    {"g": "Alkene (trans)", "min": 960, "max": 970, "m": "C-H def", "r": "Strong (s)"},
    {"g": "Alkene (cis)", "min": 675, "max": 730, "m": "C-H def", "r": "Strong (s) ~690"},

    # ALKYNES (Page 2)
    {"g": "Alkyne (Terminal)", "min": 3310, "max": 3320, "m": "C-H str", "r": "Strong (s), SHARP"},
    {"g": "Alkyne (Monosubst)", "min": 2100, "max": 2140, "m": "C#C str", "r": "Medium (m)"},
    {"g": "Alkyne (Disubst)", "min": 2190, "max": 2260, "m": "C#C str", "r": "Weak (w)"},

    # AROMATICS (Page 3)
    {"g": "Aromatic (Ar-H)", "min": 3010, "max": 3040, "m": "C-H str", "r": "Variable, Sharp"},
    {"g": "Aromatic Ring", "min": 1450, "max": 1600, "m": "C=C str", "r": "Multiple bands (m)"},
    {"g": "Aromatic (Mono)", "min": 730, "max": 770, "m": "C-H def", "r": "Strong (s)"},
    {"g": "Aromatic (ortho)", "min": 735, "max": 770, "m": "C-H def", "r": "Strong (s)"},
    {"g": "Aromatic (meta)", "min": 750, "max": 810, "m": "C-H def", "r": "Strong (s)"},
    {"g": "Aromatic (para)", "min": 800, "max": 860, "m": "C-H def", "r": "Strong (s)"},

    # CARBONYLS & ACIDS (Pages 3-4)
    {"g": "Ketone (Acyclic)", "min": 1705, "max": 1725, "m": "C=O str", "r": "Strong (s)"},
    {"g": "Aldehyde (Sat)", "min": 1730, "max": 1740, "m": "C=O str", "r": "Strong (s)"},
    {"g": "Aldehyde (C-H)", "min": 2700, "max": 2850, "m": "C-H str", "r": "Weak doublet"},
    {"g": "Carboxylic Acid", "min": 1700, "max": 1725, "m": "C=O str", "r": "Strong (s)"},
    {"g": "Acid (O-H)", "min": 2500, "max": 3300, "m": "O-H str", "r": "Extremely BROAD"},
    {"g": "Ester (Sat)", "min": 1735, "max": 1750, "m": "C=O str", "r": "Strong (s)"},
    {"g": "Anhydride", "min": 1800, "max": 1850, "m": "C=O str", "r": "Doublet pattern"},

    # ALCOHOLS & AMINES (Page 5)
    {"g": "Alcohol (Free)", "min": 3600, "max": 3650, "m": "O-H str", "r": "SHARP (v)"},
    {"g": "Alcohol (H-bond)", "min": 3200, "max": 3400, "m": "O-H str", "r": "BROAD and Strong"},
    {"g": "Amine (Primary)", "min": 3300, "max": 3500, "m": "N-H str", "r": "Doublet (m)"},
    {"g": "Amine (Secondary)", "min": 3300, "max": 3500, "m": "N-H str", "r": "Singlet (m)"},
    {"g": "Amide (C=O)", "min": 1630, "max": 1690, "m": "Amide I", "r": "Strong (s)"},
    {"g": "Amide (N-H)", "min": 1515, "max": 1570, "m": "Amide II", "r": "Medium (m)"},

    # NITRILES & NITRO (Page 6)
    {"g": "Nitrile", "min": 2215, "max": 2260, "m": "CN str", "r": "Strong (s)"},
    {"g": "Nitro (Aliph/Ar)", "min": 1530, "max": 1560, "m": "NO2 Antisym", "r": "Strong (s)"},
    {"g": "Nitro (Aliph/Ar)", "min": 1320, "max": 1390, "m": "NO2 Sym", "r": "Strong (s)"},
    {"g": "Chloro Comp.", "min": 600, "max": 800, "m": "C-Cl str", "r": "Strong (s)"},
    {"g": "Bromo Comp.", "min": 500, "max": 600, "m": "C-Br str", "r": "Strong (s)"}
]

def analyze():
    raw = entry.get()
    output.delete(1.0, tk.END)
    try:
        if '-' in raw:
            h, l = map(float, raw.split('-'))
            p_high, p_low = max(h, l), min(h, l)
        else:
            p_high = p_low = float(raw)
        
        found = False
        res_text = f"IR INTERPRETATION REPORT\n{'='*30}\n"
        for item in ir_db:
            if not (p_high < item['min'] or p_low > item['max']):
                res_text += f"• GROUP: {item['g']}\n  MODE: {item['m']}\n  NOTE: {item['r']}\n{'-'*30}\n"
                found = True
        
        if not found:
            res_text += "No match found in PDF database."
        output.insert(tk.END, res_text)
    except:
        messagebox.showerror("Error", "Enter numbers (e.g. 1715) or ranges (e.g. 3200-3400)")

# --- GUI SETUP ---
root = tk.Tk()
root.title("IR Interpreter for Scientists")

tk.Label(root, text="IR Spectrum Interpretation", font=("Arial", 14, "bold")).pack(pady=10)
entry = tk.Entry(root, width=35, justify='center', font=("Arial", 12))
entry.pack(pady=5)
entry.insert(0, "1715") # Default example

tk.Button(root, text="INTERPRET RESULTS", command=analyze, bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

output = scrolledtext.ScrolledText(root, width=45, height=18, font=("Courier", 10))
output.pack(padx=10, pady=10)

root.mainloop()
