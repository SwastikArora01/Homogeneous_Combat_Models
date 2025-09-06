from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import numpy as np
from PIL import Image, ImageTk
import os

# Constants
FONT_TITLE = ("Helvetica", 20, "bold")
FONT_SUBTITLE = ("Helvetica", 14, "bold")
FONT_NORMAL = ("Helvetica", 12)
BG_COLOR = "#f0f4f7"
BTN_COLOR = "#4a90e2"
BTN_TEXT_COLOR = "white"
DESC_COLOR = "#2e4a7d"  # Description text color


def Ancient_warfare():
    def show_full_image():
        top = Toplevel(Anc_warfare)
        top.title("Full Image - Ancient Warfare Model")
        full_img = Image.open(image_path)
        photo_full = ImageTk.PhotoImage(full_img)
        lbl = Label(top, image=photo_full, bg="white")
        lbl.image = photo_full
        lbl.pack()
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        img_width, img_height = full_img.size
        x = (screen_width // 2) - (img_width // 2)
        y = (screen_height // 2) - (img_height // 2)
        top.geometry(f"{img_width}x{img_height}+{x}+{y}")

    def anc_plot_graph(B0, R0, threshold_pct, k, parent_frame):
        R = R0
        B = B0
        t = 0
        dt = 0.1
        time, R_vals, B_vals = [], [], []

        R_thresh = R0 * (threshold_pct / 100)
        B_thresh = B0 * (threshold_pct / 100)

        for widget in parent_frame.winfo_children():
            widget.destroy()

        if threshold_pct == 100:
            Label(parent_frame, text="🚩 NO WAR TOOK PLACE", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="teal").pack(pady=(10, 5))
            return

        if threshold_pct == 0:
            R_thresh = 0
            B_thresh = 0

        while R > R_thresh and B > B_thresh:
            time.append(t)
            R_vals.append(R / R0)
            B_vals.append(B / B0)
            R -= (B * k / R0) * dt
            B -= (R / k / B0) * dt
            t += dt

        time.append(t)
        R_vals.append(R / R0)
        B_vals.append(B / B0)

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.plot(time, B_vals, label='B/B₀ (Friendly)', color='blue', linewidth=2)
        ax.plot(time, R_vals, label='R/R₀ (Enemy)', color='red', linewidth=2)
        ax.set_xlabel("Time")
        ax.set_ylabel("Normalized Strength")
        ax.set_title("Normalized Army Strength Over Time")
        ax.legend()
        ax.grid(True)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        result_text, color = "", "black"
        if abs(R - B) <= 1e-6:
            color = "#008080"
            result_text = "🤝 Equal Match: Both armies are equally worn"
        elif R > B:
            color = "red"
            result_text = "⚠️ Enemy Army (Red) Would Win!"
        else:
            color = "blue"
            result_text = "✅ Friendly Army (Blue) Would Win!"

        def fix_neg_zero(x):
            x = 0 if abs(x) < 1e-6 else round(x, 0)
            return int(x)

        Label(graph_holder,
              text=f"{result_text}\n📊 Friendly Remaining: {fix_neg_zero(B)}\n📊 Enemy Remaining: {fix_neg_zero(R)}",
              bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg=color, justify=LEFT).pack(pady=(10, 5))

    def anc_submit_button():
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) == 9:
                widget.grid_forget()

        try:
            B0_val = anc_B0_entry.get()
            R0_val = anc_R0_entry.get()
            threshold_val = anc_threshold_entry.get()
            k_val = anc_k_entry.get()

            if not (B0_val.isdigit() and R0_val.isdigit() and threshold_val.replace('.', '', 1).isdigit()):
                raise TypeError("IntegralError")

            B0 = int(B0_val)
            R0 = int(R0_val)
            threshold_pct = float(threshold_val)
            k = float(k_val)

            if B0 == 0 or R0 == 0:
                raise ZeroDivisionError("ZeroStrength")
            if B0 < 0 or R0 < 0 or k <= 0 or not (0 <= threshold_pct <= 100):
                raise ValueError("InvalidRange")

            anc_plot_graph(B0, R0, threshold_pct, k, graph_holder)

        except TypeError:
            for widget in graph_holder.winfo_children():
                widget.destroy()
            Label(left_frame, text="❌ Invalid Input (Positive Numeric values only)", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=9, column=0, columnspan=2)

        except ZeroDivisionError:
            for widget in graph_holder.winfo_children():
                widget.destroy()
            Label(left_frame, text="❌ Initial Strength can't be zero", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=9, column=0, columnspan=2)

        except ValueError:
            for widget in graph_holder.winfo_children():
                widget.destroy()
            Label(left_frame, text="❌ Invalid Range or Negative Values", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=9, column=0, columnspan=2)

    def set_blue_win():
        anc_B0_entry.delete(0, END)
        anc_B0_entry.insert(0, "160")
        anc_R0_entry.delete(0, END)
        anc_R0_entry.insert(0, "90")
        anc_threshold_entry.delete(0, END)
        anc_threshold_entry.insert(0, "60")
        anc_k_entry.delete(0, END)
        anc_k_entry.insert(0, "0.6")

    def set_red_win():
        anc_B0_entry.delete(0, END)
        anc_B0_entry.insert(0, "100")
        anc_R0_entry.delete(0, END)
        anc_R0_entry.insert(0, "180")
        anc_threshold_entry.delete(0, END)
        anc_threshold_entry.insert(0, "60")
        anc_k_entry.delete(0, END)
        anc_k_entry.insert(0, "0.8")

    Anc_warfare = Toplevel(bg=BG_COLOR)
    Anc_warfare.title("Ancient Warfare Calculator")

    window_width = 1300
    window_height = 777
    screen_width = Anc_warfare.winfo_screenwidth()
    screen_height = Anc_warfare.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    Anc_warfare.geometry(f"{window_width}x{window_height}+{x}+{y}")
    Anc_warfare.configure(bg=BG_COLOR)
    Anc_warfare.bind("<Escape>", lambda e: Anc_warfare.destroy())

    global left_frame, right_frame, graph_holder
    left_frame = Frame(Anc_warfare, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=30, pady=20, sticky=N)

    right_frame = Frame(Anc_warfare, bg=BG_COLOR)
    right_frame.grid(row=0, column=1, padx=10, pady=20, sticky=N)

    Label(left_frame, text="⚔️ Ancient Warfare Calculator", font=FONT_TITLE, bg=BG_COLOR, fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "AncientWarfare.png")
    img = Image.open(image_path)
    img = img.resize((480, 350), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    image_label = Label(left_frame, image=photo, bg=BG_COLOR)
    image_label.image = photo
    image_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))
    image_label.bind("<Button-1>", lambda e: show_full_image())
    image_label.config(cursor="hand2")

    Label(left_frame, text="⚠️ Recommended values are pre-filled below. You can change them as per your needs.",
          font=("Helvetica", 10, "bold"), fg="red", bg=BG_COLOR, justify=LEFT).grid(row=3, column=0, columnspan=2, sticky=W, pady=(0, 15))

    inputs = [
        ("Enter Initial Strength of Friendly Army (B₀):", 4, "160"),
        ("Enter Initial Strength of Enemy Army (R₀):", 5, "90"),
        ("Enter Threshold Percentage to End War:", 6, "60"),
        ("Enter Casualty Exchange Ratio (k):", 7, "0.6")
    ]
    entries = []

    for text, row, default in inputs:
        Label(left_frame, text=text, font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky=W, pady=5)
        entry = Entry(left_frame, width=30, font=FONT_NORMAL)
        entry.insert(0, default)
        entry.grid(row=row, column=1, pady=5, padx=5)
        entries.append(entry)

    anc_B0_entry, anc_R0_entry, anc_threshold_entry, anc_k_entry = entries

    Button(left_frame, text="Calculate", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_NORMAL,
           padx=20, pady=5, command=anc_submit_button).grid(row=8, column=0, columnspan=2, pady=20)

    Button(left_frame, text="Exit", bg="crimson", fg="white", font=FONT_NORMAL,
           command=Anc_warfare.destroy).grid(row=10, column=0, columnspan=2, pady=(10, 0))

    graph_holder = Frame(right_frame, bg=BG_COLOR)
    graph_holder.pack()

    Label(right_frame, text="🎯 Choose one of the recommended value sets from the buttons below:", bg=BG_COLOR,
          font=("Helvetica", 12, "bold"), fg="#333").pack(pady=(10, 5))

    button_holder = Frame(right_frame, bg=BG_COLOR)
    button_holder.pack(pady=10)

    Button(button_holder, text="🔵 Blue's Victory", bg="blue", fg="white",
           font=("Helvetica", 10, "bold"), command=set_blue_win, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="🔴 Red's Victory", bg="red", fg="white",
           font=("Helvetica", 10, "bold"), command=set_red_win, padx=10, pady=5).pack(side=LEFT, padx=8)

def Modern_warfare():
    def show_full_image():
        top = Toplevel(Mod_warfare)
        top.title("Full Image - Modern Warfare Model")
        full_img = Image.open(image_path)
        photo_full = ImageTk.PhotoImage(full_img)
        lbl = Label(top, image=photo_full, bg="white")
        lbl.image = photo_full
        lbl.pack()
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        img_width, img_height = full_img.size
        x = (screen_width // 2) - (img_width // 2)
        y = (screen_height // 2) - (img_height // 2)
        top.geometry(f"{img_width}x{img_height}+{x}+{y}")

    def mod_plot_graph(B0, R0, threshold_pct, beta, gamma):
        B = B0
        R = R0
        t, dt = 0, 0.01
        time, R_vals, B_vals = [], [], []

        B_thresh = B0 * (threshold_pct / 100)
        R_thresh = R0 * (threshold_pct / 100)

        # Clear graph area
        for widget in graph_holder.winfo_children():
            widget.destroy()

        # No war
        if threshold_pct == 100:
            Label(graph_holder, text="🚩 NO WAR TOOK PLACE", bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg="teal").pack(pady=(10, 5))
            return

        if threshold_pct == 0:
            B_thresh, R_thresh = 0, 0

        while B > B_thresh and R > R_thresh:
            time.append(t)
            B_vals.append(B / B0)
            R_vals.append(R / R0)

            dR = -gamma * (B ** 2) * dt
            dB = -beta * (R ** 2) * dt
            R += dR
            B += dB
            t += dt

        # Final point (clipped to threshold minimums)
        B = max(B, B_thresh)
        R = max(R, R_thresh)
        time.append(t)
        B_vals.append(B / B0)
        R_vals.append(R / R0)

        # Plot
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.plot(time, B_vals, label='B/B₀ (Friendly)', color='blue')
        ax.plot(time, R_vals, label='R/R₀ (Enemy)', color='red')
        ax.set_xlabel("Time")
        ax.set_ylabel("Normalized Strength")
        ax.set_title("Modern Warfare: Army Strength Over Time")
        ax.legend()
        ax.grid(True)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=graph_holder)
        canvas.draw()
        canvas.get_tk_widget().pack()


        # Format result
        def fix_neg_zero(x):
            x = round(x)
            return 0 if abs(x) < 1e-6 else int(x)

        final_B = fix_neg_zero(B)
        final_R = fix_neg_zero(R)

        def simulate_full_battle(B0, R0, beta, gamma):
            B, R = B0, R0
            t = 0
            dt = 0.01
            while B > 0 and R > 0:
                dR = -gamma * (B ** 2) * dt
                dB = -beta * (R ** 2) * dt
                R += dR
                B += dB
                t += dt
            return B, R  # Final strengths

        full_B, full_R = simulate_full_battle(B0, R0, beta, gamma)

        # Final clipped values
        final_B = fix_neg_zero(B)
        final_R = fix_neg_zero(R)

        full_B_final = fix_neg_zero(full_B)
        full_R_final = fix_neg_zero(full_R)

                # 🧠 Smarter Result Logic with Threshold Awareness
        if threshold_pct == 0:
            # No early cutoff — just declare real winner
            if abs(final_B - final_R) <= 1e-6:
                result_text = "🤝 Equal Match: Both armies are equally worn"
                color = "#008080"
            elif final_B > final_R:
                result_text = "✅ Friendly Army (Blue) Wins!"
                color = "blue"
            else:
                result_text = "⚠️ Enemy Army (Red) Wins!"
                color = "red"
        else:
            if abs(final_B - final_R) <= 1e-6:
                result_text = "🤝 Equal Match at early termination"
                color = "#008080"
            elif final_B > final_R:
                if full_B_final <= 0 and full_R_final > 0:
                    result_text = "⏸️ Blue has more troops now, but would have lost if the battle continued."
                    color = "teal"
                else:
                    result_text = "✅ Friendly Army (Blue) has the advantage at early stop"
                    color = "blue"
            else:
                if full_R_final <= 0 and full_B_final > 0:
                    result_text = "⏸️ Red has more troops now, but would have lost if the battle continued."
                    color = "teal"
                else:
                    result_text = "⚠️ Enemy Army (Red) has the advantage at early stop"
                    color = "red"

        Label(graph_holder,
            text=f"{result_text}\n📊 Friendly (Blue) Remaining: {final_B}\n📊 Enemy (Red) Remaining: {final_R}",
            bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg=color, justify=LEFT).pack(pady=(10, 5))


    def mod_submit_button():
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) == 9:
                widget.grid_forget()

        try:
            B0_val = mod_B0_entry.get()
            R0_val = mod_R0_entry.get()
            threshold_val = mod_threshold_entry.get()
            beta_val = mod_beta_entry.get()
            gamma_val = mod_gamma_entry.get()

            if not (B0_val.isdigit() and R0_val.isdigit() and threshold_val.replace('.', '', 1).isdigit()):
                raise TypeError("IntegralError")

            B0 = int(B0_val)
            R0 = int(R0_val)
            threshold_pct = float(threshold_val)
            beta = float(beta_val)
            gamma = float(gamma_val)

            if B0 == 0 or R0 == 0:
                raise ZeroDivisionError("ZeroStrength")
            if B0 < 0 or R0 < 0 or beta <= 0 or gamma <= 0 or not (0 <= threshold_pct <= 100):
                raise ValueError("InvalidRange")

            mod_plot_graph(B0, R0, threshold_pct, beta, gamma)

        except TypeError:
            for widget in graph_holder.winfo_children():
                widget.destroy()
            Label(left_frame, text="❌ Invalid Input (Positive Numeric values only)", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=9, column=0, columnspan=2)

        except ZeroDivisionError:
            for widget in graph_holder.winfo_children():
                widget.destroy()
            Label(left_frame, text="❌ Initial Strength can't be zero", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=9, column=0, columnspan=2)

        except ValueError:
            for widget in graph_holder.winfo_children():
                widget.destroy()
            Label(left_frame, text="❌ Invalid Range or Negative Values", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=9, column=0, columnspan=2)

    def set_blue_win():
        mod_B0_entry.delete(0, END)
        mod_B0_entry.insert(0, "160")
        mod_R0_entry.delete(0, END)
        mod_R0_entry.insert(0, "90")
        mod_threshold_entry.delete(0, END)
        mod_threshold_entry.insert(0, "60")
        mod_beta_entry.delete(0, END)
        mod_beta_entry.insert(0, "0.1")
        mod_gamma_entry.delete(0, END)
        mod_gamma_entry.insert(0, "0.4")

    def set_red_win():
        mod_B0_entry.delete(0, END)
        mod_B0_entry.insert(0, "100")
        mod_R0_entry.delete(0, END)
        mod_R0_entry.insert(0, "180")
        mod_threshold_entry.delete(0, END)
        mod_threshold_entry.insert(0, "60")
        mod_beta_entry.delete(0, END)
        mod_beta_entry.insert(0, "0.01")
        mod_gamma_entry.delete(0, END)
        mod_gamma_entry.insert(0, "0.005")

    def set_equal_match():
        mod_B0_entry.delete(0, END)
        mod_B0_entry.insert(0, "300")
        mod_R0_entry.delete(0, END)
        mod_R0_entry.insert(0, "200")
        mod_threshold_entry.delete(0, END)
        mod_threshold_entry.insert(0, "50")
        mod_beta_entry.delete(0, END)
        mod_beta_entry.insert(0, "0.1")
        mod_gamma_entry.delete(0, END)
        mod_gamma_entry.insert(0, "0.022")



    Mod_warfare = Toplevel(bg=BG_COLOR)
    Mod_warfare.title("Modern Warfare Calculator")

    window_width = 1250
    window_height = 810
    screen_width = Mod_warfare.winfo_screenwidth()
    screen_height = Mod_warfare.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    Mod_warfare.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    Mod_warfare.resizable(False, False)
    Mod_warfare.bind("<Escape>", lambda e: Mod_warfare.destroy())

    global left_frame, right_frame, graph_holder
    left_frame = Frame(Mod_warfare, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=30, pady=20, sticky=N)

    right_frame = Frame(Mod_warfare, bg=BG_COLOR)
    right_frame.grid(row=0, column=1, padx=10, pady=20, sticky=N)

    Label(left_frame, text="🚀 Modern Warfare Calculator", font=FONT_TITLE, bg=BG_COLOR, fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "ModernWarfare.png")
    img = Image.open(image_path)
    img = img.resize((480, 400), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    image_label = Label(left_frame, image=photo, bg=BG_COLOR)
    image_label.image = photo
    image_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))
    image_label.bind("<Button-1>", lambda e: show_full_image())
    image_label.config(cursor="hand2")

    Label(left_frame, text="⚠️ Recommended values are pre-filled below. You can change them as per your needs.",
          font=("Helvetica", 10, "bold"), fg="red", bg=BG_COLOR, justify=LEFT).grid(row=3, column=0, columnspan=2, sticky=W, pady=(0, 15))

    entries = []
    input_fields = [
        ("Initial Strength of Friendly Army (B₀):", 4, "400"),
        ("Initial Strength of Enemy Army (R₀):", 5, "200"),
        ("Threshold Percentage to End War:", 6, "50"),
        ("Red's effectiveness against Blue (β):", 7, "0.2"),
        ("Blue's effectiveness against Red (γ):", 8, "0.1")
    ]

    for text, row, default in input_fields:
        Label(left_frame, text=text, font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky=W, pady=5)
        entry = Entry(left_frame, width=30, font=FONT_NORMAL)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entries.append(entry)

    mod_B0_entry, mod_R0_entry, mod_threshold_entry, mod_beta_entry, mod_gamma_entry = entries

    Button(left_frame, text="Calculate", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_NORMAL,
           command=mod_submit_button, padx=20, pady=5).grid(row=10, column=0, columnspan=2, pady=15)

    graph_holder = Frame(right_frame, bg=BG_COLOR)
    graph_holder.pack()

    Label(right_frame, text="🎯 Choose one of the recommended value sets from the buttons below:", bg=BG_COLOR,
          font=("Helvetica", 12, "bold"), fg="#333").pack(pady=(10, 5))

    button_holder = Frame(right_frame, bg=BG_COLOR)
    button_holder.pack(pady=10)

    Button(button_holder, text="🔵 Blue's Victory", bg="blue", fg="white",
           font=("Helvetica", 10, "bold"), command=set_blue_win, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="🔴 Red's Victory", bg="red", fg="white",
           font=("Helvetica", 10, "bold"), command=set_red_win, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="⚖️ Exception Case of Early Stop", bg="#008080", fg="white",
           font=("Helvetica", 10, "bold"), command=set_equal_match, padx=10, pady=5).pack(side=LEFT, padx=8)


