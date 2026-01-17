# -*- coding: utf-8 -*-
"""
Ortak UI yardımcı fonksiyonları.
"""
import customtkinter as ctk


def create_progress_section(parent, pad_x=20, pad_y=(0, 20)):
    """Progress bar ve button frame bölümlerini oluşturur ve return eder."""
    progress_frame = ctk.CTkFrame(parent, fg_color="transparent")
    progress_frame.pack(fill="x", padx=pad_x, pady=pad_y)

    progress_label = ctk.CTkLabel(progress_frame, text="")
    progress_label.pack()

    progress_bar = ctk.CTkProgressBar(progress_frame, width=400)
    progress_bar.pack(pady=(10, 0))
    progress_bar.set(0)

    buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
    buttons_frame.pack(fill="x", padx=pad_x, pady=pad_y)

    return progress_label, progress_bar, buttons_frame


class CTkToolTip:
    """Widget üzerinde hover yapıldığında tooltip gösterir."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        try:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
            self.tip_window = tw = ctk.CTkToplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")

            # Tooltip içeriği
            label = ctk.CTkLabel(tw, text=self.text, corner_radius=6,
                               fg_color="#333333", text_color="#ffffff",
                               font=ctk.CTkFont(size=11))
            label.pack(padx=8, pady=4)
            # Pencereyi en öne getir
            tw.lift()
        except Exception:
            pass

    def hide_tip(self, event=None):
        if self.tip_window:
            try:
                self.tip_window.destroy()
            except Exception:
                pass
            self.tip_window = None
