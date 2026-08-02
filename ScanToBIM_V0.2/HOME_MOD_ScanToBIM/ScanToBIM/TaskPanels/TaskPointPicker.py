# -*- coding: utf-8 -*-

import FreeCAD as App
import FreeCADGui as Gui
from Utils.PointPicker import PointPicker

from PySide import QtWidgets


class TaskPointPicker:


    def __init__(self):

        self.points = []
        self.selectedIndexes = set()
        self.cloud = None
        self.picker = None


        self.form = QtWidgets.QWidget()

        layout = QtWidgets.QVBoxLayout(
            self.form
        )


        # ====================================================
        # Nuage
        # ====================================================

        title = QtWidgets.QLabel(
            "Nuage de points"
        )

        layout.addWidget(title)


        self.cloudName = QtWidgets.QLabel(
            "Aucun nuage sélectionné"
        )

        layout.addWidget(
            self.cloudName
        )


        self.selectCloudButton = QtWidgets.QPushButton(
            "Sélectionner le nuage"
        )

        self.selectCloudButton.clicked.connect(
            self.selectCloud
        )

        layout.addWidget(
            self.selectCloudButton
        )



        # ====================================================
        # Tableau points
        # ====================================================

        title2 = QtWidgets.QLabel(
            "Points sélectionnés"
        )

        layout.addWidget(title2)
        
        self.finishButton = QtWidgets.QPushButton(
            "Terminer la sélection des points"
        )

        self.finishButton.clicked.connect(
            self.finishSelection
        )

        layout.addWidget(
            self.finishButton
        )


        self.table = QtWidgets.QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(
            [
                "N°",
                "X",
                "Y",
                "Z"
            ]
        )

        layout.addWidget(
            self.table
        )



        # ====================================================
        # Boutons
        # ====================================================

        buttons = QtWidgets.QHBoxLayout()


        self.clearButton = QtWidgets.QPushButton(
            "Vider"
        )

        self.clearButton.clicked.connect(
            self.clearPoints
        )


        buttons.addWidget(
            self.clearButton
        )


        layout.addLayout(
            buttons
        )



    # ========================================================
    # Obligatoire TaskPanel
    # ========================================================

    def accept(self):

        self.stop()

        return True



    def reject(self):

        self.stop()

        return True



    def getStandardButtons(self):

        return (
            QtWidgets.QDialogButtonBox.Close
        )



    # ========================================================
    # Sélection nuage
    # ========================================================

    def selectCloud(self):

        sel = Gui.Selection.getSelection()


        if len(sel) != 1:

            App.Console.PrintError(
                "Sélectionnez un seul nuage de points\n"
            )

            return


        obj = sel[0]


        if not hasattr(obj, "Points"):

            App.Console.PrintError(
                "L'objet sélectionné n'est pas un nuage de points\n"
            )

            return


        self.cloud = obj


        self.cloudName.setText(
            obj.Label
        )


        App.Console.PrintMessage(
            "Nuage chargé : "
            + obj.Label
            + "\n"
        )


        # arrêt ancien sélecteur éventuel
        if self.picker:

            self.picker.stop()


        # création nouveau sélecteur
        self.picker = PointPicker(
            self.cloud,
            self
        )


        self.picker.start()



    # ========================================================
    # Gestion points
    # ========================================================

    def addPoint(self, idx, x, y, z):


        if idx in self.selectedIndexes:

            App.Console.PrintMessage(
                "Point déjà sélectionné\n"
            )

            return


        self.selectedIndexes.add(idx)


        self.points.append(
            (idx, x, y, z)
        )


        row = self.table.rowCount()

        self.table.insertRow(
            row
        )


        values = [
            idx,
            x,
            y,
            z
        ]


        for col,value in enumerate(values):

            item = QtWidgets.QTableWidgetItem(
                f"{value}"
            )

            self.table.setItem(
                row,
                col,
                item
            )



    def finishSelection(self):

        if self.picker:

            self.picker.stop()

            App.Console.PrintMessage(
                "Sélection des points terminée\n"
            )


        self.finishButton.setEnabled(
            False
        )
    
    
    
    def clearPoints(self):

        self.points.clear()
        self.selectedIndexes.clear()

        self.table.setRowCount(
            0
        )



    def stop(self):

        if self.picker:

            self.picker.stop()

            self.picker = None
            
    def close(self):

        self.stop()
