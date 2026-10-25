import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext, filedialog
import sqlite3
import platform
import re
import socket
import hashlib
import base64
from urllib.parse import urlparse
import threading

# =====================================================================
# DATABASE CONFIGURATION
# =====================================================================
db_connection = sqlite3.connect('cybersuite.db')
db_cursor = db_connection.cursor()

db_cursor.execute('''CREATE TABLE IF NOT EXISTS blocked_domains
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   domain TEXT NOT NULL UNIQUE)''')

db_cursor.execute('''CREATE TABLE IF NOT EXISTS audit_logs
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                   module TEXT NOT NULL,
                   assessment_result TEXT NOT NULL)''')
db_connection.commit()

default_target_registry = ["www.facebook.com", "facebook.com", "www.youtube.com", "youtube.com", "www.instagram.com", "instagram.com"]
for target_site in default_target_registry:
    try:
        db_cursor.execute("INSERT INTO blocked_domains (domain) VALUES (?)", (target_site,))
    except sqlite3.IntegrityError:
        pass
db_connection.commit()

# =====================================================================
# OS HOSTS FILE PATH CONFIGURATION
# =====================================================================
if platform.system() == "Windows":
    hosts_file_path = r"C:\Windows\System32\drivers\etc\hosts"
else:
    hosts_file_path = "/etc/hosts"

redirect_loopback_ip = "127.0.0.1"

# =====================================================================
# SECURITY ASSESSMENT THRESHOLDS & LEXICONS
# =====================================================================
PHISHING_KEYWORDS = ['login', 'verify', 'account', 'update', 'secure', 'banking', 'signin', 'confirm']
SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top']
POPULAR_DOMAINS = ['facebook.com', 'google.com', 'amazon.com', 'apple.com', 'microsoft.com', 'paypal.com', 'instagram.com']

SCAM_SMS_KEYWORDS = [
    "otp", "verify", "bank", "click", "winner", "lottery", "prize",
    "urgent", "free", "gift", "reward", "claim", "password",
    "account suspended", "kyc", "loan approved"
]

# =====================================================================
# UI STYLE & THEME CONFIGURATION (Cyberpunk Dark Mode)
# =====================================================================
BG_DARK = "#090d16"
BG_PANEL = "#111827"
FG_PRIMARY = "#f3f4f6"
FG_MUTED = "#9ca3af"
ACCENT_CYAN = "#06b6d4"
ACCENT_GREEN = "#10b981"
ACCENT_AMBER = "#f59e0b"
ACCENT_CRIMSON = "#ef4444"

FONT_TITLE = ("Courier New", 24, "bold")
FONT_SUBTITLE = ("Arial", 10, "italic")
FONT_HEADER = ("Arial", 14, "bold")
FONT_BODY = ("Arial", 10)
FONT_TERMINAL = ("Courier New", 10) 

root_window = tk.Tk()
root_window.title("CyberSuite Pro - Advanced Security Toolkit")
root_window.geometry("1180x900")  
root_window.configure(bg=BG_DARK)

header_frame = tk.Frame(root_window, bg=BG_DARK)
header_frame.pack(fill="x", pady=(15, 5))

tk.Label(header_frame, text="⚡ CYBERSUITE PRO ⚡", font=FONT_TITLE, bg=BG_DARK, fg=ACCENT_CYAN).pack()
tk.Label(header_frame, text="NetBlocker • Email Analyzer • Scam SMS • PhishGuard • PasswordChecker • PortScanner • FileHasher • SubRecon • CryptoXOR • AuditLogs", font=FONT_SUBTITLE, bg=BG_DARK, fg=FG_MUTED).pack(pady=(4, 0))

notebook_style = ttk.Style()
notebook_style.theme_use('default')
notebook_style.configure("TNotebook", background=BG_DARK, borderwidth=0)
notebook_style.configure("TNotebook.Tab", background=BG_PANEL, foreground=FG_MUTED, padding=[12, 6], font=('Arial', 10, 'bold'), borderwidth=1)
notebook_style.map("TNotebook.Tab", background=[("selected", ACCENT_CYAN)], foreground=[("selected", BG_DARK)])

main_notebook = ttk.Notebook(root_window)
main_notebook.pack(pady=(5, 10), padx=15, expand=True, fill="both")

def create_styled_entry(parent, **kwargs):
    if 'font' not in kwargs:
        kwargs['font'] = FONT_BODY
    return tk.Entry(parent, bg=BG_DARK, fg=FG_PRIMARY, insertbackground=FG_PRIMARY, bd=1, relief="solid", highlightthickness=1, highlightbackground=BG_PANEL, highlightcolor=ACCENT_CYAN, **kwargs)

def create_styled_button(parent, text, command, color, fg_color="white", **kwargs):
    return tk.Button(parent, text=text, command=command, bg=color, fg=fg_color, activebackground=color, activeforeground=fg_color, font=("Arial", 10, "bold"), bd=0, cursor="hand2", padx=14, pady=7, relief="flat", **kwargs)

