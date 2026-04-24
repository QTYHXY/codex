#!/usr/bin/env python3
"""Desktop UI for SW1/SW2 parser (ISO/IEC 7816)."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from sw1sw2_parser import normalize, parse_status


class SwUi(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("SW1/SW2 Parser · ISO/IEC 7816")
        self.geometry("760x520")
        self.minsize(680, 460)

        self.configure(bg="#0b1220")
        self._setup_style()
        self._build_widgets()

    def _setup_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Card.TFrame", background="#111827")
        style.configure("Title.TLabel", background="#111827", foreground="#f9fafb", font=("Segoe UI", 18, "bold"))
        style.configure("Sub.TLabel", background="#111827", foreground="#9ca3af", font=("Segoe UI", 10))
        style.configure("Field.TLabel", background="#111827", foreground="#d1d5db", font=("Segoe UI", 11, "bold"))
        style.configure("ResultTitle.TLabel", background="#111827", foreground="#93c5fd", font=("Segoe UI", 11, "bold"))
        style.configure("Accent.TButton", background="#2563eb", foreground="#ffffff", font=("Segoe UI", 11, "bold"), borderwidth=0)
        style.map("Accent.TButton", background=[("active", "#1d4ed8")])

    def _build_widgets(self) -> None:
        outer = ttk.Frame(self, style="Card.TFrame", padding=24)
        outer.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)

        ttk.Label(outer, text="SW1/SW2 快速解析", style="Title.TLabel").pack(anchor="w")
        ttk.Label(outer, text="输入 SW1SW2（如 9000 / 6A82 / 63 C3 / 0x6A 0x82），按 Enter 或点击解析。", style="Sub.TLabel").pack(anchor="w", pady=(4, 20))

        ttk.Label(outer, text="SW1SW2", style="Field.TLabel").pack(anchor="w")
        self.input_var = tk.StringVar()
        entry = ttk.Entry(outer, textvariable=self.input_var, font=("Consolas", 14))
        entry.pack(fill=tk.X, pady=(6, 12))
        entry.focus_set()
        entry.bind("<Return>", lambda _e: self._decode())

        button_row = ttk.Frame(outer, style="Card.TFrame")
        button_row.pack(fill=tk.X, pady=(0, 18))

        ttk.Button(button_row, text="解析", style="Accent.TButton", command=self._decode).pack(side=tk.LEFT)
        ttk.Button(button_row, text="清空", command=self._clear).pack(side=tk.LEFT, padx=(10, 0))

        result_frame = ttk.Frame(outer, style="Card.TFrame")
        result_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(result_frame, text="结果", style="ResultTitle.TLabel").pack(anchor="w")

        self.result = tk.Text(
            result_frame,
            height=14,
            bg="#0f172a",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
            relief=tk.FLAT,
            padx=12,
            pady=12,
            font=("Consolas", 12),
            wrap=tk.WORD,
        )
        self.result.pack(fill=tk.BOTH, expand=True, pady=(8, 0))
        self.result.insert(
            tk.END,
            "等待输入…\n\n示例：\n- 9000\n- 6A82\n- 63 C2\n- 0x6A 0x82",
        )
        self.result.configure(state=tk.DISABLED)

    def _set_result(self, text: str) -> None:
        self.result.configure(state=tk.NORMAL)
        self.result.delete("1.0", tk.END)
        self.result.insert(tk.END, text)
        self.result.configure(state=tk.DISABLED)

    def _decode(self) -> None:
        raw = self.input_var.get().strip()
        if not raw:
            self._set_result("请输入 SW1SW2。")
            return

        try:
            sw = normalize(raw)
            meaning = parse_status(sw)
        except ValueError as exc:
            self._set_result(f"输入错误：{exc}")
            return

        output = (
            f"SW1SW2: {sw}\n"
            f"Category: {meaning.category}\n"
            f"Meaning: {meaning.description}\n"
        )
        self._set_result(output)

    def _clear(self) -> None:
        self.input_var.set("")
        self._set_result("已清空。")


def main() -> None:
    app = SwUi()
    app.mainloop()


if __name__ == "__main__":
    main()