def Area_warfare():
    def show_full_image():
        top = Toplevel(Ar_warfare)
        top.title("Full Image - Area Warfare Model")
        full_img = Image.open(image_path)
        photo_full = ImageTk.PhotoImage(full_img)
        lbl = Label(top, image=photo_full, bg="white")
        lbl.image = photo_full
        lbl.pack()
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        img_width, img_height = full_img.size
        x = (screen_width // 2) - (img_width // 2)
        y = (screen_height // 2) - (img_height // 2)
        top.geometry(f"{img_width}x{img_height}+{x}+{y}")

    def ar_plot_graph(B0, R0, threshold_pct, beta, gamma):
        B, R = B0, R0
        t, dt = 0, 0.01
        time, B_vals, R_vals = [], [], []

        B_thresh = B0 * (threshold_pct / 100)
        R_thresh = R0 * (threshold_pct / 100)

        # Clear previous graph
        for widget in graph_holder.winfo_children():
            widget.destroy()

        # 🚩 No war case
        if threshold_pct == 100:
            Label(graph_holder, text="🚩 NO WAR TOOK PLACE", bg=BG_COLOR,
                font=("Helvetica", 12, "bold"), fg="teal").pack(pady=(10, 5))
            return

        # Override if full war
        if threshold_pct == 0:
            B_thresh, R_thresh = 0, 0

        while B > B_thresh and R > R_thresh:
            time.append(t)
            B_vals.append(B / B0)
            R_vals.append(R / R0)
            dR = -gamma * B * dt
            dB = -beta * R * dt
            R += dR
            B += dB
            t += dt

        # Clip to minimum threshold
        B = max(B, B_thresh)
        R = max(R, R_thresh)
        time.append(t)
        B_vals.append(B / B0)
        R_vals.append(R / R0)

        # Plot
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.plot(time, B_vals, label='B/B₀ (Friendly)', color='blue')
        ax.plot(time, R_vals, label='R/R₀ (Enemy)', color='red')
        ax.set_xlabel("Time")
        ax.set_ylabel("Normalized Strength")
        ax.set_title("Area Warfare: Army Strength Over Time")
        ax.legend()
        ax.grid(True)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=graph_holder)
        canvas.draw()
        canvas.get_tk_widget().pack()

        def fix(x): return 0 if abs(round(x)) == 0 else round(x)
        final_B, final_R = fix(B), fix(R)

        def simulate_full(B0, R0, beta, gamma):
            B, R = B0, R0
            while B > 0 and R > 0:
                dR = -gamma * B * dt
                dB = -beta * R * dt
                R += dR
                B += dB
            return fix(B), fix(R)

        full_B, full_R = simulate_full(B0, R0, beta, gamma)

        # 🧠 Smarter Result Logic
        if threshold_pct == 0:
            if abs(final_B - final_R) <= 1e-6:
                result_text = "🤝 Equal Match: Both armies exhausted"
                color = "#008080"
            elif final_B > final_R:
                result_text = "✅ Friendly Army (Blue) Wins!"
                color = "blue"
            else:
                result_text = "⚠️ Enemy Army (Red) Wins!"
                color = "red"
        else:
            if abs(final_B - final_R) <= 1e-6:
                result_text = "🤝 Equal Match at early termination"
                color = "#008080"
            elif final_B > final_R:
                if full_B <= 0 and full_R > 0:
                    result_text = "⏸️ Blue has more troops now, but would've lost if battle continued."
                    color = "teal"
                else:
                    result_text = "✅ Friendly Army (Blue) has advantage at early stop"
                    color = "blue"
            else:
                if full_R <= 0 and full_B > 0:
                    result_text = "⏸️ Red has more troops now, but would've lost if battle continued."
                    color = "teal"
                else:
                    result_text = "⚠️ Enemy Army (Red) has advantage at early stop"
                    color = "red"

        Label(graph_holder,
            text=f"{result_text}\n📊 Friendly (Blue) Remaining: {final_B}\n📊 Enemy (Red) Remaining: {final_R}",
            bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg=color, justify=LEFT).pack(pady=(10, 5))



    def ar_submit_button():
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) == 9:
                widget.grid_forget()
        for widget in graph_holder.winfo_children():
            widget.destroy()

        try:
            B0 = int(ar_B0_entry.get())
            R0 = int(ar_R0_entry.get())
            threshold = float(ar_threshold_entry.get())
            beta = float(ar_beta_entry.get())
            gamma = float(ar_gamma_entry.get())

            if B0 <= 0 or R0 <= 0 or beta <= 0 or gamma <= 0 or not (0 <= threshold <= 100):
                raise ValueError

            ar_plot_graph(B0, R0, threshold, beta, gamma)

        except:
            Label(left_frame, text="❌ Invalid Input (Only positive values, threshold 0–100%)",
                  bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg="red").grid(row=9, column=0, columnspan=2)

    def set_blue_win():
        ar_B0_entry.delete(0, END); ar_B0_entry.insert(0, "300")
        ar_R0_entry.delete(0, END); ar_R0_entry.insert(0, "180")
        ar_threshold_entry.delete(0, END); ar_threshold_entry.insert(0, "50")
        ar_beta_entry.delete(0, END); ar_beta_entry.insert(0, "0.1")
        ar_gamma_entry.delete(0, END); ar_gamma_entry.insert(0, "0.25")

    def set_red_win():
        ar_B0_entry.delete(0, END); ar_B0_entry.insert(0, "150")
        ar_R0_entry.delete(0, END); ar_R0_entry.insert(0, "300")
        ar_threshold_entry.delete(0, END); ar_threshold_entry.insert(0, "50")
        ar_beta_entry.delete(0, END); ar_beta_entry.insert(0, "0.25")
        ar_gamma_entry.delete(0, END); ar_gamma_entry.insert(0, "0.1")

    def set_equal_match():
        ar_B0_entry.delete(0, END); ar_B0_entry.insert(0, "150")
        ar_R0_entry.delete(0, END); ar_R0_entry.insert(0, "200")
        ar_threshold_entry.delete(0, END); ar_threshold_entry.insert(0, "50")
        ar_beta_entry.delete(0, END); ar_beta_entry.insert(0, "0.13")
        ar_gamma_entry.delete(0, END); ar_gamma_entry.insert(0, "0.3")

    # GUI Setup
    Ar_warfare = Toplevel(bg=BG_COLOR)
    Ar_warfare.title("Area Warfare Calculator")
    window_width, window_height = 1250, 810
    screen_width = Ar_warfare.winfo_screenwidth()
    screen_height = Ar_warfare.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    Ar_warfare.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    Ar_warfare.resizable(False, False)
    Ar_warfare.bind("<Escape>", lambda e: Ar_warfare.destroy())

    global left_frame, right_frame, graph_holder
    left_frame = Frame(Ar_warfare, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=30, pady=20, sticky=N)
    right_frame = Frame(Ar_warfare, bg=BG_COLOR)
    right_frame.grid(row=0, column=1, padx=10, pady=20, sticky=N)

    Label(left_frame, text="🗍 Area Warfare Calculator", font=FONT_TITLE, bg=BG_COLOR, fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "AreaWarfare.png")
    img = Image.open(image_path)
    img = img.resize((480, 400), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    image_label = Label(left_frame, image=photo, bg=BG_COLOR)
    image_label.image = photo
    image_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))
    image_label.bind("<Button-1>", lambda e: show_full_image())
    image_label.config(cursor="hand2")

    Label(left_frame, text="⚠️ Recommended values are pre-filled below. You can change them as per your needs.",
          font=("Helvetica", 10, "bold"), fg="red", bg=BG_COLOR).grid(row=3, column=0, columnspan=2, sticky=W, pady=(0, 10))

    entries = []
    fields = [
        ("Initial Strength of Friendly Army (B₀):", 4, "300"),
        ("Initial Strength of Enemy Army (R₀):", 5, "180"),
        ("Threshold Percentage to End War:", 6, "50"),
        ("Red's effectiveness against Blue (β):", 7, "0.1"),
        ("Blue's effectiveness against Red (γ):", 8, "0.25"),
    ]

    for text, row, default in fields:
        Label(left_frame, text=text, font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky=W, pady=5)
        entry = Entry(left_frame, width=30, font=FONT_NORMAL)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entries.append(entry)

    ar_B0_entry, ar_R0_entry, ar_threshold_entry, ar_beta_entry, ar_gamma_entry = entries

    Button(left_frame, text="Calculate", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_NORMAL,
           command=ar_submit_button, padx=20, pady=5).grid(row=10, column=0, columnspan=2, pady=15)

    graph_holder = Frame(right_frame, bg=BG_COLOR)
    graph_holder.pack()

    Label(right_frame, text="🎯 Choose one of the recommended value sets from the buttons below:", bg=BG_COLOR,
          font=("Helvetica", 12, "bold"), fg="#333").pack(pady=(10, 5))

    button_holder = Frame(right_frame, bg=BG_COLOR)
    button_holder.pack(pady=10)

    Button(button_holder, text="🔵 Blue's Victory", bg="blue", fg="white",
           font=("Helvetica", 10, "bold"), command=set_blue_win, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="🔴 Red's Victory", bg="red", fg="white",
           font=("Helvetica", 10, "bold"), command=set_red_win, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="⚖️ Exception Case of Early Stop", bg="#008080", fg="white",
           font=("Helvetica", 10, "bold"), command=set_equal_match, padx=10, pady=5).pack(side=LEFT, padx=8)


def Peterson_warfare():
    def show_full_image():
        top = Toplevel(Peterson_warfare_window)
        top.title("Full Image - Peterson's Law")
        full_img = Image.open(image_path)
        photo_full = ImageTk.PhotoImage(full_img)
        lbl = Label(top, image=photo_full, bg="white")
        lbl.image = photo_full
        lbl.pack()
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        img_width, img_height = full_img.size
        x = (screen_width // 2) - (img_width // 2)
        y = (screen_height // 2) - (img_height // 2)
        top.geometry(f"{img_width}x{img_height}+{x}+{y}")

    def peterson_plot_graph(B0, R0, threshold_pct, beta, gamma, m, n):
        B, R = B0, R0
        t, dt = 0, 0.01
        time, B_vals, R_vals = [], [], []

        B_thresh = B0 * (threshold_pct / 100)
        R_thresh = R0 * (threshold_pct / 100)

        if threshold_pct == 100:
            Label(graph_holder, text="🚩 NO WAR TOOK PLACE", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="teal").pack(pady=(10, 5))
            return

        if threshold_pct == 0:
            B_thresh, R_thresh = 0, 0

        while B > B_thresh and R > R_thresh:
            time.append(t)
            B_vals.append(B / B0)
            R_vals.append(R / R0)
            dR = -gamma * (B ** n) * dt
            dB = -beta * (R ** m) * dt
            R += dR
            B += dB
            t += dt

        B = max(B, B_thresh)
        R = max(R, R_thresh)
        time.append(t)
        B_vals.append(B / B0)
        R_vals.append(R / R0)

        for widget in graph_holder.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.plot(time, B_vals, label='B/B₀ (Friendly)', color='blue')
        ax.plot(time, R_vals, label='R/R₀ (Enemy)', color='red')
        ax.set_xlabel("Time")
        ax.set_ylabel("Normalized Strength")
        ax.set_title("Peterson's Attrition Law")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=graph_holder)
        canvas.draw()
        canvas.get_tk_widget().pack()

        def fix(x): return 0 if abs(round(x)) == 0 else round(x)
        final_B, final_R = fix(B), fix(R)

        def simulate_full(B0, R0, beta, gamma, m, n):
            B, R = B0, R0
            while B > 0 and R > 0:
                dR = -gamma * (B ** n) * dt
                dB = -beta * (R ** m) * dt
                R += dR
                B += dB
            return fix(B), fix(R)

        full_B, full_R = simulate_full(B0, R0, beta, gamma, m, n)

        # Smart result logic
        if threshold_pct == 0:
            if abs(final_B - final_R) <= 1e-6:
                result_text = "🤝 Equal Match: Both armies exhausted"
                color = "#008080"
            elif final_B > final_R:
                result_text = "✅ Friendly Army (Blue) Wins!"
                color = "blue"
            else:
                result_text = "⚠️ Enemy Army (Red) Wins!"
                color = "red"
        else:
            if abs(final_B - final_R) <= 1e-6:
                result_text = "🤝 Equal Match at early termination"
                color = "#008080"
            elif final_B > final_R:
                if full_B <= 0 and full_R > 0:
                    result_text = "⏸️ Blue has more troops now, but would've lost if battle continued."
                    color = "teal"
                else:
                    result_text = "✅ Friendly Army (Blue) has advantage at early stop"
                    color = "blue"
            else:
                if full_R <= 0 and full_B > 0:
                    result_text = "⏸️ Red has more troops now, but would've lost if battle continued."
                    color = "teal"
                else:
                    result_text = "⚠️ Enemy Army (Red) has advantage at early stop"
                    color = "red"

        Label(graph_holder,
              text=f"{result_text}\n📊 Friendly (Blue) Remaining: {final_B}\n📊 Enemy (Red) Remaining: {final_R}",
              bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg=color, justify=LEFT).pack(pady=(10, 5))

    def peterson_submit_button():
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) == 11:
                widget.grid_forget()
        for widget in graph_holder.winfo_children():
            widget.destroy()

        try:
            B0 = int(pet_B0_entry.get())
            R0 = int(pet_R0_entry.get())
            threshold = float(pet_threshold_entry.get())
            beta = float(pet_beta_entry.get())
            gamma = float(pet_gamma_entry.get())
            m = float(pet_m_entry.get())
            n = float(pet_n_entry.get())

            if B0 <= 0 or R0 <= 0 or beta <= 0 or gamma <= 0 or m < 0 or n < 0 or not (0 <= threshold <= 100):
                raise ValueError

            peterson_plot_graph(B0, R0, threshold, beta, gamma, m, n)

        except:
            Label(left_frame, text="❌ Invalid Input (Positive values only, Threshold: 0–100%)",
                  bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg="red").grid(row=11, column=0, columnspan=2)

    # GUI Setup same as before with updated field order & color logic
    Peterson_warfare_window = Toplevel(bg=BG_COLOR)
    Peterson_warfare_window.title("Peterson's Attrition Law")
    window_width, window_height = 1250, 810
    screen_width = Peterson_warfare_window.winfo_screenwidth()
    screen_height = Peterson_warfare_window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    Peterson_warfare_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    Peterson_warfare_window.resizable(False, False)
    Peterson_warfare_window.bind("<Escape>", lambda e: Peterson_warfare_window.destroy())

    global left_frame, right_frame, graph_holder
    left_frame = Frame(Peterson_warfare_window, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=30, pady=20, sticky=N)

    right_frame = Frame(Peterson_warfare_window, bg=BG_COLOR)
    right_frame.grid(row=0, column=1, padx=10, pady=20, sticky=N)

    Label(left_frame, text="📘 Peterson’s Attrition Law Calculator", font=FONT_TITLE, bg=BG_COLOR, fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "PetersonLaw.png")
    img = Image.open(image_path).resize((480, 350), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    image_label = Label(left_frame, image=photo, bg=BG_COLOR)
    image_label.image = photo
    image_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))
    image_label.bind("<Button-1>", lambda e: show_full_image())
    image_label.config(cursor="hand2")

    Label(left_frame, text="⚠️ Recommended values are pre-filled below. You can change them as per your needs.",
          font=("Helvetica", 10, "bold"), fg="red", bg=BG_COLOR).grid(row=2, column=0, columnspan=2, sticky=W, pady=(0, 10))

    entries = []
    fields = [
        ("Initial Strength of Friendly Army (B₀):", 3, "300"),
        ("Initial Strength of Enemy Army (R₀):", 4, "180"),
        ("Threshold Percentage to End War:", 5, "50"),
        ("Blue's effectiveness against Red (β):", 6, "0.25"),
        ("Red's effectiveness against Blue (γ):", 7, "0.1"),
        ("Exponent m (for Friendly):", 8, "1.2"),
        ("Exponent n (for Enemy):", 9, "1.4"),
    ]

    for text, row, default in fields:
        Label(left_frame, text=text, font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky=W, pady=5)
        entry = Entry(left_frame, width=30, font=FONT_NORMAL)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entries.append(entry)

    pet_B0_entry, pet_R0_entry, pet_threshold_entry, pet_beta_entry, pet_gamma_entry, pet_m_entry, pet_n_entry = entries

    Button(left_frame, text="Simulate Battle", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_NORMAL,
           command=peterson_submit_button, padx=20, pady=5).grid(row=10, column=0, pady=(10, 0), sticky=W)
    Button(left_frame, text="Exit", bg="crimson", fg="white", font=FONT_NORMAL,
           command=Peterson_warfare_window.destroy, padx=20, pady=5).grid(row=10, column=1, pady=(10, 0), sticky=E)

    graph_holder = Frame(right_frame, bg=BG_COLOR)
    graph_holder.pack(fill=BOTH, expand=True)

    Label(right_frame, text="🎯 Choose one of the recommended value sets from the buttons below:", bg=BG_COLOR,
          font=("Helvetica", 12, "bold"), fg="#333").pack(pady=(10, 5))

    def set_blue_win():
        pet_B0_entry.delete(0, END); pet_B0_entry.insert(0, "280")      # Strong Blue force
        pet_R0_entry.delete(0, END); pet_R0_entry.insert(0, "200")      # Weaker Red force
        pet_threshold_entry.delete(0, END); pet_threshold_entry.insert(0, "40")  # 40% cutoff
        pet_beta_entry.delete(0, END); pet_beta_entry.insert(0, "0.12") # Moderate Red attrition rate
        pet_gamma_entry.delete(0, END); pet_gamma_entry.insert(0, "0.18")# Higher Blue damage impact
        pet_m_entry.delete(0, END); pet_m_entry.insert(0, "1.3")        # Blue's power exponent
        pet_n_entry.delete(0, END); pet_n_entry.insert(0, "1.1")        # Red's power exponent


    def set_red_win():
        pet_B0_entry.delete(0, END); pet_B0_entry.insert(0, "200")       # Weaker Blue force
        pet_R0_entry.delete(0, END); pet_R0_entry.insert(0, "320")       # Stronger Red force
        pet_threshold_entry.delete(0, END); pet_threshold_entry.insert(0, "45")  # 45% threshold
        pet_beta_entry.delete(0, END); pet_beta_entry.insert(0, "0.20")  # Stronger Red attack rate
        pet_gamma_entry.delete(0, END); pet_gamma_entry.insert(0, "0.09")# Weaker Blue attack rate
        pet_m_entry.delete(0, END); pet_m_entry.insert(0, "1.1")         # Weaker Blue exponent
        pet_n_entry.delete(0, END); pet_n_entry.insert(0, "1.3")         # Stronger Red exponent


    def set_equal_match():
        pet_B0_entry.delete(0, END); pet_B0_entry.insert(0, "280")
        pet_R0_entry.delete(0, END); pet_R0_entry.insert(0, "215")
        pet_threshold_entry.delete(0, END); pet_threshold_entry.insert(0, "40")
        pet_beta_entry.delete(0, END); pet_beta_entry.insert(0, "0.12")
        pet_gamma_entry.delete(0, END); pet_gamma_entry.insert(0, "0.18")
        pet_m_entry.delete(0, END); pet_m_entry.insert(0, "1.3")
        pet_n_entry.delete(0, END); pet_n_entry.insert(0, "1.1")


    button_holder = Frame(right_frame, bg=BG_COLOR)
    button_holder.pack(pady=10)
    Button(button_holder, text="🔵 Blue's Victory", bg="blue", fg="white",
           font=("Helvetica", 10, "bold"), command=set_blue_win, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="🔴 Red's Victory", bg="red", fg="white",
           font=("Helvetica", 10, "bold"), command=set_red_win, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="⚖️ Equal Match", bg="#008080", fg="white",
           font=("Helvetica", 10, "bold"), command=set_equal_match, padx=10, pady=5).pack(side=LEFT, padx=8)


