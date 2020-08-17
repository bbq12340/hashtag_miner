from miner import Miner
import pandas as pd
import tkinter as tk


root = tk.Tk()
root.title("Hashtag Miner")
root.geometry("350x250")

#variable
tag = tk.StringVar()
custom = tk.StringVar()
num = tk.IntVar()
interval = tk.IntVar()
sets = tk.IntVar()

#function
def start_mining():
    miner = Miner(tag.get(), custom.get(), num.get(), interval.get(), sets.get())
    miner.start_miner()
    miner.start_analyzer()

#label
hashtag_label = tk.Label(root, text="# 해시태그: ")
hashtag_label.grid(row=0, column=0, padx=5, pady=5)

custom_label = tk.Label(root, text="제외 키워드: ")
custom_label.grid(row=1, column=0, padx=5, pady=5)

num_label = tk.Label(root, text="수량: ")
num_label.grid(row=2, column=0, padx=5, pady=5)

interval_label = tk.Label(root, text="시간: ")
interval_label.grid(row=3, column=0, padx=5, pady=5)

set_label = tk.Label(root, text="세트: ")
set_label.grid(row=4, column=0, padx=5, pady=5)

mining_loading_label = tk.Label(root, text="마이닝 중...")
analyze_loading_label = tk.Label(root, text="분석 중...")

#entry
hashtag_entry = tk.Entry(root, width=10, textvariable=tag)
hashtag_entry.grid(row=0, column=1, pady=5)

custom_entry = tk.Entry(root, width=10, textvariable=custom)
custom_entry.grid(row=1, column=1, pady=5)

num_entry = tk.Entry(root, width=10, textvariable=num)
num_entry.grid(row=2, column=1, pady=5)

interval_entry = tk.Entry(root, width=10, textvariable=interval)
interval_entry.grid(row=3, column=1, pady=5)

set_entry = tk.Entry(root, width=10, textvariable=sets)
set_entry.grid(row=4, column=1, pady=5)

#button
search_button = tk.Button(root, text="Activate", command=start_mining)
search_button.grid(row=5, column=2, columnspan=2, padx=5, pady=5)


root.mainloop()