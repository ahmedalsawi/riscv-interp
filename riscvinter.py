
import tkinter as tk

from core import isa


def run_assembly():
    asm = txt_asm.get("1.0", tk.END)
    print(str(asm))
    print(lbl_asm["text"])

window = tk.Tk()
window.title("riscv interp")

frm_entry = tk.Frame(master=window, width=200, height = 100, bg= "red")
lbl_asm = tk.Label(master=frm_entry, text="Write assembly", bg="blue")
btn_run = tk.Button(
    master=frm_entry,
    text="\N{RIGHTWARDS BLACK ARROW}",
    command=run_assembly 
)
txt_asm = tk.Text(master=frm_entry)

lbl_output = tk.Label(master=window, width=200, height = 100, bg= "yellow")

frm_entry.grid(row=0, column=0, padx=10)
lbl_asm.grid(row=1, column=0, padx=10)
btn_run.grid(row=2, column=0, pady=10)
txt_asm.grid(row=3, column=0, pady=10)


window.mainloop()