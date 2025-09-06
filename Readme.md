# 🪖 Warfare Simulation Models

A **Python-based warfare simulation and visualization tool** implementing **14 classical and modern warfare/attrition models**.

It provides an **interactive GUI (Tkinter)** where users can input parameters, run simulations, and visualize outcomes with **dynamic graphs (Matplotlib)**. The tool is useful for **defense analysis, research, education, and exploring theoretical combat outcomes**.

---

## 🚀 Features
- ⚔️ **14 Warfare/Attrition Models Implemented** (see list below)
- 📉 **Dynamic graphs** of force strength over time
- 🎛️ **Interactive GUI** with input fields, presets, and robust error handling
- 🖼️ **Model-specific images** with click-to-zoom (Pillow)
- 🔵 **Friendly (Blue)** vs 🔴 **Enemy (Red)** color coding
- ⏸️ **Threshold-based early termination** and “what-if” outcome analysis

---

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Libraries:**
  - `tkinter` → Graphical User Interface
  - `matplotlib` → Data Visualization
  - `pillow` (PIL) → Image Processing
  - `numpy` → Numerical Computation

---

## 📊 Models Implemented (14 Total)

### 🗡️ Classical Warfare Models
1. Ancient Warfare Model  
2. Modern Warfare Model (Lanchester’s Square Law)  
3. Area Warfare Model (Lanchester’s Linear Law)

### 📘 Other Attrition Laws
4. Peterson’s Law  
5. Guerrilla Warfare Model  
6. Taylor–Helmbold Model  
7. Hartley’s Model

### ⏸️ Combat Termination Rules: Analytic Approach
8. A-Rule  
9. P-Rule

### 🎯 Measure of Combat Success
10. Helmbold’s Law  
11. Force Elasticity  
12. Barr’s Battle Trace  
13. Regression-Based Model  
14. Logistic Regression Model

---

## 📦 Installation & Usage

1) **Clone the repository**
```bash
git clone https://github.com/yourusername/warfare-simulation.git
cd warfare-simulation
