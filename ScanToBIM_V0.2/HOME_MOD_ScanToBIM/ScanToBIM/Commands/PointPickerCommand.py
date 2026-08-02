# -*- coding: utf-8 -*-

import FreeCAD as App
import FreeCADGui as Gui
import os



class PointPickerCommand:

    def GetResources(self):
        
        icon_path = os.path.join(App.getResourceDir(), "Mod", "ScanToBIM", "Resources", "icons", "PointPicker.svg")

        return {
            "MenuText": "Sélection point nuage",
            "ToolTip": "Sélectionner des points dans un nuage de points",
            "Pixmap": icon_path
        }


    def Activated(self):

        try:

            from TaskPanels.TaskPointPicker import TaskPointPicker

            panel = TaskPointPicker()

            Gui.Control.showDialog(
                panel
            )

        except Exception as e:

            print(
                "Erreur ouverture PointPicker :",
                e
            )


    def IsActive(self):

        return True