def Guerrilla_warfare():
    def show_full_image():
        top = Toplevel(Guerrilla_warfare_window)
        top.title("Full Image - Guerrilla Warfare Model")

        full_img = Image.open(image_path)
        photo_full = ImageTk.PhotoImage(full_img)

        lbl = Label(top, image=photo_full, bg="white")
        lbl.image = photo_full  # Keep a reference!
        lbl.pack()

        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        img_width, img_height = full_img.size
        x = (screen_width // 2) - (img_width // 2)
        y = (screen_height // 2) - (img_height // 2)
        top.geometry(f"{img_width}x{img_height}+{x}+{y}")

    def guerrilla_plot_graph(R0, G0, beta, gamma, n, m):
        R = R0
        G = G0
        t = 0
        dt = 0.01
        time, R_vals, G_vals = [], [], []
        threshold = 0.01

        while R > threshold * R0 and G > threshold * G0:
            time.append(t)
            R_vals.append(R / R0)
            G_vals.append(G / G0)

            dR = -gamma * (G ** n) * dt
            dG = -beta * (R ** m) * G * dt
            R = max(0, R + dR)
            G = max(0, G + dG)
            t += dt

        Rf = max(0, R)
        Gf = max(0, G)
        R_casualties = R0 - Rf
        G_casualties = G0 - Gf

        if Rf > Gf:
            winner = "Enemy Force"
            result_color = "red"
        elif Gf > Rf:
            winner = "Friendly Force"
            result_color = "blue"
        else:
            winner = "Draw"
            result_color = "#008080"

        for widget in graph_holder.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        ax.plot(time, R_vals, label='R/R₀ (Enemy)', color='red')
        ax.plot(time, G_vals, label='G/G₀ (Friendly)', color='blue')
        ax.set_xlabel("Time")
        ax.set_ylabel("Normalized Strength")
        ax.set_title("Guerrilla Warfare Model: Strength Over Time")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=graph_holder)
        canvas.draw()
        canvas.get_tk_widget().pack()

        insights = (
            f"⏳ War Duration: {round(t, 2)} time units\n"
            f"🟥 Final Enemy Strength (Rf): {round(Rf, 2)}\n"
            f"🟦 Final Friendly Strength (Gf): {round(Gf, 2)}\n"
            f"⚔️ Enemy Casualties: {round(R_casualties, 2)}\n"
            f"💥 Friendly Casualties: {round(G_casualties, 2)}\n"
            f"🏁 Winner: {winner}"
        )

        Label(graph_holder, text=insights, bg=BG_COLOR, font=("Helvetica", 12, "bold"),
              fg=result_color, justify=LEFT, anchor=W).pack(pady=(10, 0), anchor='w')

    def guerrilla_submit_button():
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) == 12:
                widget.grid_forget()
        for widget in graph_holder.winfo_children():
            widget.destroy()

        try:
            G0_val = guer_G0_entry.get()
            R0_val = guer_R0_entry.get()
            beta_val = guer_beta_entry.get()
            gamma_val = guer_gamma_entry.get()
            m_val = guer_m_entry.get()
            n_val = guer_n_entry.get()

            if not (R0_val.isdigit() and G0_val.isdigit()):
                raise TypeError("IntegralError")

            R0 = int(R0_val)
            G0 = int(G0_val)
            beta = float(beta_val)
            gamma = float(gamma_val)
            m = float(m_val)
            n = float(n_val)

            if R0 == 0 or G0 == 0:
                raise ZeroDivisionError("ZeroStrength")

            if R0 < 0 or G0 < 0 or beta <= 0 or gamma <= 0 or m < 0 or n < 0:
                raise ValueError("NegativeOrInvalid")

            guerrilla_plot_graph(R0, G0, beta, gamma, n, m)

        except TypeError:
            Label(left_frame, text="❌ Invalid Input (Positive Integral Values Only)", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=12, column=0, columnspan=2)
        except ZeroDivisionError:
            Label(left_frame, text="❌ Invalid Input (Initial Strength can't be 0)", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=12, column=0, columnspan=2)
        except ValueError:
            Label(left_frame, text="❌ Invalid Input (Negative or illogical values)", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=12, column=0, columnspan=2)

    Guerrilla_warfare_window = Toplevel()
    Guerrilla_warfare_window.title("Guerrilla Warfare Model")
    window_width = 1250
    window_height = 810
    screen_width = Guerrilla_warfare_window.winfo_screenwidth()
    screen_height = Guerrilla_warfare_window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    Guerrilla_warfare_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    global left_frame, right_frame, graph_holder
    left_frame = Frame(Guerrilla_warfare_window, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=30, pady=20, sticky=N)

    right_frame = Frame(Guerrilla_warfare_window, bg=BG_COLOR)
    right_frame.grid(row=0, column=1, padx=10, pady=20, sticky=N)

    Label(left_frame, text="🕵️ Guerrilla Warfare Model", font=FONT_TITLE, bg=BG_COLOR, fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "GuerrillaWarfare.png")

    img = Image.open(image_path)
    img = img.resize((480, 340), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    image_label = Label(left_frame, image=photo, bg=BG_COLOR)
    image_label.image = photo
    image_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))
    image_label.bind("<Button-1>", lambda e: show_full_image())
    image_label.config(cursor="hand2")

    Label(left_frame, text="⚠️ Recommended values are pre-filled below. You can change them as per your needs.",
          font=("Helvetica", 10, "bold"), fg="red", bg=BG_COLOR, justify=LEFT).grid(row=3, column=0, columnspan=2, sticky=W, pady=(0, 15))

    entries = []
    fields = [
        ("Initial Strength of Friendly Force (G₀):", 4, "300"),
        ("Initial Strength of Enemy Force (R₀):", 5, "100"),
        ("Effectiveness of Friendly Force (β):", 6, "0.5"),
        ("Effectiveness of Enemy Force (γ):", 7, "0.5"),
        ("Exponent m (Enemy on Friendly):", 8, "1"),
        ("Exponent n (Friendly on Enemy):", 9, "1")
    ]
    for label_text, row, default in fields:
        Label(left_frame, text=label_text, font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky=W, pady=5)
        entry = Entry(left_frame, width=30, font=FONT_NORMAL)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entries.append(entry)

    guer_G0_entry, guer_R0_entry, guer_beta_entry, guer_gamma_entry, guer_m_entry, guer_n_entry = entries

    Button(left_frame, text="Simulate Battle", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_NORMAL,
           command=guerrilla_submit_button, padx=20, pady=5).grid(row=11, column=0, pady=15, sticky=W)

    Button(left_frame, text="Exit", bg="crimson", fg="white", font=FONT_NORMAL,
           command=Guerrilla_warfare_window.destroy).grid(row=11, column=1, pady=15, sticky=E)

    graph_holder = Frame(right_frame, bg=BG_COLOR)
    graph_holder.pack(fill=BOTH, expand=True)

    Label(right_frame, text="🎯 Choose one of the recommended value sets from the buttons below:", bg=BG_COLOR,
          font=("Helvetica", 12, "bold"), fg="#333").pack(pady=(10, 5))

    def set_red_win():
        guer_R0_entry.delete(0, END)
        guer_R0_entry.insert(0, "900")
        guer_G0_entry.delete(0, END)
        guer_G0_entry.insert(0, "1100")
        guer_beta_entry.delete(0, END)
        guer_beta_entry.insert(0, "0.0001")
        guer_gamma_entry.delete(0, END)
        guer_gamma_entry.insert(0, "0.03")
        guer_m_entry.delete(0, END)
        guer_m_entry.insert(0, "1")
        guer_n_entry.delete(0, END)
        guer_n_entry.insert(0, "1")

    def set_blue_win():
        guer_R0_entry.delete(0, END)
        guer_R0_entry.insert(0, "800")
        guer_G0_entry.delete(0, END)
        guer_G0_entry.insert(0, "1000")
        guer_beta_entry.delete(0, END)
        guer_beta_entry.insert(0, "0.0001")
        guer_gamma_entry.delete(0, END)
        guer_gamma_entry.insert(0, "0.05")
        guer_m_entry.delete(0, END)
        guer_m_entry.insert(0, "1")
        guer_n_entry.delete(0, END)
        guer_n_entry.insert(0, "1")

    button_holder = Frame(right_frame, bg=BG_COLOR)
    button_holder.pack(pady=10)

    Button(button_holder, text="🔵 Blue's Victory", bg="blue", fg="white",
           font=("Helvetica", 10, "bold"), command=set_blue_win, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="🔴 Red's Victory", bg="red", fg="white",
           font=("Helvetica", 10, "bold"), command=set_red_win, padx=10, pady=5).pack(side=LEFT, padx=8)


def Taylor_Helmbold_warfare():
    def show_full_image():
        top = Toplevel(Taylor_warfare_window)
        top.title("Full Image - Taylor Helmbold Warfare")

        full_img = Image.open(image_path)
        photo_full = ImageTk.PhotoImage(full_img)

        lbl = Label(top, image=photo_full, bg="white")
        lbl.image = photo_full
        lbl.pack()

        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        img_width, img_height = full_img.size
        x = (screen_width // 2) - (img_width // 2)
        y = (screen_height // 2) - (img_height // 2)
        top.geometry(f"{img_width}x{img_height}+{x}+{y}")

    def taylor_plot_graph(R0, B0, beta, gamma, delta, theta):
        R, B = R0, B0
        t, dt = 0.1, 0.1
        time, R_vals, B_vals = [], [], []

        while R > 1 and B > 1:
            time.append(t)
            R_vals.append(R / R0)
            B_vals.append(B / B0)

            dR = -gamma * B - delta * (B ** 0.5)
            dB = -beta * R - theta * (R ** 0.5)

            R = max(0, R + dR * dt)
            B = max(0, B + dB * dt)
            t += dt

        Rf, Bf = max(0, R), max(0, B)
        R_casualties, B_casualties = R0 - Rf, B0 - Bf

        if Rf > Bf:
            winner = "Enemy Army"
            result_color = "red"
        elif Bf > Rf:
            winner = "Friendly Army"
            result_color = "blue"
        else:
            winner = "Draw"
            result_color = "#008080"

        for widget in graph_holder.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        if abs(R_casualties - B_casualties) < 1e-6:
            ax.plot(time, R_vals, label="Equal Loss (Red & Blue)", color="#008080", linewidth=2)
        else:
            ax.plot(time, R_vals, label="R/R₀ (Enemy)", color='red', linewidth=2)
            ax.plot(time, B_vals, label="B/B₀ (Friendly)", color='blue', linewidth=2)

        ax.set_xlabel("Time")
        ax.set_ylabel("Normalized Strength")
        ax.set_title("Taylor-Helmbold Attrition Model")
        ax.legend()
        ax.grid(True)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=graph_holder)
        canvas.draw()
        canvas.get_tk_widget().pack()

        insights = (
            f"⏱️ War Duration: {round(t, 2)} time units\n"
            f"🟥 Final Enemy Strength (Rf): {round(Rf, 2)}\n"
            f"🟦 Final Friendly Strength (Bf): {round(Bf, 2)}\n"
            f"🔻 Enemy Casualties: {round(R_casualties, 2)}\n"
            f"🔻 Friendly Casualties: {round(B_casualties, 2)}\n"
            f"🏁 Winner: {winner}"
        )

        Label(graph_holder, text=insights, bg=BG_COLOR, font=("Helvetica", 12, "bold"),
              fg=result_color, justify=LEFT).pack(pady=(10, 0), anchor='w')

    def taylor_submit_button():
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) == 12:
                widget.destroy()
        for widget in graph_holder.winfo_children():
            widget.destroy()

        try:
            B0_val = taylor_B0_entry.get()
            R0_val = taylor_R0_entry.get()
            beta_val = taylor_beta_entry.get()
            gamma_val = taylor_gamma_entry.get()
            delta_val = taylor_delta_entry.get()
            theta_val = taylor_theta_entry.get()

            if not (R0_val.isdigit() and B0_val.isdigit()):
                raise TypeError("IntegralError")

            R0 = int(R0_val)
            B0 = int(B0_val)
            beta = float(beta_val)
            gamma = float(gamma_val)
            delta = float(delta_val)
            theta = float(theta_val)

            if R0 == 0 or B0 == 0:
                raise ZeroDivisionError("ZeroStrength")

            if R0 < 0 or B0 < 0 or beta <= 0 or gamma <= 0 or delta < 0 or theta < 0:
                raise ValueError("NegativeOrInvalid")

            taylor_plot_graph(R0, B0, beta, gamma, delta, theta)

        except TypeError:
            Label(left_frame, text="❌ Invalid Input (Positive Integral Values Only)",
                  bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg="red").grid(row=12, column=0, columnspan=2)
        except ZeroDivisionError:
            Label(left_frame, text="❌ Invalid Input (Initial Strength can't be 0)",
                  bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg="red").grid(row=12, column=0, columnspan=2)
        except ValueError:
            Label(left_frame, text="❌ Invalid Input (Negative or illogical values)",
                  bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg="red").grid(row=12, column=0, columnspan=2)

    Taylor_warfare_window = Toplevel(bg=BG_COLOR)
    Taylor_warfare_window.title("Taylor-Helmbold Warfare Model")
    window_width = 1250
    window_height = 810
    screen_width = Taylor_warfare_window.winfo_screenwidth()
    screen_height = Taylor_warfare_window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    Taylor_warfare_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    Taylor_warfare_window.bind("<Escape>", lambda e: Taylor_warfare_window.destroy())

    global left_frame, right_frame, graph_holder
    left_frame = Frame(Taylor_warfare_window, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=30, pady=20, sticky=N)

    right_frame = Frame(Taylor_warfare_window, bg=BG_COLOR)
    right_frame.grid(row=0, column=1, padx=10, pady=20, sticky=N)

    Label(left_frame, text="📘 Taylor-Helmbold Attrition Model", font=FONT_TITLE, bg=BG_COLOR, fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "TaylorHelmboldModel.png")

    img = Image.open(image_path)
    img = img.resize((480, 350), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    image_label = Label(left_frame, image=photo, bg=BG_COLOR)
    image_label.image = photo
    image_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))
    image_label.bind("<Button-1>", lambda e: show_full_image())
    image_label.config(cursor="hand2")

    Label(left_frame, text="⚠️ Recommended values are pre-filled below. You can change them as per your needs.",
          font=("Helvetica", 10, "bold"), fg="red", bg=BG_COLOR).grid(row=3, column=0, columnspan=2, sticky=W, pady=(1, 1))

    # ⬅️ Friendly inputs come first
    inputs = [
        ("Initial Strength of Friendly Army (B₀):", 4, "200"),
        ("Initial Strength of Enemy Army (R₀):", 5, "100"),
        ("Effectiveness of Enemy Army (β):", 6, "0.2"),
        ("Effectiveness of Friendly Army (γ):", 7, "0.1"),
        ("Square-root impact on Enemy (δ):", 8, "1.4"),
        ("Square-root impact on Friendly (θ):", 9, "1.2"),
    ]
    entries = []
    for label_text, row, default in inputs:
        Label(left_frame, text=label_text, font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky=W, pady=5)
        entry = Entry(left_frame, width=30, font=FONT_NORMAL)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entries.append(entry)

    taylor_B0_entry, taylor_R0_entry, taylor_beta_entry, taylor_gamma_entry, taylor_delta_entry, taylor_theta_entry = entries

    Button(left_frame, text="Simulate Battle", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_NORMAL,
           command=taylor_submit_button, padx=20, pady=5).grid(row=11, column=0, pady=20, sticky=W)

    Button(left_frame, text="Exit", bg="crimson", fg="white", font=FONT_NORMAL,
           command=Taylor_warfare_window.destroy).grid(row=11, column=1, pady=20, sticky=E)

    graph_holder = Frame(right_frame, bg=BG_COLOR)
    graph_holder.pack(fill=BOTH, expand=True)

    Label(right_frame, text="🎯 Choose one of the recommended value sets from the buttons below:", bg=BG_COLOR,
          font=("Helvetica", 12, "bold"), fg="#333").pack(pady=(10, 5))

    def set_red_win():
        taylor_B0_entry.delete(0, END)
        taylor_B0_entry.insert(0, "150")
        taylor_R0_entry.delete(0, END)
        taylor_R0_entry.insert(0, "300")
        taylor_beta_entry.delete(0, END)
        taylor_beta_entry.insert(0, "0.2")
        taylor_gamma_entry.delete(0, END)
        taylor_gamma_entry.insert(0, "0.08")
        taylor_delta_entry.delete(0, END)
        taylor_delta_entry.insert(0, "1.0")
        taylor_theta_entry.delete(0, END)
        taylor_theta_entry.insert(0, "1.4")

    def set_blue_win():
        taylor_B0_entry.delete(0, END)
        taylor_B0_entry.insert(0, "330")
        taylor_R0_entry.delete(0, END)
        taylor_R0_entry.insert(0, "160")
        taylor_beta_entry.delete(0, END)
        taylor_beta_entry.insert(0, "0.2")
        taylor_gamma_entry.delete(0, END)
        taylor_gamma_entry.insert(0, "0.08")
        taylor_delta_entry.delete(0, END)
        taylor_delta_entry.insert(0, "0.1")
        taylor_theta_entry.delete(0, END)
        taylor_theta_entry.insert(0, "1.0")

    def set_equal_match():
        taylor_B0_entry.delete(0, END)
        taylor_B0_entry.insert(0, "250")
        taylor_R0_entry.delete(0, END)
        taylor_R0_entry.insert(0, "250")
        taylor_beta_entry.delete(0, END)
        taylor_beta_entry.insert(0, "0.1")
        taylor_gamma_entry.delete(0, END)
        taylor_gamma_entry.insert(0, "0.1")
        taylor_delta_entry.delete(0, END)
        taylor_delta_entry.insert(0, "1.2")
        taylor_theta_entry.delete(0, END)
        taylor_theta_entry.insert(0, "1.2")

    button_holder = Frame(right_frame, bg=BG_COLOR)
    button_holder.pack(pady=10)

    Button(button_holder, text="🔵 Blue's Victory", bg="blue", fg="white",
           font=("Helvetica", 10, "bold"), command=set_blue_win, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="🔴 Red's Victory", bg="red", fg="white",
           font=("Helvetica", 10, "bold"), command=set_red_win, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="⚖️ Equal Match", bg="#008080", fg="white",
           font=("Helvetica", 10, "bold"), command=set_equal_match, padx=10, pady=5).pack(side=LEFT, padx=8)


