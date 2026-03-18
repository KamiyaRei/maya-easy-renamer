# Changelog

All notable changes to **Maya Easy Renamer** are documented in this file.

---

## [2.1.0]

-  **Organization:** Added **Sort in Outliner** feature to reorder selected objects alphabetically within their hierarchy.
- **Compact UI:** Merged "Cut First" and "Cut Last" functions into a single, space-saving horizontal row.
- **Enhanced Readability:** Standardized window width to **600px** and increased font sizes (14px-15px) for high-DPI monitors.
- **Naming Polish:** Renamed primary numbering action to **Set Name** for better clarity.
- **Input Refinement:** Replaced default "0" values with **Placeholder Text** in custom padding fields.

---

## [2.0.0] (Major PySide Rewrite)
- **PySide Integration:** Complete migration from `maya.cmds` UI to **PySide2/PySide6** with a cross-version compatibility layer.
- **UUID Logic:** Implemented UUID-based renaming to prevent "broken path" errors when renaming hierarchical chains.
- **Professional Styling:** Custom **QSS (Qt Style Sheets)** implementation featuring a dark palette, rounded corners, and refined hover states.
- **Smart Numbering System:**
    * Added **Radio Presets (2, 3, 4)** for instant padding selection.
    * Implemented a **Smart Custom Field** that automatically overrides presets when a value is entered.
- **Outliner Order:** Re-engineered the numbering sequence to follow the visual order in the Outliner (Top-to-Bottom).
- **Select By Normal v2.0:** Fully ported to PySide with synchronized slider/input controls and cleaned-up UI (hidden SpinBox arrows).

---

## [1.2.0]
- **Structured Layout:** Implemented collapsible `frameLayout` sections.
- **Color Palette:** Introduced the first dark grey-blue theme for better workspace integration.
- **Regex Support:** Added the `re` module for advanced search and replace operations.

---

## [1.1.0]
- Added **Sequential Numbering** with 2-digit padding.
- Implemented **Match Case** functionality.
- Added basic hierarchy-based selection sorting.

---

## [1.0.0]
- Initial release with basic Prefix, Suffix, and Search/Replace tools.

---
