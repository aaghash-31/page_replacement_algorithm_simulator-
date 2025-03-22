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
        """Runs the selected page replacement algorithm(s) and visualizes results."""
        try:
            # ✅ Validate number of frames
            num_frames = self.frames_entry.get().strip()
            if not num_frames.isdigit():
                raise ValueError("Frames should be a positive integer.")
            num_frames = int(num_frames)
            if num_frames <= 0:
                raise ValueError("Frames must be greater than 0.")

            # ✅ Validate and clean reference string
            ref_string_raw = self.ref_string_entry.get().strip()
            if not ref_string_raw:
                raise ValueError("Reference string cannot be empty.")

            # ✅ Convert reference string to list of integers
            ref_string = [x.strip() for x in ref_string_raw.split(",")]
            if not all(x.isdigit() for x in ref_string):
                raise ValueError("Reference string must contain only numbers separated by commas.")
            ref_string = list(map(int, ref_string))

            # ✅ Ensure reference string is not empty
            if not ref_string:
                raise ValueError("Reference string must contain valid numbers.")

            # ✅ Run selected algorithm(s)
            algorithm = self.algorithm_var.get()
            self.results = {}

            algorithms = {
                "FIFO": self.fifo,
                "LRU": self.lru,
                "Optimal": self.optimal,
                "LFU": self.lfu,
                "MRU": self.mru
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
        """Runs a page replacement algorithm and calculates execution time."""
        start_time = time.time()
        page_faults, history = algorithm_func(ref_string, frames)
        exec_time = round(time.time() - start_time, 5)
        return page_faults, history, exec_time

    def fifo(self, ref_string, frames):
        """FIFO Page Replacement Algorithm"""
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
        """LRU Page Replacement Algorithm"""
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
        """Optimal Page Replacement Algorithm"""
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

    def lfu(self, ref_string, frames):
        """LFU Page Replacement Algorithm"""
        queue, page_faults, history = [], 0, []
        counts = Counter()
        for page in ref_string:
            counts[page] += 1
            if page not in queue:
                if len(queue) < frames:
                    queue.append(page)
                else:
                    least_used = min(queue, key=lambda p: counts[p])
                    if least_used in queue:
                        queue.remove(least_used)
                    queue.append(page)
                page_faults += 1
            history.append(queue[:])
        return page_faults, history

    def mru(self, ref_string, frames):
        """MRU Page Replacement Algorithm"""
        queue, page_faults, history = [], 0, []
        for page in ref_string:
            if page in queue:
                queue.remove(page)
            elif len(queue) == frames:
                queue.pop(-1)
                page_faults += 1
            queue.append(page)
            history.append(queue[:])
        return page_faults, history

    def display_comparison(self, results):
        """Displays a comparison of all algorithms and determines the best one."""
        best_algorithm = min(results, key=lambda algo: results[algo]["Page Faults"])

        comparison_text = "\n".join([
            f"{algo}: Page Faults = {results[algo]['Page Faults']}, "
            f"Hit Ratio = {results[algo]['Hit Ratio (%)']}%, "
            f"Execution Time = {results[algo]['Execution Time (s)']}s"
            for algo in results
        ])

        best_algo_text = f"\n🥇 Best Algorithm: {best_algorithm} (Fewest Page Faults)"

        self.metrics_label.config(text=comparison_text + best_algo_text)

    def plot_comparison_graph(self, results):
        """Generates a bar graph comparing all algorithms."""
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
        """Saves all performance metrics to a CSV file."""
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