def Hartley_warfare():
    def show_full_image():
        top = Toplevel(Hartley_warfare_window)
        top.title("Full Image - Hartley’s Model")

        full_img = Image.open(image_path)
        photo_full = ImageTk.PhotoImage(full_img)

        lbl = Label(top, image=photo_full)
        lbl.image = photo_full  # Keep a reference
        lbl.pack()

        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        img_width, img_height = full_img.size
        x = (screen_width // 2) - (img_width // 2)
        y = (screen_height // 2) - (img_height // 2)
        top.geometry(f"{img_width}x{img_height}+{x}+{y}")

    def hartley_plot_graph(B0, R0, beta, gamma, m, n, p, q):
        B = B0
        R = R0
        t = 0
        dt = 0.1
        time = []
        B_vals = []
        R_vals = []

        while B > 1 and R > 1:
            time.append(t)
            B_vals.append(B / B0)
            R_vals.append(R / R0)

            dR = -gamma * (B ** p) * (R ** q)
            dB = -beta * (R ** m) * (B ** n)

            R = max(0, R + dR * dt)
            B = max(0, B + dB * dt)
            t += dt

        Rf = max(0, R)
        Bf = max(0, B)
        R_casualties = R0 - Rf
        B_casualties = B0 - Bf

        if Bf > Rf:
            winner = "Friendly Army"
            result_color = "blue"
        elif Rf > Bf:
            winner = "Enemy Army"
            result_color = "red"
        else:
            winner = "Draw"
            result_color = "#008080"

        for widget in graph_holder.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

        if abs(R_casualties - B_casualties) < 1e-6:
            ax.plot(time, R_vals, label="Equal Loss (Red & Blue)", color="#008080", linewidth=2)
        else:
            ax.plot(time, B_vals, label='B/B₀ (Friendly)', color='blue', linewidth=2)
            ax.plot(time, R_vals, label='R/R₀ (Enemy)', color='red', linewidth=2)

        ax.set_xlabel("Time")
        ax.set_ylabel("Normalized Strength")
        ax.set_title("Hartley’s Generalized Attrition Model")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=graph_holder)
        canvas.draw()
        canvas.get_tk_widget().pack()

        insights = (
            f"📅 War Duration: {round(t, 2)} time units\n"
            f"🔵 Final Friendly Strength (Bf): {round(Bf, 2)}\n"
            f"🔴 Final Enemy Strength (Rf): {round(Rf, 2)}\n"
            f"⚔️ Friendly Casualties: {round(B_casualties, 2)}\n"
            f"⚔️ Enemy Casualties: {round(R_casualties, 2)}\n"
            f"🏳️ Winner: {winner}"
        )

        Label(graph_holder, text=insights.strip(), bg=BG_COLOR, font=("Helvetica", 12, "bold"),
              fg=result_color, justify=LEFT, anchor=W).pack(pady=(10, 0), anchor='w')

    def hartley_submit_button():
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) == 12:
                widget.grid_forget()
        for widget in graph_holder.winfo_children():
            widget.destroy()

        try:
            B0_val = hart_B0_entry.get()
            R0_val = hart_R0_entry.get()
            beta_val = hart_beta_entry.get()
            gamma_val = hart_gamma_entry.get()
            m_val = hart_m_entry.get()
            n_val = hart_n_entry.get()
            p_val = hart_p_entry.get()
            q_val = hart_q_entry.get()

            if not (R0_val.isdigit() and B0_val.isdigit()):
                raise TypeError("IntegralError")

            B0 = int(B0_val)
            R0 = int(R0_val)
            beta = float(beta_val)
            gamma = float(gamma_val)
            m = float(m_val)
            n = float(n_val)
            p = float(p_val)
            q = float(q_val)

            if R0 == 0 or B0 == 0:
                raise ZeroDivisionError("ZeroStrength")

            if R0 < 0 or B0 < 0 or beta <= 0 or gamma <= 0 or m < 0 or n < 0 or p < 0 or q < 0:
                raise ValueError("NegativeOrInvalid")

            hartley_plot_graph(B0, R0, beta, gamma, m, n, p, q)

        except TypeError:
            Label(left_frame, text="❌ Invalid Input (Positive Integral Values Only)",
                  bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg="red").grid(row=12, column=0, columnspan=2)

        except ZeroDivisionError:
            Label(left_frame, text="❌ Invalid Input (Initial Strength can't be 0)",
                  bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg="red").grid(row=12, column=0, columnspan=2)

        except ValueError:
            Label(left_frame, text="❌ Invalid Input (Negative or illogical values)",
                  bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg="red").grid(row=12, column=0, columnspan=2)

    Hartley_warfare_window = Toplevel()
    Hartley_warfare_window.title("Hartley’s Generalized Attrition Model")
    window_width = 1250
    window_height = 810
    screen_width = Hartley_warfare_window.winfo_screenwidth()
    screen_height = Hartley_warfare_window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    Hartley_warfare_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    Hartley_warfare_window.configure(bg=BG_COLOR)
    Hartley_warfare_window.bind("<Escape>", lambda e: Hartley_warfare_window.destroy())

    global left_frame, right_frame, graph_holder
    left_frame = Frame(Hartley_warfare_window, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=30, pady=20, sticky=N)

    right_frame = Frame(Hartley_warfare_window, bg=BG_COLOR)
    right_frame.grid(row=0, column=1, padx=10, pady=20, sticky=N)

    Label(left_frame, text="📘 Hartley’s Generalized Attrition Model", font=FONT_TITLE, bg=BG_COLOR, fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "HartleysGeneralizedModel.png")

    img = Image.open(image_path)
    img = img.resize((450, 310), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    image_label = Label(left_frame, image=photo, bg=BG_COLOR)
    image_label.image = photo
    image_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))
    image_label.bind("<Button-1>", lambda e: show_full_image())
    image_label.config(cursor="hand2")

    Label(left_frame, text="⚠️ Recommended values are pre-filled below. You can change them as per your needs.",
          font=("Helvetica", 10, "bold"), fg="red", bg=BG_COLOR, justify=LEFT).grid(row=3, column=0, columnspan=2, sticky=W, pady=(0, 1))

    entries = []
    input_fields = [
        ("Initial Strength of Friendly Army (B₀):", 4, "1000"),
        ("Initial Strength of Enemy Army (R₀):", 5, "800"),
        ("Effectiveness of Enemy Army (Gamma):", 7, "0.0012"),
        ("Effectiveness of Friendly Army (Beta):", 6, "0.001"),
        ("Exponent m (R on B):", 8, "0.2"),
        ("Exponent n (B on itself):", 9, "1.1"),
        ("Exponent p (B on R):", 10, "0.2"),
        ("Exponent q (R on itself):", 11, "1"),
    ]
    for text, row, default in input_fields:
        Label(left_frame, text=text, font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky=W, pady=5)
        entry = Entry(left_frame, width=30, font=FONT_NORMAL)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entries.append(entry)

    hart_B0_entry, hart_R0_entry, hart_beta_entry, hart_gamma_entry, hart_m_entry, hart_n_entry, hart_p_entry, hart_q_entry = entries

    Button(left_frame, text="Simulate Battle", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_NORMAL,
           command=hartley_submit_button, padx=20, pady=5).grid(row=13, column=0, pady=15, sticky=W)

    Button(left_frame, text="Exit", bg="crimson", fg="white", font=FONT_NORMAL,
           command=Hartley_warfare_window.destroy, padx=20, pady=5).grid(row=13, column=1, pady=15, sticky=E)

    graph_holder = Frame(right_frame, bg=BG_COLOR)
    graph_holder.pack(fill=BOTH, expand=True)

    Label(right_frame, text="🎯 Choose one of the recommended value sets from the buttons below:", bg=BG_COLOR,
          font=("Helvetica", 12, "bold"), fg="#333").pack(pady=(10, 5))

    def set_blue_win():
        hart_B0_entry.delete(0, END)
        hart_B0_entry.insert(0, "1200")
        hart_R0_entry.delete(0, END)
        hart_R0_entry.insert(0, "800")
        hart_beta_entry.delete(0, END)
        hart_beta_entry.insert(0, "0.0015")
        hart_gamma_entry.delete(0, END)
        hart_gamma_entry.insert(0, "0.001")
        hart_m_entry.delete(0, END)
        hart_m_entry.insert(0, "0.2")
        hart_n_entry.delete(0, END)
        hart_n_entry.insert(0, "1")
        hart_p_entry.delete(0, END)
        hart_p_entry.insert(0, "0.3")
        hart_q_entry.delete(0, END)
        hart_q_entry.insert(0, "1.1")

    def set_red_win():
        hart_B0_entry.delete(0, END)
        hart_B0_entry.insert(0, "800")
        hart_R0_entry.delete(0, END)
        hart_R0_entry.insert(0, "1200")
        hart_beta_entry.delete(0, END)
        hart_beta_entry.insert(0, "0.001")
        hart_gamma_entry.delete(0, END)
        hart_gamma_entry.insert(0, "0.0015")
        hart_m_entry.delete(0, END)
        hart_m_entry.insert(0, "0.2")
        hart_n_entry.delete(0, END)
        hart_n_entry.insert(0, "1.1")
        hart_p_entry.delete(0, END)
        hart_p_entry.insert(0, "0.2")
        hart_q_entry.delete(0, END)
        hart_q_entry.insert(0, "1")

    def set_equal_match():
        hart_B0_entry.delete(0, END)
        hart_B0_entry.insert(0, "1000")
        hart_R0_entry.delete(0, END)
        hart_R0_entry.insert(0, "1000")
        hart_beta_entry.delete(0, END)
        hart_beta_entry.insert(0, "0.00125")
        hart_gamma_entry.delete(0, END)
        hart_gamma_entry.insert(0, "0.00125")
        hart_m_entry.delete(0, END)
        hart_m_entry.insert(0, "0.25")
        hart_n_entry.delete(0, END)
        hart_n_entry.insert(0, "1.05")
        hart_p_entry.delete(0, END)
        hart_p_entry.insert(0, "0.25")
        hart_q_entry.delete(0, END)
        hart_q_entry.insert(0, "1.05")

    button_holder = Frame(right_frame, bg=BG_COLOR)
    button_holder.pack(pady=10)

    Button(button_holder, text="🔵 Blue's Victory", bg="blue", fg="white",
           font=("Helvetica", 10, "bold"), command=set_blue_win, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="🔴 Red's Victory", bg="red", fg="white",
           font=("Helvetica", 10, "bold"), command=set_red_win, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="⚖️ Equal Match", bg="#008080", fg="white",
           font=("Helvetica", 10, "bold"), command=set_equal_match, padx=10, pady=5).pack(side=LEFT, padx=8)


