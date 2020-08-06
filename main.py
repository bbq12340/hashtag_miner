from miner import Miner, analyze
import pandas as pd
import tkinter as tk


root = tk.Tk()
root.title("Hashtag Miner")
root.geometry("400x400")

#variable
tag = tk.StringVar()
interval = tk.IntVar()
sets = tk.IntVar()

#function
def start_mining():
    search_button.grid_forget()
    analyze_button.grid_forget()
    mining_loading_label.grid(row=3, column=0, columnspan=2, pady=5)
    Miner(hashtag_entry.get(), intervals=interval_entry.get(), sets=set_entry.get())
def start_analyze():
    search_button.grid_forget()
    analyze_button.grid_forget()
    analyze_loading_label.grid(row=3, column=0, columnspan=2, pady=5)
    analyze("hashtag.csv")

#label
hashtag_label = tk.Label(root, text="# 해시태그: ")
hashtag_label.grid(row=0, column=0, padx=5, pady=5)

interval_label = tk.Label(root, text="시간: ")
interval_label.grid(row=1, column=0, padx=5, pady=5)

set_label = tk.Label(root, text="세트: ")
set_label.grid(row=2, column=0, padx=5, pady=5)

mining_loading_label = tk.Label(root, text="마이닝 중...")
analyze_loading_label = tk.Label(root, text="분석 중...")

#entry
hashtag_entry = tk.Entry(root, textvariable=tag)
hashtag_entry.grid(row=0, column=1, pady=5)

interval_entry = tk.Entry(root, textvariable=interval)
interval_entry.grid(row=1, column=1, pady=5)

set_entry = tk.Entry(root, textvariable=sets)
set_entry.grid(row=2, column=1, pady=5)

#button
search_button = tk.Button(root, text="마이닝 시작", command=start_mining)
search_button.grid(row=3, column=0, columnspan=2, pady=5)

analyze_button = tk.Button(root, text="분석 시작", command=start_analyze)
analyze_button.grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()