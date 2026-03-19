# Maya Toolbox

A collection of Python scripts designed to streamline workflow, improve scene management, and automate repetitive tasks.

---

## Available Tools

### 1. [Easy Renamer](./maya-easy-renamer/)
A comprehensive bulk renaming tool featuring a PySide interface and UUID-based logic for safe hierarchy management.
* **Key Features:** Sequential numbering, Search & Replace (Regex/Match Case), Prefix/Suffix, and Outliner sorting.

### 2. [Select by Normal](./maya-select-by-normal/)
A component selection utility built with OpenMaya API 2.0.
* **Key Features:** Dot product based face selection with synchronized slider and high-precision input (0.001° tolerance).

### 3. [CV Cluster Create](./maya-cv-cluster-create/)
A utility for quickly creating clusters on CV points of curves.
* **Key Features:** One-click cluster creation for selected CVs, ideal for rigging workflows and curve-based controls.

### 4. [Chroma BG Toggle](./maya-chroma-bg-toggle/)
A simple viewport utility to toggle a chroma key background.
* **Key Features:** Instantly switch viewport background to green (chroma key) and back to default.

---

## Installation

1. Navigate to the folder of the desired tool.
2. Copy the content of the `.py` script.
3. Open the **Script Editor** in Maya and paste the code into a **Python** tab.
4. Highlight the code and drag it to your **Shelf** with the Middle Mouse Button to create a shortcut.

---

## Notes

- All tools are designed to be lightweight and independent.
- No external dependencies required.
- Tested in Maya 2024