def A_rule_termination():
    def show_full_image():
        top = Toplevel(A_rule_window)
        top.title("Full Image - A-Rule")

        full_img = Image.open(image_path)
        photo_full = ImageTk.PhotoImage(full_img)
        lbl = Label(top, image=photo_full, bg="white")
        lbl.image = photo_full
        lbl.pack()

        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        img_width, img_height = full_img.size
        x = (screen_width // 2) - (img_width // 2)
        y = (screen_height // 2) - (img_height // 2)
        top.geometry(f"{img_width}x{img_height}+{x}+{y}")

    def a_rule_simulation(B0, R0, beta, gamma, fb, fr):
        B = B0
        R = R0
        t = 0
        dt = 0.1
        time = []
        B_vals = []
        R_vals = []

        B_breakpoint = fb * B0
        R_breakpoint = fr * R0

        while B > B_breakpoint and R > R_breakpoint:
            time.append(t)
            B_vals.append(B / B0)
            R_vals.append(R / R0)

            dB = -beta * R * dt
            dR = -gamma * B * dt

            B = max(0, B + dB)
            R = max(0, R + dR)
            t += dt

            if t > 1000:
                break

        Bf = max(0, B)
        Rf = max(0, R)

        if B <= B_breakpoint and R <= R_breakpoint:
            winner = "Equal Match (Draw)"
            result_color = "#008080"
        elif R <= R_breakpoint:
            winner = "Friendly Army"
            result_color = "blue"
        elif B <= B_breakpoint:
            winner = "Enemy Army"
            result_color = "red"
        else:
            winner = "Unknown"
            result_color = "black"

        for widget in graph_holder.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
        ax.axvline(B_breakpoint, color='blue', linestyle='--', linewidth=1.8, label=f'Friendly termination at B = {B_breakpoint:.1f}')
        ax.axhline(R_breakpoint, color='red', linestyle='--', linewidth=1.8, label=f'Enemy termination at R = {R_breakpoint:.1f}')
        ax.scatter(B0, R0, s=70, color='black', label=f'Initial Point ({B0}, {R0})', zorder=4)
        ax.set_xlabel('Blue Strength (B)')
        ax.set_ylabel('Red Strength (R)')
        ax.set_title('A‑Rule Termination Thresholds')
        ax.set_xlim(0, max(B0, B_breakpoint) * 1.1)
        ax.set_ylim(0, max(R0, R_breakpoint) * 1.1)
        ax.grid(True, linestyle=':', linewidth=0.7)
        ax.legend(loc='upper left', fontsize=9, frameon=True)

        canvas = FigureCanvasTkAgg(fig, master=graph_holder)
        canvas.draw()
        canvas.get_tk_widget().pack()

        insights = (
            f"⏱️ Time of Termination: {round(t, 2)} units\n"
            f"🔵 Friendly Breakpoint: {fb} × B₀ = {round(B_breakpoint, 2)}\n"
            f"🔴 Enemy Breakpoint: {fr} × R₀ = {round(R_breakpoint, 2)}\n"
            f"💪 Final Friendly Strength: {round(Bf, 2)}\n"
            f"💪 Final Enemy Strength: {round(Rf, 2)}\n"
            f"🏳️ Winner: {winner}"
        )

        Label(graph_holder, text=insights.strip(), bg=BG_COLOR, font=("Helvetica", 12, "bold"),
              fg=result_color, justify=LEFT).pack(pady=(10, 0), anchor='w')

    def a_rule_submit_button():
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) == 10:
                widget.grid_forget()
        for widget in graph_holder.winfo_children():
            widget.destroy()

        try:
            B0_val = a_B0_entry.get()
            R0_val = a_R0_entry.get()
            beta_val = a_beta_entry.get()
            gamma_val = a_gamma_entry.get()
            fb_val = a_fb_entry.get()
            fr_val = a_fr_entry.get()

            if not (B0_val.isdigit() and R0_val.isdigit()):
                raise TypeError("IntegralError")

            B0 = int(B0_val)
            R0 = int(R0_val)
            beta = float(beta_val)
            gamma = float(gamma_val)
            fb = float(fb_val)
            fr = float(fr_val)

            if B0 == 0 or R0 == 0:
                raise ZeroDivisionError("ZeroStrength")

            if B0 < 0 or R0 < 0 or beta <= 0 or gamma <= 0 or not (0 < fb < 1) or not (0 < fr < 1):
                raise ValueError("NegativeOrInvalid")

            a_rule_simulation(B0, R0, beta, gamma, fb, fr)

        except TypeError:
            Label(left_frame, text="❌ Invalid Input (Positive Integral Values Only)", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=10, column=0, columnspan=2)
        except ZeroDivisionError:
            Label(left_frame, text="❌ Invalid Input (Initial Strength can't be 0)", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=10, column=0, columnspan=2)
        except ValueError:
            Label(left_frame, text="❌ Invalid Input (Negative or illogical values)", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=10, column=0, columnspan=2)

    def set_blue_win():
        a_B0_entry.delete(0, END)
        a_B0_entry.insert(0, "600")
        a_R0_entry.delete(0, END)
        a_R0_entry.insert(0, "300")
        a_beta_entry.delete(0, END)
        a_beta_entry.insert(0, "0.1")
        a_gamma_entry.delete(0, END)
        a_gamma_entry.insert(0, "0.2")
        a_fb_entry.delete(0, END)
        a_fb_entry.insert(0, "0.3")
        a_fr_entry.delete(0, END)
        a_fr_entry.insert(0, "0.2")

    def set_red_win():
        a_B0_entry.delete(0, END)
        a_B0_entry.insert(0, "400")
        a_R0_entry.delete(0, END)
        a_R0_entry.insert(0, "500")
        a_beta_entry.delete(0, END)
        a_beta_entry.insert(0, "0.2")
        a_gamma_entry.delete(0, END)
        a_gamma_entry.insert(0, "0.1")
        a_fb_entry.delete(0, END)
        a_fb_entry.insert(0, "0.2")
        a_fr_entry.delete(0, END)
        a_fr_entry.insert(0, "0.3")

    def set_equal_match():
        a_B0_entry.delete(0, END)
        a_B0_entry.insert(0, "500")
        a_R0_entry.delete(0, END)
        a_R0_entry.insert(0, "500")
        a_beta_entry.delete(0, END)
        a_beta_entry.insert(0, "0.1")
        a_gamma_entry.delete(0, END)
        a_gamma_entry.insert(0, "0.1")
        a_fb_entry.delete(0, END)
        a_fb_entry.insert(0, "0.3")
        a_fr_entry.delete(0, END)
        a_fr_entry.insert(0, "0.3")

    A_rule_window = Toplevel()
    A_rule_window.title("Combat Termination: A-Rule")
    window_width = 1250
    window_height = 810
    screen_width = A_rule_window.winfo_screenwidth()
    screen_height = A_rule_window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    A_rule_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    A_rule_window.resizable(False, False)
    A_rule_window.configure(bg=BG_COLOR)
    A_rule_window.bind("<Escape>", lambda e: A_rule_window.destroy())

    global left_frame, right_frame, graph_holder
    left_frame = Frame(A_rule_window, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=30, pady=20, sticky=N)

    right_frame = Frame(A_rule_window, bg=BG_COLOR)
    right_frame.grid(row=0, column=1, padx=10, pady=20, sticky=N)

    Label(left_frame, text="📘 A‑Rule: Combat Termination", font=FONT_TITLE, bg=BG_COLOR, fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "ARule.png")
    img = Image.open(image_path)
    img = img.resize((480, 350), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    image_label = Label(left_frame, image=photo, bg=BG_COLOR)
    image_label.image = photo
    image_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))
    image_label.bind("<Button-1>", lambda e: show_full_image())
    image_label.config(cursor="hand2")

    Label(left_frame, text="⚠️ Recommended values are pre-filled below. You can change them as per your needs.",
          font=("Helvetica", 10, "bold"), fg="red", bg=BG_COLOR, justify=LEFT).grid(row=3, column=0, columnspan=2, sticky=W, pady=(0, 15))

    entries = []
    input_fields = [
        ("Initial Friendly Strength (B₀):", 4, "500"),
        ("Initial Enemy Strength (R₀):", 5, "400"),
        ("Effectiveness of Enemy (β):", 6, "0.1"),
        ("Effectiveness of Friendly (γ):", 7, "0.2"),
        ("Breakpoint Fraction for Friendly (f_b):", 8, "0.3"),
        ("Breakpoint Fraction for Enemy (fᵣ):", 9, "0.2"),
    ]
    for text, row, default in input_fields:
        Label(left_frame, text=text, font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky=W, pady=5)
        entry = Entry(left_frame, width=30, font=FONT_NORMAL)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entries.append(entry)

    a_B0_entry, a_R0_entry, a_beta_entry, a_gamma_entry, a_fb_entry, a_fr_entry = entries

    Button(left_frame, text="Simulate Battle", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_NORMAL,
           command=a_rule_submit_button, padx=20, pady=5).grid(row=11, column=0, pady=15, sticky=W)

    Button(left_frame, text="Exit", bg="crimson", fg="white", font=FONT_NORMAL,
           command=A_rule_window.destroy, padx=20, pady=5).grid(row=11, column=1, pady=15, sticky=E)

    graph_holder = Frame(right_frame, bg=BG_COLOR)
    graph_holder.pack(fill=BOTH, expand=True)

    Label(right_frame, text="🎯 Choose one of the recommended value sets from the buttons below:", bg=BG_COLOR,
          font=("Helvetica", 12, "bold"), fg="#333").pack(pady=(10, 5))

    button_holder = Frame(right_frame, bg=BG_COLOR)
    button_holder.pack(pady=10)


    Button(button_holder, text="🔵 Blue's Victory", bg="blue", fg="white",
           font=("Helvetica", 10, "bold"), command=set_blue_win, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="🔴 Red's Victory", bg="red", fg="white",
           font=("Helvetica", 10, "bold"), command=set_red_win, padx=10, pady=5).pack(side=LEFT, padx=8)

    Button(button_holder, text="⚖️ Equal Match", bg="#008080", fg="white",
           font=("Helvetica", 10, "bold"), command=set_equal_match, padx=10, pady=5).pack(side=LEFT, padx=8)


