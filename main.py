import tkinter as tk
from app.gui import FinanceVaultPro
from app.database import initialize_db

if __name__ == "__main__":

    initialize_db()

    root = tk.Tk()
    app = FinanceVaultPro(root)
    root.mainloop()