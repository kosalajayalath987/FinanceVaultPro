import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from datetime import datetime
import os


# PDF Generation Imports
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

# Path Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


class FinanceVaultPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Corporate PettyCash Control - DR/CR System")
        self.root.geometry("1100x850")
        self.root.configure(bg="#f1f2f6")

        self.COMPANY_TITLE = "KSB ENTERPRISE SOLUTIONS LTD"
        self.currency = "Rs."

        # Database Configuration
        self.db_config = {
            'host': "localhost",
            'user': "root",
            'password': "",
            'database': "petty_cash_mgt"
        }

        self.connect_vault()
        self.setup_ui_architecture()
        self.refresh_financial_view()

    def connect_vault(self):
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor(dictionary=True)
        except Exception as e:
            messagebox.showerror("System Error", f"Database Link Failed: {e}")

    def setup_ui_architecture(self):
        # --- Sidebar ---
        sidebar = tk.Frame(self.root, bg="#2c3e50", width=240)
        sidebar.pack(side="left", fill="y")

        # Load Logo from Assets
        logo_path = os.path.join(ASSETS_DIR, "images", "company_logo.png")
        if os.path.exists(logo_path):
            img = Image.open(logo_path).resize((180, 60), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(sidebar, image=self.logo_img, bg="#2c3e50").pack(pady=30)
        else:
            tk.Label(sidebar, text="KSB ENTERPRISE", fg="white", bg="#2c3e50", font=("Arial", 12, "bold")).pack(pady=30)

        btn_style = {"bg": "#34495e", "fg": "white", "relief": "flat", "font": ("Arial", 10), "pady": 12,
                     "cursor": "hand2"}
        tk.Button(sidebar, text="🔄 RELOAD LEDGER", **btn_style, command=self.refresh_financial_view).pack(fill="x",
                                                                                                          padx=15,
                                                                                                          pady=5)
        tk.Button(sidebar, text="📄 FULL AUDIT PDF", **btn_style, command=self.export_full_audit_pdf).pack(fill="x",
                                                                                                          padx=15,
                                                                                                          pady=5)

        # --- Main Content ---
        self.main = tk.Frame(self.root, bg="#f1f2f6")
        self.main.pack(side="right", expand=True, fill="both", padx=25)

        # KPI Cards
        card_frame = tk.Frame(self.main, bg="#f1f2f6")
        card_frame.pack(fill="x", pady=20)
        self.total_bal = self.create_kpi_card(card_frame, "CURRENT LIQUIDITY", "#2ecc71")
        self.session_cr = self.create_kpi_card(card_frame, "TOTAL CREDITS (+)", "#1e90ff")
        self.session_dr = self.create_kpi_card(card_frame, "TOTAL DEBITS (-)", "#e74c3c")

        # Transaction Registry Form
        form = tk.LabelFrame(self.main, text=" LEDGER TRANSACTION REGISTRY ", bg="white", font=("Arial", 9, "bold"),
                             padx=20, pady=15)
        form.pack(fill="x", pady=5)

        tk.Label(form, text="Mode:", bg="white").grid(row=0, column=0, sticky="w")
        self.entry_mode = ttk.Combobox(form, values=["Debit (Expense)", "Credit (Top-up)"], width=20)
        self.entry_mode.set("Debit (Expense)")
        self.entry_mode.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form, text="Narration:", bg="white").grid(row=0, column=2, sticky="w")
        self.entry_desc = tk.Entry(form, width=40)
        self.entry_desc.grid(row=0, column=3, padx=10)

        tk.Label(form, text="Amount (Rs.):", bg="white").grid(row=1, column=0, sticky="w")
        self.entry_amt = tk.Entry(form, width=23)
        self.entry_amt.grid(row=1, column=1, padx=10)

        tk.Label(form, text="Authorized By:", bg="white").grid(row=1, column=2, sticky="w")
        self.entry_auth = ttk.Combobox(form, values=self.fetch_users(), width=38)
        self.entry_auth.grid(row=1, column=3, padx=10)

        tk.Button(form, text="POST TRANSACTION", bg="#2980b9", fg="white", font=("Arial", 10, "bold"),
                  command=self.post_transaction, padx=30).grid(row=2, column=3, sticky="e", pady=10)

        # Live Ledger
        self.ledger = ttk.Treeview(self.main, columns=("ID", "DATE", "DESC", "AMT", "FLOW"), show="headings", height=15)
        headers = ["Ref ID", "Date/Time", "Narration", "Value (Rs.)", "Mode"]
        for col, h in zip(self.ledger["columns"], headers):
            self.ledger.heading(col, text=h)
            self.ledger.column(col, width=150 if col == "DESC" else 100)
        self.ledger.pack(fill="both", expand=True, pady=10)

    def create_kpi_card(self, parent, label, color):
        f = tk.Frame(parent, bg="white", padx=15, pady=15, highlightbackground="#dcdde1", highlightthickness=1)
        f.pack(side="left", expand=True, fill="x", padx=5)
        tk.Label(f, text=label, bg="white", fg="#7f8c8d", font=("Arial", 9, "bold")).pack()
        v = tk.StringVar(value="0.00")
        tk.Label(f, textvariable=v, bg="white", fg=color, font=("Arial", 18, "bold")).pack()
        return v

    def fetch_users(self):
        try:
            self.cursor.execute("SELECT username FROM users")
            return [r['username'] for r in self.cursor.fetchall()]
        except:
            return ["System Admin"]

    def refresh_financial_view(self):
        # Update Balance
        self.cursor.execute("SELECT balance FROM funds WHERE fund_id = 1")
        res = self.cursor.fetchone()
        self.total_bal.set(f"Rs.{res['balance'] if res else 0.0:,.2f}")

        # Refresh Ledger Table
        for i in self.ledger.get_children(): self.ledger.delete(i)
        self.cursor.execute("SELECT * FROM transactions ORDER BY created_at DESC LIMIT 20")

        t_cr, t_dr = 0, 0
        for r in self.cursor.fetchall():
            is_credit = "Credit" in r['description']
            mode = "CREDIT (+)" if is_credit else "DEBIT (-)"

            if is_credit:
                t_cr += float(r['amount'])
            else:
                t_dr += float(r['amount'])

            tag = 'cr' if is_credit else 'dr'
            self.ledger.insert("", "end", values=(r['tx_id'], r['created_at'].strftime("%Y-%m-%d %H:%M"),
                                                  r['description'], f"Rs.{abs(r['amount']):,.2f}", mode), tags=(tag,))

        self.session_cr.set(f"Rs.{t_cr:,.2f}")
        self.session_dr.set(f"Rs.{t_dr:,.2f}")
        self.ledger.tag_configure('cr', foreground="#2ecc71")
        self.ledger.tag_configure('dr', foreground="#e74c3c")

    def post_transaction(self):
        mode, desc, auth = self.entry_mode.get(), self.entry_desc.get(), self.entry_auth.get()
        try:
            val = float(self.entry_amt.get())
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid numeric amount.")
            return

        impact = val if "Credit" in mode else -val
        final_desc = f"{mode}: {desc}"

        try:
            # Atomic update: Insert transaction and update balance
            self.cursor.execute(
                "INSERT INTO transactions (fund_id, amount, description, approved_by) VALUES (1, %s, %s, %s)",
                (val, final_desc, auth))
            self.cursor.execute("UPDATE funds SET balance = balance + %s WHERE fund_id = 1", (impact,))
            self.conn.commit()

            if "Debit" in mode:
                self.generate_dr_voucher(desc, val, auth)

            self.refresh_financial_view()
            self.entry_desc.delete(0, tk.END)
            self.entry_amt.delete(0, tk.END)
            messagebox.showinfo("Success", "Ledger updated successfully.")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Database Error", str(e))

    def generate_dr_voucher(self, d, a, u):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(OUTPUT_DIR, f"Voucher_{timestamp}.pdf")

        c = canvas.Canvas(filename, pagesize=A4)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 800, self.COMPANY_TITLE)
        c.setFont("Helvetica", 12)
        c.drawString(50, 780, "OFFICIAL DEBIT VOUCHER")
        c.line(50, 775, 550, 775)

        c.setFont("Helvetica", 10)
        c.drawString(50, 750, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        c.drawString(50, 730, f"Description: {d}")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 710, f"TOTAL DEBIT: {self.currency} {a:,.2f}")

        c.line(50, 630, 200, 630)
        c.drawString(50, 615, "Recipient Signature")
        c.line(350, 630, 500, 630)
        c.drawString(350, 615, f"Authorized by: {u}")
        c.save()

    def export_full_audit_pdf(self):
        filename = filedialog.asksaveasfilename(initialdir=OUTPUT_DIR, defaultextension=".pdf",
                                                initialfile="Treasury_Audit_Statement.pdf")
        if not filename: return

        c = canvas.Canvas(filename, pagesize=A4)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(300, 800, "Audit Trail: Petty Cash Flow")

        data = [["Date", "Narration", "Amount", "Authorized"]]
        self.cursor.execute("SELECT * FROM transactions ORDER BY created_at DESC")
        for r in self.cursor.fetchall():
            data.append(
                [r['created_at'].strftime("%d-%m-%y"), r['description'][:30], f"{r['amount']:,.2f}", r['approved_by']])

        table = Table(data, colWidths=[80, 220, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (2, 1), (2, -1), 'RIGHT')
        ]))
        table.wrapOn(c, 50, 700)
        table.drawOn(c, 50, 750 - (len(data) * 20))
        c.save()
        messagebox.showinfo("Exported", f"Audit report saved to {filename}")