def P_rule_termination():
    def show_full_image():
        top = Toplevel(P_rule_window)
        top.title("Full Image - P-Rule")

        full_img = Image.open(image_path)
        photo_full = ImageTk.PhotoImage(full_img)

        lbl = Label(top, image=photo_full, bg="white")
        lbl.image = photo_full
        lbl.pack()

        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        img_width, img_height = full_img.size
        x = (screen_width // 2) - (img_width // 2)
        y = (screen_height // 2) - (img_height // 2)
        top.geometry(f"{img_width}x{img_height}+{x}+{y}")

    def p_rule_simulation(E0, F0, beta, gamma, kr, kb):
        R = E0  # Enemy
        B = F0  # Friendly
        t = 0
        dt = 0.1
        time = []
        R_vals = []
        B_vals = []

        winner = None
        while R > 0 and B > 0:
            time.append(t)
            R_vals.append(R / E0)
            B_vals.append(B / F0)

            dR = -gamma * B * dt
            dB = -beta * R * dt

            R = max(0, R + dR)
            B = max(0, B + dB)
            t += dt

            if B > 0:
                ratio = R / B
                if ratio <= kr:
                    winner = "Friendly Army"
                    break
                elif ratio >= kb:
                    winner = "Enemy Army"
                    break

            if t > 1000:
                winner = "No Termination (Timed Out)"
                break

        Rf = max(0, R)
        Bf = max(0, B)

        global graph_holder
        for widget in graph_holder.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
        xmax = max(F0 * 1.2, 100)
        ymax = max(E0 * 1.2, 100)
        x = np.linspace(0, xmax, 300)
        y_enemy_loses = kr * x
        y_friendly_loses = kb * x

        ax.fill_between(x, 0, y_enemy_loses, color='blue', alpha=0.2, label='Enemy Loses Region (R/B ≤ kᵣ)')
        ax.fill_between(x, y_friendly_loses, ymax, color='red', alpha=0.2, label='Friendly Loses Region (R/B ≥ kᵦ)')
        ax.plot(x, y_enemy_loses, linestyle='--', color='blue', linewidth=2, label=f'R = {kr:.2f} × B')
        ax.plot(x, y_friendly_loses, linestyle='--', color='red', linewidth=2, label=f'R = {kb:.2f} × B')
        ax.scatter(F0, E0, s=70, color='black', label=f'Initial Point ({F0}, {E0})')

        ax.set_xlabel('Friendly Strength (B)')
        ax.set_ylabel('Enemy Strength (R)')
        ax.set_title('P‑Rule Termination Thresholds')
        ax.set_xlim(0, xmax)
        ax.set_ylim(0, ymax)
        ax.grid(True, linestyle=':', linewidth=0.7)
        ax.legend(loc='upper left', fontsize=9)

        canvas = FigureCanvasTkAgg(fig, master=graph_holder)
        canvas.draw()
        canvas.get_tk_widget().pack()

        result_color = "blue" if winner == "Friendly Army" else "red" if winner == "Enemy Army" else "#008080"

        insights = (
            f"⏱️ Termination Time: {round(t, 2)}\n"
            f"📉 R/B Ratio at Termination: {round(R / B, 2) if B != 0 else '∞'}\n"
            f"⚖️ Thresholds → Enemy loses if R/B ≤ {kr}, Friendly loses if R/B ≥ {kb}\n"
            f"💪 Final Friendly Strength: {round(Bf, 2)}\n"
            f"💪 Final Enemy Strength: {round(Rf, 2)}\n"
            f"🏳️ Winner: {winner}"
        )

        Label(graph_holder, text=insights.strip(), bg=BG_COLOR, font=("Helvetica", 12, "bold"),
              fg=result_color, justify=LEFT).pack(pady=(10, 0), anchor='w')

    def p_rule_submit_button():
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) == 11:
                widget.grid_forget()
        for widget in graph_holder.winfo_children():
            widget.destroy()

        try:
            E0_input = p_R0_entry.get()
            F0_input = p_B0_entry.get()
            beta_input = p_beta_entry.get()
            gamma_input = p_gamma_entry.get()
            kr_input = p_kr_entry.get()
            kb_input = p_kb_entry.get()

            if not (E0_input.isdigit() and F0_input.isdigit()):
                raise TypeError("IntegralError")

            E0 = int(E0_input)
            F0 = int(F0_input)
            beta = float(beta_input)
            gamma = float(gamma_input)
            kr = float(kr_input)
            kb = float(kb_input)

            if E0 == 0 or F0 == 0:
                raise ZeroDivisionError("ZeroStrength")
            if E0 < 0 or F0 < 0 or beta <= 0 or gamma <= 0 or kr <= 0 or kb <= 0:
                raise ValueError("NegativeOrInvalid")
            if kr >= kb:
                raise ValueError("❌ Invalid Input (Enemy threshold kᵣ must be less than Friendly threshold kᵦ)")

            p_rule_simulation(E0, F0, beta, gamma, kr, kb)

        except TypeError:
            Label(left_frame, text="❌ Invalid Input (Positive Integral Values Only)", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red", wraplength=400, justify=LEFT).grid(row=11, column=0, columnspan=2)
        except ZeroDivisionError:
            Label(left_frame, text="❌ Invalid Input (Initial Strength can't be 0)", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red", wraplength=400, justify=LEFT).grid(row=11, column=0, columnspan=2)
        except ValueError as ve:
            Label(left_frame, text=str(ve), bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red", wraplength=400, justify=LEFT).grid(row=11, column=0, columnspan=2)

    # === GUI Setup ===
    P_rule_window = Toplevel()
    P_rule_window.title("Combat Termination: P-Rule (Ratio-Based)")
    window_width = 1250
    window_height = 810
    screen_width = P_rule_window.winfo_screenwidth()
    screen_height = P_rule_window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    P_rule_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    P_rule_window.configure(bg=BG_COLOR)
    P_rule_window.bind("<Escape>", lambda e: P_rule_window.destroy())

    global left_frame, right_frame, graph_holder
    left_frame = Frame(P_rule_window, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=30, pady=20, sticky=N)
    right_frame = Frame(P_rule_window, bg=BG_COLOR)
    right_frame.grid(row=0, column=1, padx=10, pady=20, sticky=N)

    Label(left_frame, text="📘 P‑Rule: Ratio-Based Termination", font=FONT_TITLE, bg=BG_COLOR, fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "PRule.png")
    img = Image.open(image_path)
    img = img.resize((480, 350), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    image_label = Label(left_frame, image=photo, bg=BG_COLOR)
    image_label.image = photo
    image_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))
    image_label.bind("<Button-1>", lambda e: show_full_image())
    image_label.config(cursor="hand2")

    Label(left_frame, text="⚠️ Recommended values are pre-filled below. You can change them as per your needs.",
          font=("Helvetica", 10, "bold"), fg="red", bg=BG_COLOR, justify=LEFT).grid(row=3, column=0, columnspan=2, sticky=W, pady=(0, 1))

    entries = []
    input_fields = [
    ("Initial Friendly Strength (B₀):", 4, "600"),
    ("Initial Enemy Strength (R₀):", 5, "400"),
    ("Effectiveness of Enemy (Beta):", 6, "0.2"),
    ("Effectiveness of Friendly (Gamma):", 7, "0.1"),
    ("Enemy Loss Ratio Threshold (kᵣ):", 8, "0.5"),
    ("Friendly Loss Ratio Threshold (kᵦ):", 9, "1.5")
    ]

    for text, row, default in input_fields:
        Label(left_frame, text=text, font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky=W, pady=5)
        entry = Entry(left_frame, width=30, font=FONT_NORMAL)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entries.append(entry)

    p_R0_entry, p_B0_entry, p_beta_entry, p_gamma_entry, p_kr_entry, p_kb_entry = entries

    Button(left_frame, text="Simulate Battle", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_NORMAL,
           command=p_rule_submit_button, padx=20, pady=5).grid(row=10, column=0, pady=15, sticky=W)
    Button(left_frame, text="Exit", bg="crimson", fg="white", font=FONT_NORMAL,
           command=P_rule_window.destroy, padx=20, pady=5).grid(row=10, column=1, pady=15, sticky=E)

    graph_holder = Frame(right_frame, bg=BG_COLOR)
    graph_holder.pack(fill=BOTH, expand=True)

    Label(right_frame, text="🎯 Choose one of the recommended value sets from the buttons below:", bg=BG_COLOR,
          font=("Helvetica", 12, "bold"), fg="#333").pack(pady=(10, 5))

    def set_enemy_win():
        p_R0_entry.delete(0, END)
        p_R0_entry.insert(0, "500")
        p_B0_entry.delete(0, END)
        p_B0_entry.insert(0, "400")
        p_beta_entry.delete(0, END)
        p_beta_entry.insert(0, "0.2")
        p_gamma_entry.delete(0, END)
        p_gamma_entry.insert(0, "0.1")
        p_kr_entry.delete(0, END)
        p_kr_entry.insert(0, "0.5")
        p_kb_entry.delete(0, END)
        p_kb_entry.insert(0, "1.5")

    def set_friendly_win():
        p_R0_entry.delete(0, END)
        p_R0_entry.insert(0, "300")
        p_B0_entry.delete(0, END)
        p_B0_entry.insert(0, "600")
        p_beta_entry.delete(0, END)
        p_beta_entry.insert(0, "0.1")
        p_gamma_entry.delete(0, END)
        p_gamma_entry.insert(0, "0.2")
        p_kr_entry.delete(0, END)
        p_kr_entry.insert(0, "0.4")
        p_kb_entry.delete(0, END)
        p_kb_entry.insert(0, "1.3")

    def set_equal_match():
        p_R0_entry.delete(0, END)
        p_R0_entry.insert(0, "500")
        p_B0_entry.delete(0, END)
        p_B0_entry.insert(0, "500")
        p_beta_entry.delete(0, END)
        p_beta_entry.insert(0, "0.1")
        p_gamma_entry.delete(0, END)
        p_gamma_entry.insert(0, "0.1")
        p_kr_entry.delete(0, END)
        p_kr_entry.insert(0, "0.9")
        p_kb_entry.delete(0, END)
        p_kb_entry.insert(0, "1.1")

    button_holder = Frame(right_frame, bg=BG_COLOR)
    button_holder.pack(pady=10)

    Button(button_holder, text="🔵 Blue's Victory", bg="blue", fg="white",
           font=("Helvetica", 10, "bold"), command=set_friendly_win, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="🔴 Red's Victory", bg="red", fg="white",
           font=("Helvetica", 10, "bold"), command=set_enemy_win, padx=10, pady=5).pack(side=LEFT, padx=8)

    Button(button_holder, text="⚖️ Equal Match", bg="teal", fg="white",
           font=("Helvetica", 10, "bold"), command=set_equal_match, padx=10, pady=5).pack(side=LEFT, padx=8)


def helmbold_advantage():
    def show_full_image():
        top = Toplevel(Helmbold_Window)
        top.title("Full Image - Helmbold's Law")

        full_img = Image.open(image_path)
        photo_full = ImageTk.PhotoImage(full_img)

        lbl = Label(top, image=photo_full, bg="white")
        lbl.image = photo_full
        lbl.pack()

        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        img_width, img_height = full_img.size
        x = (screen_width // 2) - (img_width // 2)
        y = (screen_height // 2) - (img_height // 2)
        top.geometry(f"{img_width}x{img_height}+{x}+{y}")

    def plot_helmbold_graph(B0, R0, Bf, Rf, parent_frame):
        blue_loss = (B0 - Bf) / B0 if B0 else 0
        red_loss  = (R0 - Rf) / R0 if R0 else 0
        steps = 100

        t_vals = [i / steps for i in range(steps + 1)]
        blue_interp = [i * blue_loss / steps for i in range(steps + 1)]
        red_interp  = [i * red_loss  / steps for i in range(steps + 1)]

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

        if abs(red_loss - blue_loss) < 1e-6:
            ax.plot(t_vals, blue_interp, label="Equal Loss (Blue & Red)", color="#008080")
        else:
            ax.plot(t_vals, blue_interp, label="Blue Loss (Normalised)", color="blue")
            ax.plot(t_vals, red_interp, label="Red Loss (Normalised)", color="red")

        ax.set_xlabel("Progress of Battle (time)")
        ax.set_ylabel("Normalised Loss")
        ax.set_title("Helmbold Advantage – Loss Comparison")
        ax.legend()
        ax.grid(True)
        fig.tight_layout()

        global graph_holder
        for widget in graph_holder.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=graph_holder)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def compute_helmbold(B0, R0, Bf, Rf):
        global result_holder

        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) >= 11:
                widget.grid_forget()

        for widget in result_holder.winfo_children():
            widget.destroy()

        blue_loss = (B0 - Bf) / B0
        red_loss  = (R0 - Rf) / R0

        if blue_loss == 0:
            Label(result_holder, text="⚠️ Blue suffered no loss → Advantage undefined",
                  bg=BG_COLOR, fg="darkred", font=FONT_NORMAL,
                  justify=LEFT, wraplength=600).pack(anchor=W)
            return

        FERb = red_loss / blue_loss
        Vb   = 0.5 * math.log(FERb) if FERb > 0 else float("-inf")

        if Vb > 0:
            interpretation = "✅ Blue had the advantage — inflicted more damage per own loss."
            colour = "blue"
        elif Vb < 0:
            interpretation = "✅ Red had the advantage — inflicted more damage per own loss."
            colour = "red"
        else:
            interpretation = "⚖️ No clear advantage — both suffered proportionally."
            colour = "#008080"

        legend_texts = [
            "🟩 Blue – Blue’s Advantage",
            "🟥 Red   – Red’s Advantage",
            "🟦 Teal  – Equal Match",
            ""
        ]
        for txt in legend_texts:
            Label(result_holder, text=txt, bg=BG_COLOR, fg="red",
                  font=("Helvetica", 10, "bold"),
                  justify=LEFT, wraplength=600).pack(anchor=W)

        explanation = (
            f"📉 Blue Loss = (B₀ − Bf) / B₀ = {blue_loss:.4f} → {blue_loss*100:.1f}%\n"
            f"📉 Red Loss  = (R₀ − Rf) / R₀ = {red_loss:.4f} → {red_loss*100:.1f}%\n"
            f"📊 FERᵦ = Red Loss / Blue Loss = {FERb:.4f}\n"
            f"📈 Vᵦ  = ½ ln(FERᵦ) = {Vb:.4f}\n\n"
            f"{interpretation}"
        )
        Label(result_holder, text=explanation, bg=BG_COLOR, fg=colour,
              font=("Helvetica", 13, "bold"),
              justify=LEFT, wraplength=600).pack(anchor=W)

        plot_helmbold_graph(B0, R0, Bf, Rf, right_frame)

    def submit_helmbold():
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) >= 11:
                widget.grid_forget()

        for widget in graph_holder.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()

        try:
            B0_input = h_B0_entry.get()
            R0_input = h_R0_entry.get()
            Bf_input = h_Bf_entry.get()
            Rf_input = h_Rf_entry.get()

            if not (R0_input.isdigit() and B0_input.isdigit() and Rf_input.isdigit() and Bf_input.isdigit()):
                raise TypeError("NonInteger")

            B0 = int(B0_input)
            R0 = int(R0_input)
            Bf = int(Bf_input)
            Rf = int(Rf_input)

            if B0 == 0 or R0 == 0:
                raise ZeroDivisionError("ZeroStrength")
            if B0 < 0 or R0 < 0 or Bf < 0 or Rf < 0:
                raise ValueError("Negative")
            if Bf > B0 or Rf > R0:
                raise ValueError("FinalExceedsInitial")

            compute_helmbold(B0, R0, Bf, Rf)

        except TypeError:
            for widget in graph_holder.winfo_children():
                widget.destroy()
            for widget in result_holder.winfo_children():
                widget.destroy()
            Label(left_frame, text="❌ Invalid Input (Positive Integral Values Only)", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=11, column=0, columnspan=2)

        except ZeroDivisionError:
            for widget in graph_holder.winfo_children():
                widget.destroy()
            for widget in result_holder.winfo_children():
                widget.destroy()
            Label(left_frame, text="❌ Invalid Input (Initial Strength can't be 0)", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=11, column=0, columnspan=2)

        except ValueError as ve:
            for widget in graph_holder.winfo_children():
                widget.destroy()
            for widget in result_holder.winfo_children():
                widget.destroy()
            if str(ve) == "Negative":
                msg = "❌ Invalid Input (Negative values not allowed)"
            elif str(ve) == "FinalExceedsInitial":
                msg = "❌ Final strength cannot exceed initial strength"
            else:
                msg = "❌ Invalid Input"
            Label(left_frame, text=msg, bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg="red").grid(row=11, column=0, columnspan=2)

    Helmbold_Window = Toplevel(bg=BG_COLOR)
    Helmbold_Window.title("Helmbold’s Advantage Parameter")
    window_width = 1250
    window_height = 810
    screen_width = Helmbold_Window.winfo_screenwidth()
    screen_height = Helmbold_Window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    Helmbold_Window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    Helmbold_Window.bind("<Escape>", lambda e: Helmbold_Window.destroy())

    global left_frame, right_frame, graph_holder
    left_frame = Frame(Helmbold_Window, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=30, pady=20, sticky=N)

    right_frame = Frame(Helmbold_Window, bg=BG_COLOR)
    right_frame.grid(row=0, column=1, padx=10, pady=20, sticky=N)

    Label(left_frame, text="📘 Helmbold’s Advantage Parameter", font=FONT_TITLE, bg=BG_COLOR, fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "HelmboldsAdvantageParameter.png")

    img = Image.open(image_path)
    img = img.resize((480, 350), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    image_label = Label(left_frame, image=photo, bg=BG_COLOR)
    image_label.image = photo
    image_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))
    image_label.bind("<Button-1>", lambda e: show_full_image())
    image_label.config(cursor="hand2")

    Label(left_frame, text="⚠️ Recommended values are pre-filled below. You can change them as per your needs.",
          font=("Helvetica", 10, "bold"), fg="red", bg=BG_COLOR, justify=LEFT).grid(row=3, column=0, columnspan=2, sticky=W, pady=(0, 15))

    entries = []
    input_fields = [
        ("Initial Blue Army (B₀):", 4, "300"),
        ("Initial Red Army (R₀):", 5, "100"),
        ("Final Blue Army (Bf):", 6, "150"),
        ("Final Red Army (Rf):", 7, "50"),
    ]
    for text, row, default in input_fields:
        Label(left_frame, text=text, font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky=W, pady=5)
        entry = Entry(left_frame, width=30, font=FONT_NORMAL)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entries.append(entry)

    h_B0_entry, h_R0_entry, h_Bf_entry, h_Rf_entry = entries

    Button(left_frame, text="🔍 Calculate", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_NORMAL,
           command=submit_helmbold, padx=20, pady=5).grid(row=9, column=0, pady=15, sticky=W)

    Button(left_frame, text="Exit", bg="crimson", fg="white", font=FONT_NORMAL,
           command=Helmbold_Window.destroy).grid(row=9, column=1, pady=15, sticky=E)

    graph_holder = Frame(right_frame, bg=BG_COLOR)
    graph_holder.pack(fill=BOTH, expand=True)

    global result_holder
    result_holder = Frame(right_frame, bg=BG_COLOR)
    result_holder.pack(fill=X, padx=10, pady=(0, 20))

    Label(right_frame, text="🎯 Choose one of the recommended value sets from the buttons below:", bg=BG_COLOR,
          font=("Helvetica", 12, "bold"), fg="#333").pack(pady=(10, 5))

    def set_blue_victory():
        h_B0_entry.delete(0, END)
        h_B0_entry.insert(0, "200")
        h_R0_entry.delete(0, END)
        h_R0_entry.insert(0, "200")
        h_Bf_entry.delete(0, END)
        h_Bf_entry.insert(0, "180")
        h_Rf_entry.delete(0, END)
        h_Rf_entry.insert(0, "40")

    def set_red_victory():
        h_B0_entry.delete(0, END)
        h_B0_entry.insert(0, "200")
        h_R0_entry.delete(0, END)
        h_R0_entry.insert(0, "200")
        h_Bf_entry.delete(0, END)
        h_Bf_entry.insert(0, "30")
        h_Rf_entry.delete(0, END)
        h_Rf_entry.insert(0, "160")

    def set_equal_match():
        h_B0_entry.delete(0, END)
        h_B0_entry.insert(0, "300")
        h_R0_entry.delete(0, END)
        h_R0_entry.insert(0, "100")
        h_Bf_entry.delete(0, END)
        h_Bf_entry.insert(0, "150")
        h_Rf_entry.delete(0, END)
        h_Rf_entry.insert(0, "50")

    button_holder = Frame(right_frame, bg=BG_COLOR)
    button_holder.pack(side=BOTTOM, pady=10)

    Button(button_holder, text="🔵 Blue's Victory", bg="blue", fg="white",
           font=("Helvetica", 10, "bold"), command=set_blue_victory, padx=10, pady=5).pack(side=LEFT, padx=8)

    Button(button_holder, text="🔴 Red's Victory", bg="red", fg="white",
           font=("Helvetica", 10, "bold"), command=set_red_victory, padx=10, pady=5).pack(side=LEFT, padx=8)

    Button(button_holder, text="⚖️ Equal Match", bg="#008080", fg="white",
           font=("Helvetica", 10, "bold"), command=set_equal_match, padx=10, pady=5).pack(side=LEFT, padx=8)


def force_elasticity():
    def show_full_image():
        top = Toplevel(Elasticity_Window)
        top.title("Full Image - Force Elasticity")

        full_img = Image.open(image_path)
        photo_full = ImageTk.PhotoImage(full_img)

        lbl = Label(top, image=photo_full, bg="white")
        lbl.image = photo_full
        lbl.pack()

        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        img_width, img_height = full_img.size

        x = (screen_width // 2) - (img_width // 2)
        y = (screen_height // 2) - (img_height // 2)
        top.geometry(f"{img_width}x{img_height}+{x}+{y}")

    def plot_elasticity_graph(B1, B2, R1, R2, parent_frame):
        blue_loss = (B1 - B2) / B1
        red_loss = (R1 - R2) / R1
        steps = 100
        t_vals = [i / steps for i in range(steps + 1)]
        blue_interp = [i * blue_loss / steps for i in range(steps + 1)]
        red_interp = [i * red_loss / steps for i in range(steps + 1)]

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        if abs(blue_loss - red_loss) < 1e-6:
            ax.plot(t_vals, blue_interp, label="Equal Loss (Blue & Red)", color="#008080")
        else:
            ax.plot(t_vals, blue_interp, label="Blue Loss (Normalized)", color="blue")
            ax.plot(t_vals, red_interp, label="Red Loss (Normalized)", color="red")

        ax.set_xlabel("Progress of Battle (Time)")
        ax.set_ylabel("Normalized Loss")
        ax.set_title("Force Elasticity Loss Comparison")
        ax.legend()
        ax.grid(True)
        fig.tight_layout()

        for widget in graph_holder.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=graph_holder)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def compute_elasticity(B1, B2, R1, R2):
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) >= 11:
                widget.grid_forget()

        for widget in result_holder.winfo_children():
            widget.destroy()

        dB_by_B = (B1 - B2) / B1 if B1 != 0 else 0
        dR_by_R = (R1 - R2) / R1 if R1 != 0 else 0

        if dB_by_B == 0:
            Label(result_holder, text="⚠️ Blue suffered no loss → Elasticity undefined", bg=BG_COLOR,
                  font=FONT_NORMAL, fg="darkred", wraplength=600, justify=LEFT).pack(anchor=W)
            return

        eps_b = dR_by_R / dB_by_B
        u = math.sqrt(eps_b) if eps_b >= 0 else float('nan')

        if eps_b > 1:
            interpretation = "🔵 Blue is more effective — Red is losing faster."
            color = "blue"
        elif eps_b < 1:
            interpretation = "🔴 Red is more effective — Blue is losing faster."
            color = "red"
        else:
            interpretation = "⚖️ Both sides are equally effective."
            color = "#008080"

        legend_texts = [
            "🟦 Blue – Blue’s Effectiveness",
            "🟥 Red  – Red’s Effectiveness",
            "🟦 Teal  – Equal Match",
            ""
        ]
        for txt in legend_texts:
            Label(result_holder, text=txt, bg=BG_COLOR, fg="red",
                  font=("Helvetica", 10, "bold"),
                  justify=LEFT, wraplength=600).pack(anchor=W)

        explanation = (
            f"📉 Blue Loss = (B₁ − B₂) / B₁ = {dB_by_B:.4f} → {dB_by_B*100:.1f}%\n"
            f"📉 Red Loss  = (R₁ − R₂) / R₁ = {dR_by_R:.4f} → {dR_by_R*100:.1f}%\n"
            f"📊 ε_b = Red Loss / Blue Loss = {eps_b:.4f}\n"
            f"📈 √ε_b (u) = {u:.4f}\n\n"
            f"{interpretation}"
        )
        Label(result_holder, text=explanation, bg=BG_COLOR, font=("Helvetica", 13, "bold"), fg=color,
              justify=LEFT, wraplength=600).pack(anchor=W)

        plot_elasticity_graph(B1, B2, R1, R2, graph_holder)

    def submit_elasticity():
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) >= 11:
                widget.grid_forget()
        for widget in graph_holder.winfo_children():
            widget.destroy()
        for widget in result_holder.winfo_children():
            widget.destroy()

        try:
            B1_input = f_B1_entry.get()
            B2_input = f_B2_entry.get()
            R1_input = f_R1_entry.get()
            R2_input = f_R2_entry.get()

            if not (B1_input.isdigit() and B2_input.isdigit() and R1_input.isdigit() and R2_input.isdigit()):
                raise TypeError("NonInteger")

            B1 = int(B1_input)
            B2 = int(B2_input)
            R1 = int(R1_input)
            R2 = int(R2_input)

            if B1 == 0 or R1 == 0:
                raise ZeroDivisionError("ZeroStrength")
            if B1 < 0 or B2 < 0 or R1 < 0 or R2 < 0:
                raise ValueError("Negative")
            if B2 > B1 or R2 > R1:
                raise ValueError("FinalExceedsInitial")

            compute_elasticity(B1, B2, R1, R2)

        except TypeError:
            Label(left_frame, text="❌ Invalid Input (Positive Integral Values Only)", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=11, column=0, columnspan=2)

        except ZeroDivisionError:
            Label(left_frame, text="❌ Invalid Input (Initial Strength can't be 0)", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=11, column=0, columnspan=2)

        except ValueError as ve:
            msg = {
                "Negative": "❌ Invalid Input (Negative values not allowed)",
                "FinalExceedsInitial": "❌ Final strength cannot exceed initial strength"
            }.get(str(ve), "❌ Invalid Input")
            Label(left_frame, text=msg, bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg="red").grid(row=11, column=0, columnspan=2)

    # === GUI Setup ===
    Elasticity_Window = Toplevel(bg=BG_COLOR)
    Elasticity_Window.title("Force Elasticity - Measure of Combat Success")
    window_width = 1250
    window_height = 810
    screen_width = Elasticity_Window.winfo_screenwidth()
    screen_height = Elasticity_Window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    Elasticity_Window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    Elasticity_Window.bind("<Escape>", lambda e: Elasticity_Window.destroy())

    global left_frame, right_frame, graph_holder, result_holder
    left_frame = Frame(Elasticity_Window, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=30, pady=20, sticky=N)

    right_frame = Frame(Elasticity_Window, bg=BG_COLOR)
    right_frame.grid(row=0, column=1, padx=10, pady=20, sticky=N)

    Label(left_frame, text="📘 Force Elasticity (εᵦ)", font=FONT_TITLE, bg=BG_COLOR, fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "ForceElasticity.png")
    img = Image.open(image_path).resize((480, 400), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    image_label = Label(left_frame, image=photo, bg=BG_COLOR)
    image_label.image = photo
    image_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))
    image_label.bind("<Button-1>", lambda e: show_full_image())
    image_label.config(cursor="hand2")

    Label(left_frame, text="⚠️ Recommended values are pre-filled below. You can change them as per your needs.",
          font=("Helvetica", 10, "bold"), fg="red", bg=BG_COLOR, justify=LEFT).grid(row=3, column=0, columnspan=2, sticky=W, pady=(0, 15))

    entries = []
    input_fields = [
        ("Blue Force at Time 1 (B₁):", 4, "300"),
        ("Blue Force at Time 2 (B₂):", 5, "150"),
        ("Red Force at Time 1 (R₁):", 6, "100"),
        ("Red Force at Time 2 (R₂):", 7, "50"),
    ]
    for text, row, default in input_fields:
        Label(left_frame, text=text, font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky=W, pady=5)
        entry = Entry(left_frame, width=30, font=FONT_NORMAL)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entries.append(entry)

    f_B1_entry, f_B2_entry, f_R1_entry, f_R2_entry = entries

    Button(left_frame, text="🔍 Calculate", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_NORMAL,
           command=submit_elasticity, padx=20, pady=5).grid(row=9, column=0, pady=15, sticky=W)
    Button(left_frame, text="❌ Exit", bg="crimson", fg="white", font=FONT_NORMAL,
           command=Elasticity_Window.destroy).grid(row=9, column=1, pady=15, sticky=E)

    graph_holder = Frame(right_frame, bg=BG_COLOR)
    graph_holder.pack(fill=BOTH, expand=True)
    result_holder = Frame(right_frame, bg=BG_COLOR)
    result_holder.pack(fill=X, padx=10, pady=(0, 20))

    Label(right_frame, text="🎯 Choose one of the recommended value sets from the buttons below:", bg=BG_COLOR,
          font=("Helvetica", 12, "bold"), fg="#333").pack(pady=(10, 5))

    def set_blue_effective():
        f_B1_entry.delete(0, END); f_B1_entry.insert(0, "200")
        f_B2_entry.delete(0, END); f_B2_entry.insert(0, "180")
        f_R1_entry.delete(0, END); f_R1_entry.insert(0, "200")
        f_R2_entry.delete(0, END); f_R2_entry.insert(0, "40")

    def set_red_effective():
        f_B1_entry.delete(0, END); f_B1_entry.insert(0, "200")
        f_B2_entry.delete(0, END); f_B2_entry.insert(0, "30")
        f_R1_entry.delete(0, END); f_R1_entry.insert(0, "200")
        f_R2_entry.delete(0, END); f_R2_entry.insert(0, "160")

    def set_equal_effective():
        f_B1_entry.delete(0, END); f_B1_entry.insert(0, "300")
        f_B2_entry.delete(0, END); f_B2_entry.insert(0, "150")
        f_R1_entry.delete(0, END); f_R1_entry.insert(0, "100")
        f_R2_entry.delete(0, END); f_R2_entry.insert(0, "50")

    button_holder = Frame(right_frame, bg=BG_COLOR)
    button_holder.pack(side=BOTTOM, pady=10)

    Button(button_holder, text="🔵 Blue Effective", bg="blue", fg="white",
           font=("Helvetica", 10, "bold"), command=set_blue_effective, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="🔴 Red Effective", bg="red", fg="white",
           font=("Helvetica", 10, "bold"), command=set_red_effective, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="⚖️ Equal Match", bg="#008080", fg="white",
           font=("Helvetica", 10, "bold"), command=set_equal_effective, padx=10, pady=5).pack(side=LEFT, padx=8)


