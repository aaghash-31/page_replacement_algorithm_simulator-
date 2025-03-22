# Page Replacement Algorithm Simulator   
A Python-based **GUI simulator** using **Tkinter** that compares different **page replacement algorithms** (FIFO, LRU and Optimal).  
It provides **visualizations** and **performance metrics** to analyze algorithm efficiency.

---

##  Features  
 **Supports 3 Page Replacement Algorithms:**  
- **FIFO (First-In-First-Out)**  
- **LRU (Least Recently Used)**  
- **Optimal Page Replacement**  

 **Graphical User Interface (GUI) using Tkinter**  
 **Displays performance metrics:**  
   - **Page Hits & Page Faults**  
   - **Hit Ratio & Miss Ratio**  
   - **Execution Time for Each Algorithm**  
 **Bar Chart Comparison of Algorithms**  
 **CSV Export of Results**  

---

## 📌 Installation  
### Step 1: Clone the Repository  
```bash  
git clone https://github.com/aaghash-31/page_replacement_algorithm_simulator-.git  
cd page_replacement_algorithm_simulator-  
```  

### Step 2: Install Dependencies  
```bash  
pip install -r requirements.txt  
```  

### Step 3: Run the Simulator  
```bash  
python page_replacement_simulator.py  
```  

---

## 📌 Usage Guide  
1️⃣ **Enter the number of frames.**  
2️⃣ **Provide a reference string** (comma-separated numbers, e.g., `7, 5, 6, 4, 7, 5, 4, 7, 8, 3`).  
3️⃣ **Select an algorithm** or choose **"All Algorithms"** to compare.  
4️⃣ **Click "Simulate"** to view results.  
5️⃣ **Check the performance metrics and bar chart.**  
6️⃣ **Click "Save as CSV"** to store results for analysis.  

---

## 📌 Example Input & Output  
### Example Input  
- **Frames:** `3`  
- **Reference String:** `7, 5, 6, 4, 7, 5, 4, 7, 8, 3`  
- **Algorithm:** `All Algorithms`  

### Example Output  
| Algorithm  | Page Hits | Page Faults | Hit Ratio (%) | Miss Ratio (%) |  
|------------|----------|------------|--------------|--------------|  
| **FIFO**   | 2        | 8          | **20.0%**    | **80.0%**    |  
| **LRU**    | 3        | 7          | **30.0%**    | **70.0%**    |  
| **Optimal**| 4        | 6          | **40.0%**    | **60.0%**    |   

---


## 📌 How It Works?  
Each page replacement algorithm **simulates memory management** by:  
✔ **Keeping a limited number of frames (memory slots).**  
✔ **Replacing pages using FIFO, LRU or Optimal strategy.**  
✔ **Tracking page hits (when a page is already in memory).**  
✔ **Tracking page faults (when a page needs to be loaded).**  