def log_audit_telemetry(module_name, result_summary):
    try:
        db_cursor.execute("INSERT INTO audit_logs (module, assessment_result) VALUES (?, ?)", (module_name, result_summary))
        db_connection.commit()
    except Exception:
        pass

# --- TAB 1: NETBLOCKER ---
netblocker_tab = tk.Frame(main_notebook, bg=BG_PANEL)
main_notebook.add(netblocker_tab, text="  🔒 NetBlocker  ")
tk.Label(netblocker_tab, text="🔒 System Domain Firewall Engine", font=FONT_HEADER, bg=BG_PANEL, fg=ACCENT_CRIMSON).pack(pady=(15, 2))

database_input_frame = tk.Frame(netblocker_tab, bg=BG_PANEL)
database_input_frame.pack(pady=10)
tk.Label(database_input_frame, text="Enter Domain Target:", font=FONT_BODY, bg=BG_PANEL, fg=FG_PRIMARY).grid(row=0, column=0, padx=5)
site_input_entry = create_styled_entry(database_input_frame, width=30)
site_input_entry.grid(row=0, column=1, padx=5, ipady=2)

def refresh_websites_listbox():
    blocked_listbox.delete(0, tk.END)
    db_cursor.execute("SELECT domain FROM blocked_domains")
    for database_row in db_cursor.fetchall():
        blocked_listbox.insert(tk.END, database_row[0])

def insert_new_domain():
    domain_text = site_input_entry.get().strip().lower()
    if domain_text and re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", domain_text):
        try:
            db_cursor.execute("INSERT INTO blocked_domains (domain) VALUES (?)", (domain_text,))
            db_connection.commit()
            site_input_entry.delete(0, tk.END)
            refresh_websites_listbox()
            log_audit_telemetry("NetBlocker Registry", f"Added target domain: {domain_text}")
        except sqlite3.IntegrityError:
            messagebox.showwarning("Registry Error", "Domain already exists.")
    else:
            messagebox.showerror("Validation Error", "Invalid domain structure format.")

def remove_selected_domain():
    try:
        selected_target_domain = blocked_listbox.get(blocked_listbox.curselection())
        db_cursor.execute("DELETE FROM blocked_domains WHERE domain = ?", (selected_target_domain,))
        db_connection.commit()
        refresh_websites_listbox()
    except Exception:
        messagebox.showwarning("Selection Error", "No domain selected.")

create_styled_button(database_input_frame, text="Add To Database", command=insert_new_domain, color=ACCENT_CYAN, fg_color=BG_DARK).grid(row=0, column=2, padx=5)

listbox_viewport_frame = tk.Frame(netblocker_tab, bg=BG_DARK, bd=1, relief="solid")
listbox_viewport_frame.pack(pady=10, padx=40, fill="both", expand=True)
blocked_listbox = tk.Listbox(listbox_viewport_frame, font=FONT_TERMINAL, width=50, height=6, bg=BG_PANEL, fg=ACCENT_CRIMSON, selectbackground=ACCENT_CRIMSON, bd=0)
blocked_listbox.pack(pady=5)
create_styled_button(netblocker_tab, text="Remove Selected Domain", command=remove_selected_domain, color=ACCENT_CRIMSON).pack(pady=5)
refresh_websites_listbox()

# --- TAB 2: EMAIL ANALYZER ---
email_tab = tk.Frame(main_notebook, bg=BG_PANEL)
main_notebook.add(email_tab, text="  📧 Email Analyzer  ")
tk.Label(email_tab, text="📧 Structured Vector Domain Analyzer", font=FONT_HEADER, bg=BG_PANEL, fg=ACCENT_CYAN).pack(pady=(15, 2))
input_row_em = tk.Frame(email_tab, bg=BG_PANEL)
input_row_em.pack(pady=15)
tk.Label(input_row_em, text="Target Handle String: ", font=FONT_BODY, bg=BG_PANEL, fg=FG_PRIMARY).grid(row=0, column=0, padx=5)
email_input_entry = create_styled_entry(input_row_em, width=40)
email_input_entry.grid(row=0, column=1, padx=5, ipady=3)
email_report_display = tk.Text(email_tab, height=12, width=75, font=FONT_TERMINAL, bg=BG_DARK, fg=ACCENT_GREEN, bd=1, relief="solid")
email_report_display.pack(pady=10, padx=40, fill="both", expand=True)

def analyze_email_address_string():
    target_email_string = email_input_entry.get().strip()
    email_report_display.delete("1.0", tk.END)
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', target_email_string):
        email_report_display.insert(tk.END, f"Valid Email Structure Detected: {target_email_string}\n")
    else:
        email_report_display.insert(tk.END, "❌ INVALID EMAIL SYNTAX FORMAT")

create_styled_button(email_tab, text="⚡ INITIALIZE AUDIT", command=analyze_email_address_string, color=ACCENT_CYAN, fg_color=BG_DARK).pack(pady=10)

# --- APP RUN ---
def graceful_shutdown():
    try:
        db_connection.close()
    except Exception:
        pass
    root_window.destroy()

root_window.protocol("WM_DELETE_WINDOW", graceful_shutdown)
root_window.mainloop()