def barr_battle_trace():
    def show_full_image():
        top = Toplevel(trace_window)
        top.title("Full Image - Barr's Battle Trace")

        full_img = Image.open(image_path)
        photo_full = ImageTk.PhotoImage(full_img)

        lbl = Label(top, image=photo_full, bg="white")
        lbl.image = photo_full
        lbl.pack()

        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        img_width, img_height = full_img.size

        x = (screen_width // 2) - (img_width // 2)
        y = (screen_height // 2) - (img_height // 2)
        top.geometry(f"{img_width}x{img_height}+{x}+{y}")

    def plot_trace_graph(B0, R0, Bt, Rt, parent_frame):
        for widget in parent_frame.winfo_children():
            widget.destroy()

        blue_remaining = Bt / B0
        red_remaining = Rt / R0

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.bar(["Blue (Friendly)", "Red (Enemy)"], [blue_remaining, red_remaining], color=["blue", "red"])
        ax.set_ylabel("Normalized Force Remaining")
        ax.set_title("Force Remaining at Time t")
        ax.set_ylim(0, 1.1)
        ax.grid(axis='y')
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def compute_trace(B0, R0, Bf, Rf, Bt, Rt):
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) >= 11:
                widget.grid_forget()
        for widget in result_holder.winfo_children():
            widget.destroy()

        delta_B = B0 - Bt
        delta_R = R0 - Rt
        blue_loss_f = B0 - Bf
        red_loss_f = R0 - Rf

        if delta_R == 0 or delta_B == 0 or Bt > B0 or Rt > R0 or Bt < 0 or Rt < 0:
            Label(left_frame, text="⚠️ Invalid combat snapshot or final loss values", bg=BG_COLOR,
                  font=FONT_NORMAL, fg="darkred", wraplength=500, justify=LEFT).grid(row=11, column=0, columnspan=2, sticky=W)
            return

        numerator = delta_B * red_loss_f
        denominator = delta_R * blue_loss_f
        T = numerator / denominator if denominator != 0 else float('inf')

        if T < 1:
            interp = "🔵 Blue (friendly attacker) is performing better."
            color = "blue"
        elif T > 1:
            interp = "🔴 Blue (friendly attacker) is performing worse."
            color = "red"
        else:
            interp = "⚖️ Both sides are equally effective."
            color = "#008080"

        explanation = (
            f"📊 Total Blue Loss (ΔB) = B₀ - B(t) = {delta_B}\n"
            f"📊 Total Red Loss (ΔR) = R₀ - R(t) = {delta_R}\n\n"
            f"📉 Blue loss at time t = B₀ - Bf = {blue_loss_f}\n"
            f"📉 Red loss at time t = R₀ - Rf = {red_loss_f}\n\n"
            f"📐 T = (ΔR × BlueLossₜ) / (ΔB × RedLossₜ) = {round(T, 4)}\n\n"
            f"{interp}"
        )

        Label(result_holder, text="📌 Interpretation", font=("Helvetica", 10, "bold"), bg=BG_COLOR, fg="black").pack(anchor=W)
        Label(result_holder, text=explanation, bg=BG_COLOR, font=("Helvetica", 13, "bold"), fg=color,
              wraplength=600, justify=LEFT).pack(anchor=W)

        plot_trace_graph(B0, R0, Bt, Rt, graph_holder)

    def submit_trace():
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) >= 11:
                widget.grid_forget()
        for widget in graph_holder.winfo_children():
            widget.destroy()
        for widget in result_holder.winfo_children():
            widget.destroy()

        try:
            B0 = float(t_B0_entry.get())
            R0 = float(t_R0_entry.get())
            Bf = float(t_Bf_entry.get())
            Rf = float(t_Rf_entry.get())
            Bt = float(t_Bt_entry.get())
            Rt = float(t_Rt_entry.get())

            if not all(x.is_integer() for x in [B0, R0, Bf, Rf, Bt, Rt]):
                raise ValueError("Decimal")
            B0, R0, Bf, Rf, Bt, Rt = map(int, [B0, R0, Bf, Rf, Bt, Rt])

            if any(x < 0 for x in [B0, R0, Bf, Rf, Bt, Rt]):
                raise ValueError("Negative")
            if Bf > B0 or Rf > R0 or Bt > B0 or Rt > R0:
                raise ValueError("Exceed")

            compute_trace(B0, R0, Bf, Rf, Bt, Rt)

        except ValueError as ve:
            msg = {
                "Negative": "❌ Invalid Input (Negative values not allowed)",
                "Exceed": "❌ Final or intermediate values can't exceed initial values",
                "Decimal": "❌ Invalid Input (Decimal values not allowed — use integers only)"
            }.get(str(ve), "❌ Invalid Input")
            Label(left_frame, text=msg, bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg="red").grid(row=11, column=0, columnspan=2)
        except:
            Label(left_frame, text="❌ Invalid Input (Positive integers only)", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red").grid(row=11, column=0, columnspan=2)

    trace_window = Toplevel(bg=BG_COLOR)
    trace_window.title("Barr’s Battle Trace - Combat Snapshot Analysis")
    window_width = 1250
    window_height = 810
    center_x = int(trace_window.winfo_screenwidth() / 2 - window_width / 2)
    center_y = int(trace_window.winfo_screenheight() / 2 - window_height / 2)
    trace_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    trace_window.bind("<Escape>", lambda e: trace_window.destroy())

    global left_frame, right_frame, graph_holder, result_holder
    left_frame = Frame(trace_window, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=30, pady=20, sticky=N)

    right_frame = Frame(trace_window, bg=BG_COLOR)
    right_frame.grid(row=0, column=1, padx=10, pady=20, sticky=N)

    Label(left_frame, text="📘 Barr’s Battle Trace (T)", font=FONT_TITLE, bg=BG_COLOR, fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "BarrsBattleTrace.png")
    img = Image.open(image_path)
    img = img.resize((480, 350), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    image_label = Label(left_frame, image=photo, bg=BG_COLOR)
    image_label.image = photo
    image_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))
    image_label.bind("<Button-1>", lambda e: show_full_image())
    image_label.config(cursor="hand2")

    Label(left_frame, text="⚠️ Recommended values are pre-filled below. You can change them as per your needs.",
          font=("Helvetica", 10, "bold"), fg="red", bg=BG_COLOR, justify=LEFT).grid(row=2, column=0, columnspan=2, sticky=W, pady=(0, 1))

    entries = []
    input_fields = [
        ("🔵 Initial Blue Force (B₀):", 3, "200"),
        ("🔴 Initial Red Force (R₀):", 4, "200"),
        ("🔵 Final Blue Force (B𝒇):", 5, "100"),
        ("🔴 Final Red Force (R𝒇):", 6, "50"),
        ("🔵 Blue Force at time t (B(t)):", 7, "160"),
        ("🔴 Red Force at time t (R(t)):", 8, "140"),
    ]
    for text, row, default in input_fields:
        Label(left_frame, text=text, font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky=W, pady=5)
        entry = Entry(left_frame, width=30, font=FONT_NORMAL)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entries.append(entry)

    t_B0_entry, t_R0_entry, t_Bf_entry, t_Rf_entry, t_Bt_entry, t_Rt_entry = entries

    Button(left_frame, text="🔍 Calculate", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_NORMAL,
           command=submit_trace, padx=20, pady=5).grid(row=10, column=0, pady=15, sticky=W)

    Button(left_frame, text="❌ Exit", bg="crimson", fg="white", font=FONT_NORMAL,
           command=trace_window.destroy).grid(row=10, column=1, pady=15, sticky=E)

    graph_holder = Frame(right_frame, bg=BG_COLOR)
    graph_holder.pack(fill=BOTH, expand=True)

    result_holder = Frame(right_frame, bg=BG_COLOR)
    result_holder.pack(fill=X, padx=10, pady=(0, 20))

    Label(right_frame, text="🎯 Choose one of the recommended value sets from the buttons below:", bg=BG_COLOR,
          font=("Helvetica", 12, "bold"), fg="#333").pack(pady=(10, 5))

    def set_blue_efficiency():
        t_B0_entry.delete(0, END); t_B0_entry.insert(0, "200")
        t_R0_entry.delete(0, END); t_R0_entry.insert(0, "200")
        t_Bf_entry.delete(0, END); t_Bf_entry.insert(0, "100")
        t_Rf_entry.delete(0, END); t_Rf_entry.insert(0, "50")
        t_Bt_entry.delete(0, END); t_Bt_entry.insert(0, "180")
        t_Rt_entry.delete(0, END); t_Rt_entry.insert(0, "130")

    def set_red_efficiency():
        t_B0_entry.delete(0, END); t_B0_entry.insert(0, "200")
        t_R0_entry.delete(0, END); t_R0_entry.insert(0, "200")
        t_Bf_entry.delete(0, END); t_Bf_entry.insert(0, "100")
        t_Rf_entry.delete(0, END); t_Rf_entry.insert(0, "50")
        t_Bt_entry.delete(0, END); t_Bt_entry.insert(0, "120")
        t_Rt_entry.delete(0, END); t_Rt_entry.insert(0, "180")

    def set_equal_performance():
        t_B0_entry.delete(0, END); t_B0_entry.insert(0, "200")
        t_R0_entry.delete(0, END); t_R0_entry.insert(0, "200")
        t_Bf_entry.delete(0, END); t_Bf_entry.insert(0, "100")
        t_Rf_entry.delete(0, END); t_Rf_entry.insert(0, "50")
        t_Bt_entry.delete(0, END); t_Bt_entry.insert(0, "150")
        t_Rt_entry.delete(0, END); t_Rt_entry.insert(0, "125")

    button_holder = Frame(right_frame, bg=BG_COLOR)
    button_holder.pack(side=BOTTOM, pady=10)

    Button(button_holder, text="🔵 Blue's Victory", bg="blue", fg="white",
           font=("Helvetica", 10, "bold"), command=set_blue_efficiency, padx=10, pady=5).pack(side=LEFT, padx=8)

    Button(button_holder, text="🔴 Red's Victory", bg="red", fg="white",
           font=("Helvetica", 10, "bold"), command=set_red_efficiency, padx=10, pady=5).pack(side=LEFT, padx=8)

    Button(button_holder, text="⚖️ Equal Match", bg="#008080", fg="white",
           font=("Helvetica", 10, "bold"), command=set_equal_performance, padx=10, pady=5).pack(side=LEFT, padx=8)


