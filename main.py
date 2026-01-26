import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import shutil
import os
import json
import webbrowser

# ==========================================================
# KONFIGURACJA ŚCIEŻEK I USTAWIEŃ polsoft.ITS™
# ==========================================
APP_DIR = os.path.expandvars(r"%userprofile%\.polsoft\WinGet")
DOWNLOAD_DIR = os.path.expandvars(r"%userprofile%\Downloads\WinGet")
SETTINGS_FILE = os.path.join(APP_DIR, "settings.json")

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"lang": "pl", "theme": "dark"}

def save_settings(settings):
    try:
        os.makedirs(APP_DIR, exist_ok=True)
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
    except:
        pass

# ==========================================================
# LOKALIZACJA
# ==========================================================
TEXTS = {
    "pl": {
        "title": "polsoft.ITS™ London – WinGet Deployer",
        "label_pkg": "ID:",
        "btn_search": "Szukaj",
        "btn_install": "Instaluj",
        "btn_upgrade": "Upgr.",
        "btn_upgrade_all": "Upgr. All",
        "btn_uninstall": "Usuń",
        "btn_installed": "Lista",
        "btn_available": "Dostępne",
        "btn_about": "O nas",
        "btn_info": "iNfO",
        "btn_repair": "Napraw / Instaluj WinGet",
        "group_manage": "Zarządzanie Pakietami",
        "msg_empty": "Pole puste",
        "msg_empty_txt": "Wpisz ID pakietu",
        "msg_no_winget": "Brak WinGet",
        "msg_no_winget_txt": "Zainstaluj WinGet najpierw.",
        "searching": ">>> Szukanie: ",
        "installing": ">>> Instalacja: ",
        "upgrading": ">>> Aktualizacja: ",
        "upgrading_all": ">>> Aktualizacja wszystkich...\n",
        "uninstalling": ">>> Usuwanie: ",
        "showing_list": ">>> Lista zainstalowanych...\n",
        "showing_available": ">>> Sprawdzanie aktualizacji...\n",
        "repairing": ">>> Pobieranie i naprawa...",
        "fetching_info": ">>> Pobieranie informacji o systemie WinGet...\n",
        "lang_toggle": "EN"
    },
    "en": {
        "title": "polsoft.ITS™ London – WinGet Deployer",
        "label_pkg": "ID:",
        "btn_search": "Search",
        "btn_install": "Install",
        "btn_upgrade": "Upgrade",
        "btn_upgrade_all": "Upgr. All",
        "btn_uninstall": "Remove",
        "btn_installed": "List",
        "btn_available": "Available",
        "btn_about": "About",
        "btn_info": "iNfO",
        "btn_repair": "Repair / Install WinGet",
        "group_manage": "Package Management",
        "msg_empty": "Field empty",
        "msg_empty_txt": "Please enter Package ID",
        "msg_no_winget": "WinGet Missing",
        "msg_no_winget_txt": "Please install WinGet first.",
        "searching": ">>> Searching: ",
        "installing": ">>> Installing: ",
        "upgrading": ">>> Upgrading: ",
        "upgrading_all": ">>> Upgrading all packages...\n",
        "uninstalling": ">>> Uninstalling: ",
        "showing_list": ">>> Fetching list...\n",
        "showing_available": ">>> Checking for upgrades...\n",
        "repairing": ">>> Downloading and repairing...",
        "fetching_info": ">>> Fetching WinGet system info...\n",
        "lang_toggle": "PL"
    }
}

COMMON_IDS = [
    "Google.Chrome", "Mozilla.Firefox", "Microsoft.Edge", "Microsoft.VisualStudioCode",
    "Git.Git", "7zip.7zip", "VideoLAN.VLC", "WinRAR.WinRAR", "Notepad++.Notepad++",
    "Docker.DockerDesktop", "Discord.Discord", "Spotify.Spotify", "Zoom.Zoom",
    "AnyDesk.AnyDesk", "TeamViewer.TeamViewer", "GIMP.GIMP", "Inkscape.Inkscape"
]

