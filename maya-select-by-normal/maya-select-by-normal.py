import maya.cmds as cmds
import maya.api.OpenMaya as om
import math

# --- PYSIDE COMPATIBILITY LAYER ---
try:
    from PySide6 import QtWidgets, QtCore, QtGui
except ImportError:
    try:
        from PySide2 import QtWidgets, QtCore, QtGui
    except ImportError:
        cmds.error("PySide is not available in this Maya version.")

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

class SelectByNormalQt(MayaQWidgetBaseMixin, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SelectByNormalQt, self).__init__(parent)
        self.setWindowTitle("Maya Select By Normal v1.1")
        
        # Standard width 600px for UI consistency
        self.resize(600, 240)
        
        self.main_bg = QtWidgets.QFrame()
        self.main_bg.setObjectName("MainBG")
        
        # --- QSS STYLESHEET (Exact System Palette) ---
        self.setStyleSheet("""
            QFrame#MainBG { background-color: #23262d; }
            QLabel { color: #d7dce6; font-size: 14px; }
            
            QGroupBox {
                border: 1px solid #3b414d; 
                border-radius: 4px;
                margin-top: 20px; 
                padding-top: 22px; 
                font-weight: bold;
                font-size: 14px;
                color: #f1f5fb; 
                background-color: #2a2f38; 
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 8px;
            }
            QGroupBox::indicator {
                width: 0px; height: 0px; border: none;
            }
            
            QPushButton {
                background-color: #394152; 
                border: 1px solid #505a6d; 
                border-radius: 4px;
                padding: 12px;
                color: #f3f6fb; 
                font-size: 15px;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover { background-color: #455066; }
            QPushButton:pressed { background-color: #53607b; }
            
            QDoubleSpinBox {
                background-color: #1f232a; 
                border: 1px solid #434b59; 
                border-radius: 3px;
                padding: 6px;
                color: #eef2f7; 
                font-size: 14px;
            }
            QDoubleSpinBox:focus { border: 1px solid #6f8cff; }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button { width: 0px; }

            QSlider::groove:horizontal {
                border: 1px solid #3a4352; 
                height: 6px;
                background: #1b1f26; 
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: #6f8cff; 
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #d9e3ff; 
                border: 1px solid #7f93d8; 
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
        """)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        # Settings Group
        self.grp_settings = QtWidgets.QGroupBox("Tolerance Settings")
        
        self.lbl_angle = QtWidgets.QLabel("Angle Tolerance:")
        
        self.sld_angle = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sld_angle.setRange(0, 18000) 
        self.sld_angle.setValue(10) # 0.1 deg
        
        self.spn_angle = QtWidgets.QDoubleSpinBox()
        self.spn_angle.setRange(0.001, 180.0)
        self.spn_angle.setValue(0.1)
        self.spn_angle.setDecimals(3)
        self.spn_angle.setFixedWidth(90)
        self.spn_angle.setAlignment(QtCore.Qt.AlignCenter)

        # Action Button
        self.btn_select = QtWidgets.QPushButton("SELECT MATCHING FACES")

    def create_layouts(self):
        master_layout = QtWidgets.QVBoxLayout(self)
        master_layout.setContentsMargins(0, 0, 0, 0)
        master_layout.addWidget(self.main_bg)

        main_layout = QtWidgets.QVBoxLayout(self.main_bg)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # Tolerance Row
        lyt_settings = QtWidgets.QHBoxLayout(self.grp_settings)
        lyt_settings.setContentsMargins(15, 25, 15, 15)
        lyt_settings.addWidget(self.lbl_angle)
        lyt_settings.addWidget(self.sld_angle)
        lyt_settings.addWidget(self.spn_angle)
        
        main_layout.addWidget(self.grp_settings)
        main_layout.addWidget(self.btn_select)
        main_layout.addStretch()

    def create_connections(self):
        # Sync Slider and SpinBox values
        self.sld_angle.valueChanged.connect(lambda v: self.spn_angle.setValue(v / 100.0))
        self.spn_angle.valueChanged.connect(lambda v: self.sld_angle.setValue(int(v * 100)))
        self.btn_select.clicked.connect(self.execute_selection)

    def execute_selection(self):
        # Initial selection check
        sel = cmds.ls(selection=True, flatten=True)
        faces = cmds.filterExpand(sel, selectionMask=34) # 34 = Polygon Face
        
        if not faces:
            cmds.warning("Please select at least one polygon face.")
            return

        ref_face = faces[0]
        mesh_name = ref_face.split('.')[0]
        
        try:
            # Parse face index from string
            ref_index = int(ref_face.split('[')[-1].split(']')[0])
        except Exception:
            cmds.warning("Could not parse face index.")
            return

        # Prepare math threshold
        tolerance = self.spn_angle.value()
        tol_radians = math.radians(max(tolerance, 0.001))
        threshold_dot = math.cos(tol_radians)

        # OpenMaya API setup
        sel_list = om.MSelectionList()
        try:
            sel_list.add(mesh_name)
            dag_path = sel_list.getDagPath(0)
        except Exception:
            cmds.warning("Could not find mesh: " + mesh_name)
            return

        poly_iter = om.MItMeshPolygon(dag_path)
        
        # 1. Get reference face normal in object space
        poly_iter.setIndex(ref_index)
        ref_normal = poly_iter.getNormal(om.MSpace.kObject).normalize()

        faces_to_select = []
        
        # 2. Iterate through all polygons and compare normals using Dot Product
        poly_iter.reset()
        while not poly_iter.isDone():
            n = poly_iter.getNormal(om.MSpace.kObject).normalize()
            dot = ref_normal * n 
            
            if dot >= threshold_dot:
                faces_to_select.append("{}.f[{}]".format(mesh_name, poly_iter.index()))
            poly_iter.next()

        # 3. Apply final selection
        if faces_to_select:
            cmds.select(faces_to_select, replace=True)
            cmds.inViewMessage(amg="Selected {} faces.".format(len(faces_to_select)), pos='midCenter', fade=True)

# UI Instance handling
try:
    select_normal_ui.close()
    select_normal_ui.deleteLater()
except:
    pass

select_normal_ui = SelectByNormalQt()
select_normal_ui.show()