def regression_based_mcs_model():
    def show_full_image():
        top = Toplevel(regression_window)
        top.title("Full Image - Regression-Based MCS Model")

        # Load full-size image
        full_img = Image.open(image_path)
        photo_full = ImageTk.PhotoImage(full_img)

        lbl = Label(top, image=photo_full, bg="white")
        lbl.image = photo_full  # Keep a reference!
        lbl.pack()

        # Get screen dimensions
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()

        # Get image dimensions
        img_width, img_height = full_img.size

        # Calculate center position
        x = (screen_width // 2) - (img_width // 2)
        y = (screen_height // 2) - (img_height // 2)

        # Apply centered geometry
        top.geometry(f"{img_width}x{img_height}+{x}+{y}")

    def compute_mcs_over_time():
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) >= 12:
                widget.grid_forget()
        for widget in graph_holder.winfo_children():
            widget.destroy()
        for widget in result_holder.winfo_children():
            widget.destroy()

        try:
            R0_input = r0_entry.get().strip()
            B0_input = b0_entry.get().strip()
            KMDA_input = kmda_entry.get().strip()
            WOFA_input = wofa_entry.get().strip()
            Rt_input = rt_entry.get().strip()
            Bt_input = bt_entry.get().strip()

            if not (R0_input.isdigit() and B0_input.isdigit() and KMDA_input.isdigit() and WOFA_input.isdigit()):
                raise TypeError("NonIntegerScalar")

            R0 = int(R0_input)
            B0 = int(B0_input)
            KMDA = int(KMDA_input)
            WOFA = int(WOFA_input)

            Rt_values = Rt_input.split()
            Bt_values = Bt_input.split()

            if len(Rt_values) != len(Bt_values):
                raise ValueError("LengthMismatch")
            if not all(val.isdigit() for val in Rt_values + Bt_values):
                raise TypeError("NonIntegerSeries")

            Rt_values = list(map(int, Rt_values))
            Bt_values = list(map(int, Bt_values))

            if R0 <= 0 or B0 <= 0 or KMDA <= 0 or WOFA <= 0:
                raise ValueError("NonPositive")
            if any(r < 0 for r in Rt_values) or any(b < 0 for b in Bt_values):
                raise ValueError("NegativeSeries")
            if any(r > R0 for r in Rt_values) or any(b > B0 for b in Bt_values):
                raise ValueError("FinalExceedsInitial")

            time_series = np.arange(len(Rt_values))
            MCS_scores = []

            for t in range(len(Rt_values)):
                Rt = Rt_values[t]
                Bt = Bt_values[t]

                if Rt == 0 or Bt == 0:
                    MCS_scores.append(None)
                    continue

                x1 = (R0 - Rt) / R0
                x2 = (B0 - Bt) / B0
                x3 = KMDA / WOFA
                x4 = R0 / B0
                x5 = (B0 - Bt) / Rt
                x6 = (R0 - Rt) / Bt
                x7 = (R0 - Rt) / (B0 - Bt) if (B0 - Bt) != 0 else 0

                y = (-0.2625
                    - 1.6631 * x1 + 2.5304 * x2 + 0.7799 * x3 + 0.1793 * x4 +
                    3.5277 * x5 - 2.4197 * x6 - 0.1479 * x7)

                MCS_scores.append(round(y, 3))

            global final_y
            final_y = MCS_scores[-1]

            if final_y > 0:
                outcome = "🟢 Final: Attacker has Upper Hand."
                color = "red"
            elif final_y < 0:
                outcome = "🔵 Final: Defender has Upper Hand."
                color = "blue"
            else:
                outcome = "⚪ Final: Stalemate."
                color = "gray"

            insights = (
                f"🔢 Initial Red (R₀): {R0}, Initial Blue (B₀): {B0}\n"
                f"🕓 Time steps: {len(time_series)} hours\n"
                f"📈 Final MCS Score (y): {final_y}\n"
                f"📊 R² = 0.58 (Moderate Predictive Strength)\n\n"
                f"{outcome}"
            )

            fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
            ax.plot(time_series, MCS_scores, marker='o', color='#008080', linewidth=2)
            ax.axhline(0, color='black', linestyle='--', linewidth=1)
            ax.set_xlabel("Time (hr)")
            ax.set_ylabel("MCS Score (y)")
            ax.set_title("Regression-Based MCS Over Time")
            ax.grid(True)
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=graph_holder)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True)

            Label(result_holder, text=insights, bg=BG_COLOR, font=("Helvetica", 12, "bold"), fg=color,
                wraplength=600, justify=LEFT).pack(anchor=W, padx=10, pady=(10, 0))

        except TypeError as te:
            msg = "❌ Invalid Input (Positive Integer Values Only)"
            if str(te) == "NonIntegerScalar":
                msg = "❌ Invalid Input — Only integers allowed"
            elif str(te) == "NonIntegerSeries":
                msg = "❌ Time-Series values must be positive integers"
            Label(left_frame, text=msg, bg=BG_COLOR, font=("Helvetica", 12, "bold"),
                  fg="red", wraplength=500).grid(row=12, column=0, columnspan=2, sticky=W, padx=10)

        except ValueError as ve:
            if str(ve) == "LengthMismatch":
                msg = "❌ Mismatched Time-Series Lengths"
            elif str(ve) == "NonPositive":
                msg = "❌ Inputs must be strictly positive"
            elif str(ve) == "NegativeSeries":
                msg = "❌ Negative values are not allowed"
            elif str(ve) == "FinalExceedsInitial":
                msg = "❌ Final strengths cannot exceed initial values"
            else:
                msg = "❌ Invalid Input"
            Label(left_frame, text=msg, bg=BG_COLOR, font=("Helvetica", 12, "bold"),
                  fg="red", wraplength=500).grid(row=12, column=0, columnspan=2, sticky=W, padx=10)

        except Exception:
            Label(left_frame, text="❌ Please enter valid numeric inputs", bg=BG_COLOR,
                font=("Helvetica", 12, "bold"), fg="red", wraplength=500).grid(row=12, column=0, columnspan=2, sticky=W, padx=10)

    # ========== Window Setup ==========
    regression_window = Toplevel()
    regression_window.title("Regression-Based MCS Model (Fortified Defence)")
    window_width = 1250
    window_height = 810
    screen_width = regression_window.winfo_screenwidth()
    screen_height = regression_window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    regression_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    regression_window.configure(bg=BG_COLOR)
    regression_window.bind("<Escape>", lambda e: regression_window.destroy())

    global left_frame, right_frame, graph_holder, result_holder
    left_frame = Frame(regression_window, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=30, pady=20, sticky=N)

    right_frame = Frame(regression_window, bg=BG_COLOR)
    right_frame.grid(row=0, column=1, padx=10, pady=20, sticky=N)

    Label(left_frame, text="📘 Regression-Based MCS Model", font=FONT_TITLE, bg=BG_COLOR, fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "RegressionBasedMCSModel.png")

    img = Image.open(image_path)
    img = img.resize((480, 350), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    image_label = Label(left_frame, image=photo, bg=BG_COLOR)
    image_label.image = photo
    image_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))

    image_label.bind("<Button-1>", lambda e: show_full_image())
    image_label.config(cursor="hand2")


    Label(left_frame, text="⚠️ Recommended values are pre-filled below. You can change them as per your needs.", font=("Helvetica", 10, "bold"),
          fg="red", bg=BG_COLOR).grid(row=2, column=0, columnspan=2, sticky=W, pady=(0, 1))

    entries = []
    default_values = ["500", "400", "60", "40", "500 480 450 420 390 360", "400 370 340 300 260 220"]
    input_fields = [
        ("🔴 Initial Red/Attacker's Strength (R₀):", 3),
        ("🔵 Initial Blue/Defender's Strength (B₀):", 4),
        ("📏 KMDA (Kills per MD Area):", 5),
        ("📐 WOFA (Weapon Opportunity Area):", 6),
        ("📊 Red Strengths over time (Rₜ):", 7),
        ("📊 Blue Strengths over time (Bₜ):", 8),
    ]

    for i, (text, row) in enumerate(input_fields):
        Label(left_frame, text=text, font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky=W, pady=5)
        entry = Entry(left_frame, width=30, font=FONT_NORMAL)
        entry.insert(0, default_values[i])
        entry.grid(row=row, column=1, padx=5, pady=5)
        entries.append(entry)

    r0_entry, b0_entry, kmda_entry, wofa_entry, rt_entry, bt_entry = entries

    Button(left_frame, text="🔍 Simulate", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_NORMAL,
           command=compute_mcs_over_time, padx=20, pady=5).grid(row=10, column=0, pady=15, sticky=W)

    Button(left_frame, text="❌ Exit", bg="crimson", fg="white", font=FONT_NORMAL,
           command=regression_window.destroy).grid(row=10, column=1, pady=15, sticky=E)

    graph_holder = Frame(right_frame, bg=BG_COLOR)
    graph_holder.pack(fill=BOTH, expand=True)

    # ✅ New Result Holder Frame (placed below graph)
    result_holder = Frame(right_frame, bg=BG_COLOR)
    result_holder.pack(fill=X, padx=10, pady=(0, 20))

    Label(right_frame, text="🎯 Choose one of the recommended value sets from the buttons below:", bg=BG_COLOR,
          font=("Helvetica", 12, "bold"), fg="#333").pack(pady=(10, 5))

    def set_attacker_win():
        r0_entry.delete(0, END); r0_entry.insert(0, "600")
        b0_entry.delete(0, END); b0_entry.insert(0, "400")
        kmda_entry.delete(0, END); kmda_entry.insert(0, "70")
        wofa_entry.delete(0, END); wofa_entry.insert(0, "35")
        rt_entry.delete(0, END); rt_entry.insert(0, "600 550 510 470 430")
        bt_entry.delete(0, END); bt_entry.insert(0, "400 360 310 260 200")

    def set_defender_win():
        r0_entry.delete(0, END); r0_entry.insert(0, "500")
        b0_entry.delete(0, END); b0_entry.insert(0, "600")
        kmda_entry.delete(0, END); kmda_entry.insert(0, "60")
        wofa_entry.delete(0, END); wofa_entry.insert(0, "30")
        rt_entry.delete(0, END); rt_entry.insert(0, "500 450 400 350 300")
        bt_entry.delete(0, END); bt_entry.insert(0, "600 590 580 570 560")

    button_holder = Frame(right_frame, bg=BG_COLOR)
    button_holder.pack(pady=10)

    Button(button_holder, text="🔵 Blue/Defender Wins", bg="blue", fg="white", font=("Helvetica", 10, "bold"),
           command=set_defender_win, padx=10, pady=5).pack(side=LEFT, padx=8)
    Button(button_holder, text="🔴 Enemy/Attacker Wins", bg="red", fg="white", font=("Helvetica", 10, "bold"),
           command=set_attacker_win, padx=10, pady=5).pack(side=LEFT, padx=8)


def logistic_regression_win_prob():
    def show_full_image():
        top = Toplevel(prob_window)
        top.title("Full Image - Logistic Regression Model")

        full_img = Image.open(image_path)
        photo_full = ImageTk.PhotoImage(full_img)

        lbl = Label(top, image=photo_full, bg="white")
        lbl.image = photo_full  # Keep reference
        lbl.pack()

        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        img_width, img_height = full_img.size

        x = (screen_width // 2) - (img_width // 2)
        y = (screen_height // 2) - (img_height // 2)
        top.geometry(f"{img_width}x{img_height}+{x}+{y}")

    def compute_probability():
        for widget in left_frame.grid_slaves():
            if int(widget.grid_info()['row']) >= 6:
                widget.grid_forget()
        for widget in right_frame.grid_slaves():
            widget.grid_forget()

        mcs_entry.config(state="normal")

        try:
            y_input = mcs_entry.get().strip()
            if y_input == "":
                raise ValueError("EmptyInput")
            if not y_input.replace('.', '', 1).lstrip('-').isdigit():
                raise ValueError("NonNumeric")

            y = float(y_input)

            # Constants for logistic regression
            k1 = -1.4442
            k2 = 1.0490
            exponent = k1 + k2 * y
            p_enemy_win = math.exp(exponent) / (1 + math.exp(exponent))
            p_friendly_win = 1 - p_enemy_win  # Inverted logic

            # New outcome logic (from friendly's perspective)
            if p_friendly_win > 0.57:
                outcome = "🔵 High chance friendly will win."
                color = "blue"
            elif p_friendly_win < 0.54:
                outcome = "🔴 Low chance friendly will win."
                color = "red"
            else:
                outcome = "⚪ Uncertain outcome – evenly matched."
                color = "gray"

            explanation = (
                f"• MCS (y) = {y}\n"
                f"• k₁ = {k1}, k₂ = {k2}\n"
                f"• P(friendly win) = {round(p_friendly_win, 4)}\n"
                f"• P(enemy win) = {round(p_enemy_win, 4)}\n\n"
                f"{outcome}\n"
                f"📊 R² = 0.70 (Good Predictive Fit)"
            )

            Label(right_frame, text=explanation, bg="white", font=("Helvetica", 12, "bold"), fg=color,
                justify=LEFT, wraplength=500).grid(row=1, column=0, padx=10, pady=(0, 20), sticky=W)

            # Graphing
            y_range = [i * 0.1 for i in range(-50, 51)]
            p_enemy = [math.exp(k1 + k2 * yi) / (1 + math.exp(k1 + k2 * yi)) for yi in y_range]
            p_friendly = [1 - val for val in p_enemy]

            fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
            ax.plot(y_range, p_friendly, label="Friendly Win Probability", color="blue", linewidth=2)
            ax.axhline(0.5, color='gray', linestyle='--')
            ax.axvline(y, color='black', linestyle='--', label=f"MCS = {round(y, 2)}")
            ax.plot(y, p_friendly_win, 'bo')

            ax.set_xlabel("MCS Score (y)")
            ax.set_ylabel("Probability of Friendly (Blue) Win")
            ax.set_title("Logistic Regression: Friendly Win Probability vs MCS")
            ax.legend()
            ax.grid(False)
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=right_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

        except ValueError as ve:
            msg = "❌ Invalid value entered"
            if str(ve) == "EmptyInput":
                msg = "❌ Please enter the MCS value"
            elif str(ve) == "NonNumeric":
                msg = "❌ Invalid input — MCS must be a number"

            Label(left_frame, text=msg, bg=BG_COLOR, font=("Helvetica", 12, "bold"),
                  fg="red", wraplength=500).grid(row=7, column=0, columnspan=2, sticky=W, padx=10)

        except Exception:
            Label(left_frame, text="❌ Unexpected error. Please check your input.", bg=BG_COLOR,
                  font=("Helvetica", 12, "bold"), fg="red", wraplength=500).grid(row=7, column=0, columnspan=2, sticky=W, padx=10)

    # GUI Setup remains unchanged
    prob_window = Toplevel()
    prob_window.title("Probability of Friendly Win (Logistic Regression)")

    window_width = 1300
    window_height = 700
    screen_width = prob_window.winfo_screenwidth()
    screen_height = prob_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    prob_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    prob_window.configure(bg=BG_COLOR)

    prob_window.bind("<Escape>", lambda e: prob_window.destroy())

    global left_frame, right_frame, mcs_entry
    left_frame = Frame(prob_window, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=30, pady=20, sticky=N)

    right_frame = Frame(prob_window, bg="white")
    right_frame.grid(row=0, column=1, padx=10, pady=20)

    Label(left_frame, text="📘 Logistic Regression Model", font=FONT_TITLE,
          bg=BG_COLOR, fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "LogisticRegressionModel.png")

    img = Image.open(image_path)
    img = img.resize((480, 400), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    image_label = Label(left_frame, image=photo, bg=BG_COLOR)
    image_label.image = photo
    image_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))
    image_label.bind("<Button-1>", lambda e: show_full_image())
    image_label.config(cursor="hand2")

    Label(left_frame,
          text="⚠️ You can modify values or calculate Regression Based Model to get value of MCS",
          font=("Helvetica", 10, "bold"),
          fg="red", bg=BG_COLOR).grid(row=2, column=0, columnspan=20, sticky=W, pady=(0, 15))

    Label(left_frame, text="Enter MCS Value (y):", font=FONT_NORMAL, bg=BG_COLOR).grid(row=3, column=0, sticky=W, pady=5)
    mcs_entry = Entry(left_frame, width=30, font=FONT_NORMAL)
    mcs_entry.grid(row=3, column=1, padx=5, pady=5)

    try:
        if final_y is not None:
            mcs_entry.insert(0, str(round(final_y, 4)))
            mcs_entry.config(state="readonly")
            Label(left_frame, text="(Loaded from regression output)", font=("Segoe UI", 8),
                  bg=BG_COLOR, fg="green").grid(row=4, column=0, columnspan=2)
        else:
            Label(left_frame, text="(Enter manually if not using regression)", font=("Segoe UI", 8),
                  bg=BG_COLOR, fg="gray").grid(row=4, column=0, columnspan=2)
    except:
        Label(left_frame, text="(Manual input required)", font=("Segoe UI", 8),
              bg=BG_COLOR, fg="gray").grid(row=4, column=0, columnspan=2)

    Button(left_frame, text="📊 Calculate", bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
           font=FONT_NORMAL, command=compute_probability, padx=20, pady=5).grid(row=5, column=0, pady=15, sticky=W)

    Button(left_frame, text="❌ Exit", bg="crimson", fg="white", font=FONT_NORMAL,
           command=prob_window.destroy).grid(row=5, column=1, pady=15, sticky=E)



# Constants
FONT_LARGE = ("Helvetica", 16, "bold")
FONT_NORMAL = ("Helvetica", 12)
BG_COLOR = "#f0f4f7"
BTN_COLOR = "#4a90e2"
BTN_TEXT_COLOR = "white"

root = Tk()
root.title("HOMOGENEOUS COMBAT MODELS")

# Set custom width and height
window_width = 1200
window_height = 800

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate x and y coordinates for the Tk root window
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Set the geometry and position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg="white")

# === Canvas for Scroll Support ===
main_canvas = Canvas(root, bg="white", highlightthickness=0)
main_canvas.pack(side=LEFT, fill=BOTH, expand=True)
main_canvas.pack_propagate(0)

scrollbar = Scrollbar(root, command=main_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
main_canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = Frame(main_canvas, bg="white")
scrollable_frame.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
main_canvas.create_window((0, 0), window=scrollable_frame, anchor="n", width=window_width)

# Mousewheel scroll
def on_mousewheel(event):
    main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
main_canvas.bind_all("<MouseWheel>", on_mousewheel)

# === Layout Helpers ===
def section_title(text):
    return Label(scrollable_frame, text=text, font=FONT_LARGE, bg="white", anchor="center", justify="center")

def section_subtext(text):
    return Label(scrollable_frame, text=text, font=FONT_NORMAL, bg="white", anchor="center", justify="center")

def create_button(text, command=None):
    return Button(scrollable_frame, text=text, font=FONT_NORMAL, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
                  padx=20, pady=10, width=22, command=command)

# === UI Content ===

# Section 1: Lanchester
section_title("⚔️ Lanchester's Equations of Warfare").pack(pady=(30, 5), anchor="center")
section_subtext("The various types of Warfare are as follows ⬇️").pack(pady=(0, 20), anchor="center")

frame1 = Frame(scrollable_frame, bg="white")
frame1.pack(anchor="center")
create_button("Ancient Warfare", Ancient_warfare).pack(side=LEFT, padx=10, pady=10, in_=frame1)
create_button("Modern Warfare", Modern_warfare).pack(side=LEFT, padx=10, pady=10, in_=frame1)
create_button("Area Warfare", Area_warfare).pack(side=LEFT, padx=10, pady=10, in_=frame1)

# Section 2: Other Attrition Laws
section_title("📘 Other Attrition Laws").pack(pady=(40, 5), anchor="center")
section_subtext("The Other Attrition Laws are as follows ⬇️").pack(pady=(0, 20), anchor="center")

frame2 = Frame(scrollable_frame, bg="white")
frame2.pack(anchor="center")
create_button("Peterson's Law", Peterson_warfare).pack(side=LEFT, padx=10, pady=10, in_=frame2)
create_button("Guerrilla Model", Guerrilla_warfare).pack(side=LEFT, padx=10, pady=10, in_=frame2)
create_button("Taylor Helmbold", Taylor_Helmbold_warfare).pack(side=LEFT, padx=10, pady=10, in_=frame2)

frame2b = Frame(scrollable_frame, bg="white")
frame2b.pack(anchor="center")
create_button("Hartley's Model", Hartley_warfare).pack(side=LEFT, padx=10, pady=10, in_=frame2b)

# Section 3: Termination Rules
section_title("📊 Combat Termination Rules: Analytic Approach").pack(pady=(40, 5), anchor="center")
section_subtext("The Types of Analytic Approach are ⬇️").pack(pady=(0, 20), anchor="center")

frame3 = Frame(scrollable_frame, bg="white")
frame3.pack(anchor="center")
create_button("A - Rule", A_rule_termination).pack(side=LEFT, padx=10, pady=10, in_=frame3)
create_button("P - Rule", P_rule_termination).pack(side=LEFT, padx=10, pady=10, in_=frame3)

# Section 4: Measure of Combat Success
section_title("🎯 Measure of Combat Success").pack(pady=(40, 5), anchor="center")
section_subtext("Measure of Combat Success can be done by ⬇️").pack(pady=(0, 20), anchor="center")

frame4 = Frame(scrollable_frame, bg="white")
frame4.pack(anchor="center")
create_button("Helmbold's Law", helmbold_advantage).pack(side=LEFT, padx=10, pady=10, in_=frame4)
create_button("Force Elasticity", force_elasticity).pack(side=LEFT, padx=10, pady=10, in_=frame4)
create_button("Barr’s Battle Trace", barr_battle_trace).pack(side=LEFT, padx=10, pady=10, in_=frame4)

frame4b = Frame(scrollable_frame, bg="white")
frame4b.pack(anchor="center")
create_button("Regression Based Model", regression_based_mcs_model).pack(side=LEFT, padx=10, pady=10, in_=frame4b)
create_button("Logistic Regression Model", logistic_regression_win_prob).pack(side=LEFT, padx=10, pady=10, in_=frame4b)

# Exit Button
Button(scrollable_frame, text="❌ Exit", font=FONT_NORMAL, bg="crimson", fg="white", width=20, pady=10, command=root.destroy).pack(pady=40, anchor="center")

# Run main loop
root.mainloop()