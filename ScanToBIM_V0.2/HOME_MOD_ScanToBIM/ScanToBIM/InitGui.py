# -*- coding: utf-8 -*-

import FreeCAD as App
import FreeCADGui as Gui


class ScanToBIMWorkbench(Gui.Workbench):
    
    def __init__(self):
        
        # FreeCAD theme to get the right Workbench icon
        FCAD_theme_param = App.ParamGet("User parameter:BaseApp/Preferences/MainWindow")
        FCAD_theme = FCAD_theme_param.GetString("Theme")
        
        print(f"Theme Freecad: '{FCAD_theme}'")
        
        if FCAD_theme == "FreeCAD Dark":
            ScanToBIM_Icon_Name = "ScanToBIM_dark.svg"
        elif FCAD_theme == "FreeCAD Light":
            ScanToBIM_Icon_Name = "ScanToBIM_light.svg"
        else:
            print("ScanToBIM - Theme Classic ou personnalisé - icon << Dark >>")
            ScanToBIM_Icon_Name = "ScanToBIM_light.svg"
            
        __dirname__ = os.path.join(FreeCAD.getResourceDir(), "Mod", "ScanToBIM")
        self.__class__.Icon = os.path.join(__dirname__, "Resources", "icons", ScanToBIM_Icon_Name)
        
        
        def QT_TRANSLATE_NOOP(context, text):
            return text

        self.__class__.MenuText = QT_TRANSLATE_NOOP("scantobim", "ScanToBIM")
        
        _tooltip = "The Scan To BIM workbench is used for 3D reconstruction from pointcloud to parametric elements"
        self.__class__.ToolTip = QT_TRANSLATE_NOOP("scantobim", _tooltip)


    def Initialize(self):

        from Commands.PointPickerCommand import PointPickerCommand


        Gui.addCommand(
            "ScanToBIM_PointPicker",
            PointPickerCommand()
        )


        self.appendToolbar(
            "ScanToBIM",
            [
                "ScanToBIM_PointPicker"
            ]
        )


        self.appendMenu(
            "ScanToBIM",
            [
                "ScanToBIM_PointPicker"
            ]
        )


    def GetClassName(self):

        return "Gui::PythonWorkbench"



Gui.addWorkbench(
    ScanToBIMWorkbench()
)