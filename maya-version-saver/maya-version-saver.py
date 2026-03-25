import maya.cmds as cmds
import os
import re

def get_scene_info():
    """Extract base name, version number, extension, and directory from current scene"""
    filepath = cmds.file(q=True, sceneName=True)
    if not filepath:
        # Return default values if scene has never been saved
        return "untitled", 1, ".mb", ""
    
    dir_path = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    
    # Check for version pattern like _v01, _v02 at the end of filename
    match = re.search(r'_v(\d+)$', name, re.IGNORECASE)
    if match:
        version = int(match.group(1))
        base_name = name[:match.start()]
    else:
        # No version found, start at version 1
        version = 1
        base_name = name
        
    return base_name, version, ext, dir_path

def smart_save_ui():
    """Create the UI window for smart save functionality"""
    window_id = "smartSaveWindow"
    if cmds.window(window_id, exists=True):
        cmds.deleteUI(window_id)
        
    base_name, current_v, ext, dir_path = get_scene_info()
    
    win = cmds.window(window_id, title="Version Saver", widthHeight=(350, 220), sizeable=True)
    
    cmds.columnLayout(adjustableColumn=True, rowSpacing=12, columnOffset=['both', 15])
    cmds.separator(height=15, style='none')
    
    # Display the base filename
    cmds.text(label="BASE FILENAME:", align='left', font='smallPlainLabelFont')
    cmds.text(label=base_name, align='left', font='boldLabelFont')
    
    cmds.separator(height=8, style='single')
    
    # Version control row with increment/decrement buttons
    cmds.rowLayout(numberOfColumns=4, columnWidth4=(85, 60, 45, 45))
    cmds.text(label="Version: _v", align='right', font='boldLabelFont')
    v_field = cmds.intField(value=current_v, minValue=1, width=50)
    cmds.button(label="-", width=40, height=26, c=lambda x: cmds.intField(v_field, e=True, v=max(1, cmds.intField(v_field, q=True, v=True)-1)))
    cmds.button(label="+", width=40, height=26, c=lambda x: cmds.intField(v_field, e=True, v=cmds.intField(v_field, q=True, v=True)+1))
    cmds.setParent('..') 
    
    cmds.separator(height=10, style='none')
    
    # Action buttons
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(155, 155))
    # Quick save: increment version and save immediately
    cmds.button(label="+1 & QUICK SAVE", bgc=[0.32, 0.42, 0.52], height=45, width=150,
                c=lambda x: [cmds.intField(v_field, e=True, v=cmds.intField(v_field, q=True, v=True)+1), 
                             execute_save(base_name, v_field, ext, dir_path)])
    # Save with current version number
    cmds.button(label="SAVE VERSION", height=45, width=150, bgc=[0.32, 0.52, 0.32], 
                c=lambda x: execute_save(base_name, v_field, ext, dir_path))
    
    cmds.setParent('..')
    cmds.separator(height=15, style='none')
    
    cmds.showWindow(win)

def execute_save(base_name, v_field, ext, dir_path):
    """Save the scene with the specified version number"""
    if not dir_path:
        cmds.warning("Scene has no path! Please save the file manually first.")
        return
        
    ver_val = cmds.intField(v_field, q=True, value=True)
    # Format version with leading zero (e.g., _v01, _v02)
    new_filename = "{}_v{:02d}{}".format(base_name, ver_val, ext)
    full_path = os.path.join(dir_path, new_filename).replace('\\', '/')
    
    # Determine file type based on extension
    f_type = "mayaAscii" if ext.lower() == ".ma" else "mayaBinary"
    
    try:
        cmds.file(rename=full_path)
        cmds.file(save=True, type=f_type)
        # Close UI after successful save
        if cmds.window("smartSaveWindow", exists=True):
            cmds.deleteUI("smartSaveWindow")
        print("Success: File saved as " + full_path)
    except Exception as e:
        cmds.error("Failed to save: " + str(e))

smart_save_ui()