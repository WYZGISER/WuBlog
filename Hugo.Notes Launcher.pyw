"""
Lincy.Notes 启动器 - 双击运行
需要 Python 3.10+（系统已自带）
"""

import subprocess
import threading
import webbrowser
import tkinter as tk
from tkinter import scrolledtext, messagebox
from pathlib import Path
import os
import sys
import time

# ============ 配置 ============
SCRIPT_DIR = Path(__file__).parent.resolve()
HUGO_EXE   = SCRIPT_DIR / "hugo.exe"
PORT       = 1314
URL        = f"http://127.0.0.1:{PORT}"
# 线上部署在 /WuBlog/ 子目录，本地预览用根路径，否则访问 / 会 404
BASE_URL   = f"http://127.0.0.1:{PORT}/"

# 品牌色
BRAND_500  = "#FF6E40"
BRAND_600  = "#EA580C"
BRAND_50   = "#FFF4ED"
INK_900    = "#0F172A"
INK_700    = "#334155"
INK_500    = "#64748B"
INK_300    = "#CBD5E1"
INK_100    = "#F1F5F9"
BG         = "#FAFAF9"
SUCCESS    = "#10B981"
ERROR      = "#EF4444"


class HugoLauncher:
    def __init__(self, root):
        self.root  = root
        self.proc  = None  # subprocess.Popen
        self.alive = False

        root.title("Lincy.Notes 启动器")
        root.geometry("520x460")
        root.resizable(False, False)
        root.configure(bg=BG)

        # 字体
        try:
            self.font_title = ("Segoe UI", 16, "bold")
            self.font_body  = ("Segoe UI", 10)
            self.font_mono  = ("Consolas", 9)
        except Exception:
            self.font_title = ("Arial", 16, "bold")
            self.font_body  = ("Arial", 10)
            self.font_mono  = ("Courier", 9)

        self._build_ui()
        self._poll_status()

    # ---------- UI 构建 ----------
    def _build_ui(self):
        # Header（品牌色块）
        header = tk.Frame(self.root, bg=BRAND_500, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="L", font=("Georgia", 28, "bold"),
            fg="white", bg=BRAND_500
        ).pack(side="left", padx=(20, 8), pady=12)

        tk.Label(
            header, text="Lincy.Notes", font=self.font_title,
            fg="white", bg=BRAND_500
        ).pack(side="left", pady=18)

        tk.Label(
            header, text="启动器", font=self.font_body,
            fg="white", bg=BRAND_500
        ).pack(side="left", padx=(4, 0), pady=22)

        # 主体
        body = tk.Frame(self.root, bg=BG, padx=24, pady=20)
        body.pack(fill="both", expand=True)

        # 状态行
        status_row = tk.Frame(body, bg=BG)
        status_row.pack(fill="x", pady=(0, 12))

        self.status_dot = tk.Label(
            status_row, text="●", font=("Arial", 14),
            fg=INK_300, bg=BG
        )
        self.status_dot.pack(side="left")

        self.status_text = tk.Label(
            status_row, text="服务器未运行", font=self.font_body,
            fg=INK_500, bg=BG
        )
        self.status_text.pack(side="left", padx=(6, 0))

        # URL 显示
        url_row = tk.Frame(body, bg=INK_100, padx=12, pady=10)
        url_row.pack(fill="x", pady=(0, 16))

        tk.Label(
            url_row, text="访问地址", font=self.font_body,
            fg=INK_500, bg=INK_100
        ).pack(anchor="w")

        tk.Label(
            url_row, text=URL, font=self.font_mono,
            fg=INK_900, bg=INK_100
        ).pack(anchor="w", pady=(2, 0))

        # 按钮区
        btn_row = tk.Frame(body, bg=BG)
        btn_row.pack(fill="x", pady=(0, 12))

        self.btn_start = self._make_button(
            btn_row, "启动服务器", BRAND_500, "white", self._start_server
        )
        self.btn_start.pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.btn_stop = self._make_button(
            btn_row, "停止", INK_300, INK_700, self._stop_server, disabled=True
        )
        self.btn_stop.pack(side="left", padx=(6, 6))

        self.btn_browser = self._make_button(
            btn_row, "打开浏览器", "white", INK_700, self._open_browser,
            border=True, disabled=True
        )
        self.btn_browser.pack(side="left", expand=True, fill="x", padx=(6, 0))

        # 日志区
        tk.Label(
            body, text="实时日志", font=self.font_body,
            fg=INK_500, bg=BG
        ).pack(anchor="w", pady=(0, 6))

        self.log = scrolledtext.ScrolledText(
            body, height=8, font=self.font_mono,
            bg="#0B1120", fg="#F8FAFC",
            insertbackground="white",
            relief="flat", padx=10, pady=8
        )
        self.log.pack(fill="both", expand=True)
        self.log.insert("end", "[就绪] 双击「启动服务器」开始预览...\n")
        self.log.config(state="disabled")

    def _make_button(self, parent, text, bg, fg, command,
                     border=False, disabled=False):
        btn = tk.Button(
            parent, text=text, font=self.font_body,
            bg=bg, fg=fg,
            activebackground=BRAND_600 if bg == BRAND_500 else bg,
            activeforeground=fg,
            relief="flat" if not border else "solid",
            borderwidth=1 if border else 0,
            padx=14, pady=8, cursor="hand2",
            command=command, state="disabled" if disabled else "normal",
            disabledforeground=INK_300
        )
        return btn

    # ---------- 状态轮询 ----------
    def _poll_status(self):
        if self.proc:
            alive = self.proc.poll() is None
            if alive != self.alive:
                self.alive = alive
                self._refresh_ui()
        self.root.after(500, self._poll_status)

    def _refresh_ui(self):
        if self.alive:
            self.status_dot.config(fg=SUCCESS)
            self.status_text.config(text="服务器运行中", fg=INK_900)
            self.btn_start.config(state="disabled", bg=INK_300)
            self.btn_stop.config(state="normal", bg=ERROR, fg="white",
                                 activebackground="#DC2626")
            self.btn_browser.config(state="normal")
        else:
            self.status_dot.config(fg=INK_300)
            self.status_text.config(text="服务器未运行", fg=INK_500)
            self.btn_start.config(state="normal", bg=BRAND_500, fg="white")
            self.btn_stop.config(state="disabled", bg=INK_300, fg=INK_300)
            self.btn_browser.config(state="disabled")

    # ---------- 操作 ----------
    def _log(self, msg):
        self.log.config(state="normal")
        ts = time.strftime("%H:%M:%S")
        self.log.insert("end", f"[{ts}] {msg}\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def _start_server(self):
        if self.alive:
            return
        if not HUGO_EXE.exists():
            messagebox.showerror("错误", f"找不到 hugo.exe:\n{HUGO_EXE}")
            return

        self._log("正在启动 Hugo 服务器...")

        # 启动 hugo.exe server，捕获 stdout/stderr
        try:
            self.proc = subprocess.Popen(
                [str(HUGO_EXE), "server", "-D",
                 "--bind", "127.0.0.1", "--port", str(PORT),
                 "--baseURL", BASE_URL],
                cwd=str(SCRIPT_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW,
                text=True, bufsize=1
            )
        except Exception as e:
            self._log(f"启动失败: {e}")
            messagebox.showerror("启动失败", str(e))
            return

        self.alive = True
        self._refresh_ui()
        self._log(f"已启动 (PID={self.proc.pid})")
        self._log(f"访问: {URL}")

        # 异步读取输出
        threading.Thread(target=self._read_output, daemon=True).start()

        # 2 秒后自动打开浏览器
        self.root.after(2000, self._open_browser)

    def _stop_server(self):
        if not self.proc:
            return
        self._log("正在停止服务器...")
        try:
            self.proc.terminate()
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        except Exception as e:
            self._log(f"停止失败: {e}")
        finally:
            self.proc = None
            self.alive = False
            self._refresh_ui()
            self._log("服务器已停止")

    def _open_browser(self):
        if self.alive:
            webbrowser.open(URL)
            self._log(f"已打开浏览器: {URL}")

    def _read_output(self):
        if not self.proc:
            return
        try:
            for line in iter(self.proc.stdout.readline, ""):
                if not line:
                    break
                self.root.after(0, self._log, line.rstrip())
        except Exception:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = HugoLauncher(root)
    root.mainloop()
