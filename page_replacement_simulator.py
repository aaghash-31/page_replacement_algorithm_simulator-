import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd
from collections import Counter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PageReplacementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Algorithm Simulator")
        self.root.geometry("1000x650")
        
        # Table Frame to display comparison results
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Other UI components...

        
        # Initialize results to prevent "undefined variable" error
        self.results = {}

        # UI Layout
        ttk.Label(root, text="Number of Frames:").grid(row=0, column=0, padx=5, pady=5)
        self.frames_entry = ttk.Entry(root)
        self.frames_entry.grid(row=0, column=1)

        ttk.Label(root, text="Reference String (comma-separated):").grid(row=1, column=0, padx=5, pady=5)
        self.ref_string_entry = ttk.Entry(root)
        self.ref_string_entry.grid(row=1, column=1)

        ttk.Label(root, text="Choose Algorithm:").grid(row=2, column=0, padx=5, pady=5)
        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("All Algorithms")
        self.algorithm_menu = ttk.Combobox(root, textvariable=self.algorithm_var, 
                                           values=["All Algorithms", "FIFO", "LRU", "Optimal", "LFU", "MRU"])
        self.algorithm_menu.grid(row=2, column=1)

        # Buttons
        self.simulate_btn = ttk.Button(root, text="Simulate", command=self.run_simulation)
        self.simulate_btn.grid(row=3, column=0, columnspan=2, pady=10)

        self.save_btn = ttk.Button(root, text="Save Results as CSV", command=self.save_metrics_to_csv)
        self.save_btn.grid(row=3, column=1, columnspan=2, pady=10)

        # Performance Metrics
        self.metrics_label = ttk.Label(root, text="", font=("Arial", 12), foreground="blue")
        self.metrics_label.grid(row=4, column=0, columnspan=2)

        # Visualization Area (Matplotlib)
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2)

    
    def run_simulation(self):
        #Runs the selected page replacement algorithm(s) and visualizes results
        try:
            num_frames = self.frames_entry.get().strip()
            if not num_frames.isdigit():
                raise ValueError("Frames should be a positive integer.")
            num_frames = int(num_frames)
            if num_frames <= 0:
                raise ValueError("Frames must be greater than 0.")

            ref_string_raw = self.ref_string_entry.get().strip()
            if not ref_string_raw:
                raise ValueError("Reference string cannot be empty.")

            ref_string = [x.strip() for x in ref_string_raw.split(",")]
            if not all(x.isdigit() for x in ref_string):
                raise ValueError("Reference string must contain only numbers separated by commas.")
            ref_string = list(map(int, ref_string))

            if not ref_string:
                raise ValueError("Reference string must contain valid numbers.")

            algorithm = self.algorithm_var.get()
            self.results = {}

            algorithms = {
                "FIFO": self.fifo,
                "LRU": self.lru,
                "Optimal": self.optimal
            }

            if algorithm == "All Algorithms":
                for algo_name, algo_func in algorithms.items():
                    page_faults, history, exec_time = self.run_algorithm(algo_func, ref_string, num_frames)
                    self.results[algo_name] = {
                        "Page Faults": page_faults,
                        "Page Hits": len(ref_string) - page_faults,
                        "Hit Ratio (%)": round(((len(ref_string) - page_faults) / len(ref_string)) * 100, 2),
                        "Execution Time (s)": exec_time
                    }
            else:
                algo_func = algorithms[algorithm]
                page_faults, history, exec_time = self.run_algorithm(algo_func, ref_string, num_frames)
                self.results[algorithm] = {
                    "Page Faults": page_faults,
                    "Page Hits": len(ref_string) - page_faults,
                    "Hit Ratio (%)": round(((len(ref_string) - page_faults) / len(ref_string)) * 100, 2),
                    "Execution Time (s)": exec_time
                }

            self.display_comparison(self.results)
            self.plot_comparison_graph(self.results)

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input! {str(e)}")


    def run_algorithm(self, algorithm_func, ref_string, frames):
        #Runs a page replacement algorithm and calculates execution time
        start_time = time.time()
        page_faults, history = algorithm_func(ref_string, frames)
        exec_time = round(time.time() - start_time, 5)
        return page_faults, history, exec_time

    def fifo(self, ref_string, frames):
        #FIFO Page Replacement Algorithm
        queue, page_faults, history = [], 0, []
        for page in ref_string:
            if page not in queue:
                if len(queue) < frames:
                    queue.append(page)
                else:
                    queue.pop(0)
                    queue.append(page)
                page_faults += 1
            history.append(queue[:])
        return page_faults, history

    def lru(self, ref_string, frames):
        #LRU Page Replacement Algorithm
        queue, page_faults, history, recent_use = [], 0, [], {}
        for i, page in enumerate(ref_string):
            if page not in queue:
                if len(queue) < frames:
                    queue.append(page)
                else:
                    least_used = min(recent_use, key=recent_use.get)
                    if least_used in queue:
                        queue.remove(least_used)
                    queue.append(page)
                page_faults += 1
            recent_use[page] = i
            history.append(queue[:])
        return page_faults, history

    def optimal(self, ref_string, frames):
        #Optimal Page Replacement Algorithm
        queue, page_faults, history = [], 0, []
        for i, page in enumerate(ref_string):
            if page not in queue:
                if len(queue) < frames:
                    queue.append(page)
                else:
                    future_use = {p: ref_string[i+1:].index(p) if p in ref_string[i+1:] else float('inf') for p in queue}
                    farthest_page = max(future_use, key=future_use.get)
                    queue.remove(farthest_page)
                    queue.append(page)
                page_faults += 1
            history.append(queue[:])
        return page_faults, history

    def display_comparison(self, results):
        #Displays a comparison table of all algorithms inside the GUI and highlights the best algorithm.
        
        # Clear previous results
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        # Find the best algorithm (minimum page faults)
        best_algo = min(results, key=lambda algo: results[algo]["Page Faults"])

        # Create Table Headers
        headers = ["Algorithm", "Page Hits", "Page Faults", "Hit Ratio (%)", "Miss Ratio (%)"]
        for col, text in enumerate(headers):
            label = ttk.Label(self.table_frame, text=text, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", padding=5)
            label.grid(row=0, column=col, sticky="nsew")

        # Fill Table with Data
        for row, (algo, data) in enumerate(results.items(), start=1):
            values = [
                algo,
                data["Page Hits"],
                data["Page Faults"],
                f"{data['Hit Ratio (%)']}%",
                f"{100 - data['Hit Ratio (%)']}%"  # Miss Ratio = 100 - Hit Ratio
            ]
            
            for col, value in enumerate(values):
                # Highlight best algorithm with a green background
                bg_color = "lightgreen" if algo == best_algo else "white"
                label = ttk.Label(self.table_frame, text=value, borderwidth=1, relief="solid", padding=5, background=bg_color)
                label.grid(row=row, column=col, sticky="nsew")

        # Adjust Column Widths
        for col in range(len(headers)):
            self.table_frame.columnconfigure(col, weight=1)

        # Show Best Algorithm Message
        best_algo_message = f"🏆 Best Algorithm: {best_algo} (Fewest Page Faults: {results[best_algo]['Page Faults']})"
        self.metrics_label.config(text=best_algo_message, font=("Arial", 12, "bold"), foreground="green")


    def plot_comparison_graph(self, results):
        #Generates a bar graph comparing all algorithms.
        self.ax.clear()
        self.ax.set_title("Algorithm Comparison")
        self.ax.set_ylabel("Page Faults")
        self.ax.grid(axis="y")

        labels = list(results.keys())
        page_faults = [results[algo]["Page Faults"] for algo in labels]

        x = np.arange(len(labels))
        width = 0.4

        self.ax.bar(x, page_faults, width, label="Page Faults", color="red")

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(labels)
        self.ax.legend()
        self.canvas.draw_idle()

    def save_metrics_to_csv(self):
        #Saves all performance metrics to a CSV file
        if not self.results:
            messagebox.showerror("Error", "No results to save! Run the simulation first.")
            return

        df = pd.DataFrame.from_dict(self.results, orient="index")
        df.to_csv("page_replacement_results.csv")
        messagebox.showinfo("Saved", "Performance metrics saved as page_replacement_results.csv")


# Run the GUI application
root = tk.Tk()
app = PageReplacementSimulator(root)
root.mainloop()