class WingetApp:
    def __init__(self, root):
        self.root = root
        self.settings = load_settings()
        self.lang = self.settings.get("lang", "pl")
        self.theme = self.settings.get("theme", "dark")
        self.style = ttk.Style()
        
        self.setup_ui()
        self.apply_theme()
        self.update_ui_text()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.settings["lang"] = self.lang
        self.settings["theme"] = self.theme
        save_settings(self.settings)
        self.root.destroy()

    def setup_ui(self):
        self.root.geometry("1000x680") 
        self.root.minsize(900, 550)

        self.group_manage = ttk.LabelFrame(self.root, padding=8)
        self.group_manage.pack(fill="x", padx=10, pady=5)

        self.lbl_pkg = ttk.Label(self.group_manage)
        self.lbl_pkg.grid(row=0, column=0, padx=2)

        self.entry_frame = tk.Frame(self.group_manage)
        self.entry_frame.grid(row=0, column=1, padx=5, sticky="w")

        self.main_entry = tk.Entry(self.entry_frame, width=16, font=("Arial", 10), borderwidth=0)
        self.main_entry.pack(ipady=3)
        
        self.suggestion_list = tk.Listbox(self.root, height=5, font=("Arial", 9), borderwidth=0, highlightthickness=1)
        self.suggestion_list.place_forget()

        self.main_entry.bind("<KeyRelease>", self.on_key_release)
        self.main_entry.bind("<FocusOut>", lambda e: self.root.after(200, self.suggestion_list.place_forget))
        self.suggestion_list.bind("<<ListboxSelect>>", self.on_suggestion_select)
        self.main_entry.bind("<Down>", lambda e: self.suggestion_list.focus_set())
        self.suggestion_list.bind("<Return>", self.on_suggestion_select)

        # PRZYCISKI
        self.btn_search = ttk.Button(self.group_manage, width=7, command=self.run_search)
        self.btn_search.grid(row=0, column=2, padx=1)

        self.btn_inst = ttk.Button(self.group_manage, width=8, command=self.run_install)
        self.btn_inst.grid(row=0, column=3, padx=1)

        self.btn_uninst = ttk.Button(self.group_manage, width=7, command=self.run_uninstall)
        self.btn_uninst.grid(row=0, column=4, padx=1)

        ttk.Separator(self.group_manage, orient="vertical").grid(row=0, column=5, padx=6, sticky="ns")

        self.btn_upgr = ttk.Button(self.group_manage, width=7, command=self.run_upgrade)
        self.btn_upgr.grid(row=0, column=6, padx=1)

        self.btn_upgr_all = ttk.Button(self.group_manage, width=9, command=self.run_upgrade_all)
        self.btn_upgr_all.grid(row=0, column=7, padx=1)

        self.btn_avail = ttk.Button(self.group_manage, width=9, command=self.run_available)
        self.btn_avail.grid(row=0, column=8, padx=1)

        ttk.Separator(self.group_manage, orient="vertical").grid(row=0, column=9, padx=6, sticky="ns")

        self.btn_list = ttk.Button(self.group_manage, width=7, command=self.run_list)
        self.btn_list.grid(row=0, column=10, padx=1)

        ttk.Separator(self.group_manage, orient="vertical").grid(row=0, column=11, padx=6, sticky="ns")

        # Sekcja końcowa: Język, iNfO, About, Theme
        self.btn_lang = ttk.Button(self.group_manage, width=4, command=self.toggle_lang)
        self.btn_lang.grid(row=0, column=12, padx=1)

        # Nowy przycisk iNfO
        self.btn_info = ttk.Button(self.group_manage, width=6, command=self.run_info)
        self.btn_info.grid(row=0, column=13, padx=1)

        self.btn_about = ttk.Button(self.group_manage, width=7, command=self.show_about)
        self.btn_about.grid(row=0, column=14, padx=1)

        self.btn_theme = ttk.Button(self.group_manage, width=3, command=self.toggle_theme)
        self.btn_theme.grid(row=0, column=15, padx=1)

        self.main_entry.bind("<Return>", lambda e: self.run_search())

        # KONSOLA
        log_frame = ttk.Frame(self.root)
        log_frame.pack(expand=True, fill="both", padx=10, pady=5)
        self.log_box = tk.Text(log_frame, font=("Consolas", 10), borderwidth=0, padx=10, pady=10)
        self.log_box.pack(side="left", expand=True, fill="both")
        self.log_box.tag_config("highlight", foreground="#40ff40", font=("Consolas", 10, "bold"))
        self.log_box.bind("<Button-3>", self.on_right_click)
        
        sb = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_box.yview)
        sb.pack(side="right", fill="y")
        self.log_box.configure(yscrollcommand=sb.set)

        self.btn_repair = ttk.Button(self.root, command=self.run_repair)
        self.btn_repair.pack(pady=5)

        self.footer = ttk.Label(self.root, text="WinGet (GUI) v1.5 ©2026 polsoft.ITS™ London", font=("Arial", 7))
        self.footer.pack(side="bottom", pady=2)

    def on_key_release(self, event):
        if event.keysym in ("Up", "Down", "Return"): return
        val = self.main_entry.get().strip().lower()
        if not val:
            self.suggestion_list.place_forget()
            return
        matches = [s for s in COMMON_IDS if val in s.lower()]
        if matches:
            self.suggestion_list.delete(0, tk.END)
            for m in matches: self.suggestion_list.insert(tk.END, m)
            x = self.main_entry.winfo_rootx() - self.root.winfo_rootx()
            y = (self.main_entry.winfo_rooty() - self.root.winfo_rooty()) + self.main_entry.winfo_height()
            self.suggestion_list.place(x=x, y=y, width=self.main_entry.winfo_width())
            self.suggestion_list.lift()
        else:
            self.suggestion_list.place_forget()

    def on_suggestion_select(self, event=None):
        try:
            sel = self.suggestion_list.get(self.suggestion_list.curselection())
            self.main_entry.delete(0, tk.END); self.main_entry.insert(0, sel)
            self.suggestion_list.place_forget(); self.main_entry.focus_set()
        except: pass

    def apply_theme(self):
        if self.theme == "dark":
            m_bg, c_bg, b_bg, f_fg, out_bg = "#121212", "#1e1e1e", "#333333", "#ffffff", "#0a0a0a"
            self.root.configure(bg=m_bg)
            self.style.theme_use('clam')
            self.style.configure("TLabelframe", background=m_bg, foreground=f_fg)
            self.style.configure("TLabelframe.Label", background=m_bg, foreground=f_fg)
            self.style.configure("TLabel", background=m_bg, foreground=f_fg)
            self.style.configure("TButton", background=b_bg, foreground=f_fg)
            self.style.map("TButton", background=[('active', '#444444')])
            self.log_box.configure(bg=out_bg, fg=f_fg, insertbackground="white")
            self.main_entry.configure(bg=c_bg, fg=f_fg, insertbackground="white")
            self.suggestion_list.configure(bg=c_bg, fg=f_fg, highlightbackground=b_bg)
            self.btn_theme.config(text="☀️"); self.entry_frame.config(bg=m_bg)
        else:
            self.root.configure(bg="#f0f0f0")
            self.style.theme_use('default')
            self.log_box.configure(bg="white", fg="black", insertbackground="black")
            self.main_entry.configure(bg="white", fg="black", insertbackground="black")
            self.suggestion_list.configure(bg="white", fg="black", highlightbackground="gray")
            self.btn_theme.config(text="🌙"); self.entry_frame.config(bg="#f0f0f0")

    def update_ui_text(self):
        t = TEXTS[self.lang]
        self.root.title(t["title"])
        self.group_manage.config(text=t["group_manage"])
        self.lbl_pkg.config(text=t["label_pkg"])
        self.btn_search.config(text=t["btn_search"])
        self.btn_inst.config(text=t["btn_install"])
        self.btn_uninst.config(text=t["btn_uninstall"])
        self.btn_upgr.config(text=t["btn_upgrade"])
        self.btn_upgr_all.config(text=t["btn_upgrade_all"])
        self.btn_avail.config(text=t["btn_available"])
        self.btn_list.config(text=t["btn_installed"])
        self.btn_about.config(text=t["btn_about"])
        self.btn_info.config(text=t["btn_info"])
        self.btn_repair.config(text=t["btn_repair"])
        self.btn_lang.config(text=t["lang_toggle"])

    def toggle_lang(self):
        self.lang = "en" if self.lang == "pl" else "pl"
        self.update_ui_text()

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.apply_theme()

    def show_about(self):
        about_win = tk.Toplevel(self.root)
        about_win.title("About polsoft.ITS™")
        about_win.geometry("450x320")
        about_win.resizable(False, False)
        about_win.transient(self.root)
        about_win.grab_set()

        is_dark = self.theme == "dark"
        bg_main = "#121212" if is_dark else "#ffffff"
        bg_header = "#1e1e1e" if is_dark else "#f0f0f0"
        fg_main = "#ffffff" if is_dark else "#000000"
        fg_sub = "#aaaaaa" if is_dark else "#555555"
        accent = "#40ff40" if is_dark else "#0078d7"

        about_win.configure(bg=bg_main)

        header = tk.Frame(about_win, bg=bg_header, height=80)
        header.pack(fill="x"); header.pack_propagate(False)
        tk.Label(header, text="polsoft.ITS™ London", font=("Segoe UI", 16, "bold"), bg=bg_header, fg=accent).pack(pady=(15, 0))
        tk.Label(header, text="WinGet Deployer Engine v1.5", font=("Segoe UI", 9), bg=bg_header, fg=fg_sub).pack()

        content = tk.Frame(about_win, bg=bg_main, padx=30, pady=20)
        content.pack(expand=True, fill="both")

        tk.Label(content, text="Lead Developer:", font=("Segoe UI", 9, "bold"), bg=bg_main, fg=fg_main).pack(anchor="w")
        tk.Label(content, text="Sebastian Januchowski", font=("Segoe UI", 11), bg=bg_main, fg=fg_main).pack(anchor="w", pady=(0, 10))
        tk.Label(content, text="Contact:", font=("Segoe UI", 9, "bold"), bg=bg_main, fg=fg_main).pack(anchor="w")
        tk.Label(content, text="polsoft.its@fastservice.com", font=("Segoe UI", 10), bg=bg_main, fg=fg_main).pack(anchor="w", pady=(0, 10))

        link = tk.Label(content, text="View Project on GitHub", font=("Segoe UI", 10, "underline"), bg=bg_main, fg=accent, cursor="hand2")
        link.pack(anchor="w", pady=(5, 0))
        link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/seb07uk"))

        footer = tk.Frame(about_win, bg=bg_main, pady=10)
        footer.pack(side="bottom", fill="x")
        tk.Label(footer, text="© 2026 polsoft.ITS™ All Rights Reserved", font=("Segoe UI", 8), bg=bg_main, fg=fg_sub).pack()
        ttk.Button(footer, text="Close", width=15, command=about_win.destroy).pack(pady=10)

    def on_right_click(self, event):
        try:
            sel = self.log_box.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
            if sel: self.main_entry.delete(0, tk.END); self.main_entry.insert(0, sel)
        except: pass

    def get_winget(self):
        s = shutil.which("winget")
        if s: return s
        l = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\winget.exe")
        return l if os.path.exists(l) else None

    def execute(self, cmd, btn=None, highlight=None):
        if btn: btn.config(state="disabled")
        def run():
            try:
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
                for line in p.stdout:
                    self.log_box.insert(tk.END, line); self.log_box.see(tk.END)
                p.wait()
                if highlight: self.apply_highlight(highlight)
            except Exception as e:
                self.log_box.insert(tk.END, f"\nError: {e}\n")
            finally:
                if btn: btn.config(state="normal")
        threading.Thread(target=run, daemon=True).start()

    def apply_highlight(self, term):
        self.log_box.tag_remove("highlight", "1.0", tk.END)
        start = "1.0"
        while True:
            start = self.log_box.search(term, start, stopindex=tk.END, nocase=True)
            if not start: break
            end = f"{start}+{len(term)}c"; self.log_box.tag_add("highlight", start, end); start = end

    # --- FUNKCJE WYKONAWCZE ---

    def run_info(self):
        t = TEXTS[self.lang]
        w = self.get_winget()
        if not w: return
        self.log_box.delete(1.0, tk.END)
        self.log_box.insert(tk.END, t["fetching_info"])
        self.execute([w, "--info"], btn=self.btn_info)

    def run_search(self):
        t = TEXTS[self.lang]; q = self.main_entry.get().strip()
        if not q: return
        w = self.get_winget()
        if not w: messagebox.showerror(t["msg_no_winget"], t["msg_no_winget_txt"]); return
        self.log_box.delete(1.0, tk.END); self.log_box.insert(tk.END, f"{t['searching']}{q}...\n")
        self.execute([w, "search", q], highlight=q)

    def run_list(self):
        t = TEXTS[self.lang]; w = self.get_winget()
        if not w: return
        self.log_box.delete(1.0, tk.END); self.log_box.insert(tk.END, t["showing_list"])
        self.execute([w, "list"], btn=self.btn_list)

    def run_available(self):
        t = TEXTS[self.lang]; w = self.get_winget()
        if not w: return
        self.log_box.delete(1.0, tk.END); self.log_box.insert(tk.END, t["showing_available"])
        self.execute([w, "list", "--upgrade-available"], btn=self.btn_avail)

    def run_install(self):
        t = TEXTS[self.lang]; i = self.main_entry.get().strip()
        if not i: messagebox.showwarning(t["msg_empty"], t["msg_empty_txt"]); return
        w = self.get_winget()
        if not w: return
        self.log_box.insert(tk.END, f"\n{t['installing']}{i}\n")
        self.execute([w, "install", "--id", i, "-e", "--silent", "--accept-source-agreements", "--accept-package-agreements"], btn=self.btn_inst)

    def run_upgrade(self):
        t = TEXTS[self.lang]; i = self.main_entry.get().strip()
        if not i: messagebox.showwarning(t["msg_empty"], t["msg_empty_txt"]); return
        w = self.get_winget()
        if not w: return
        self.log_box.insert(tk.END, f"\n{t['upgrading']}{i}\n")
        self.execute([w, "upgrade", "--id", i, "--silent", "--accept-source-agreements"], btn=self.btn_upgr)

    def run_upgrade_all(self):
        t = TEXTS[self.lang]; w = self.get_winget()
        if not w: return
        self.log_box.insert(tk.END, f"\n{t['upgrading_all']}")
        self.execute([w, "upgrade", "--all", "--silent", "--accept-source-agreements"], btn=self.btn_upgr_all)

    def run_uninstall(self):
        t = TEXTS[self.lang]; i = self.main_entry.get().strip()
        if not i: messagebox.showwarning(t["msg_empty"], t["msg_empty_txt"]); return
        w = self.get_winget()
        if not w: return
        self.log_box.insert(tk.END, f"\n{t['uninstalling']}{i}\n")
        self.execute([w, "uninstall", "--id", i, "--silent"], btn=self.btn_uninst)

    def run_repair(self):
        t = TEXTS[self.lang]
        self.log_box.delete(1.0, tk.END); self.log_box.insert(tk.END, f"{t['repairing']}\n")
        if not os.path.exists(DOWNLOAD_DIR): os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        m = os.path.join(DOWNLOAD_DIR, "winget_installer.msixbundle")
        ps = (f"$progressPreference = 'silentlyContinue'; "
              f"$latest = Invoke-RestMethod -Uri 'https://api.github.com/repos/microsoft/winget-cli/releases/latest'; "
              f"$url = ($latest.assets | Where-Object Name -match 'msixbundle$').browser_download_url; "
              f"Invoke-WebRequest -Uri $url -OutFile '{m}'; Add-AppxPackage -Path '{m}'")
        self.execute(["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps])

if __name__ == "__main__":
    root = tk.Tk(); app = WingetApp(root); root.mainloop()