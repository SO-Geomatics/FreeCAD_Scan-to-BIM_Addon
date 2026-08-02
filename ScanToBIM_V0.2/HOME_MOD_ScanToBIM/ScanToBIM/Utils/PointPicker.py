# -*- coding: utf-8 -*-

import FreeCADGui as Gui
import pivy.coin as coin
import numpy as np

from Utils.Octree import Octree



class PointPicker:


    def __init__(
        self,
        cloud,
        taskPanel
    ):

        self.cloud = cloud
        self.taskPanel = taskPanel

        self.running = False


        pts = cloud.Points.Points


        self.points = np.array(
            [
                (p.x,p.y,p.z)
                for p in pts
            ],
            dtype=float
        )


        print(
            len(self.points),
            "points chargés"
        )


        print(
            "Construction octree..."
        )


        self.octree = Octree(
            self.points,
            np.arange(
                len(self.points)
            )
        )


        print(
            "Octree terminé"
        )


        self.createMarker()



    # ======================================================
    # Marqueur jaune
    # ======================================================

    def createMarker(self):

        view = Gui.ActiveDocument.ActiveView

        root = view.getSceneGraph()


        self.sep = coin.SoSeparator()


        self.sep.whichChild = -1


        mat = coin.SoMaterial()

        mat.diffuseColor.setValue(
            1.0,
            1.0,
            0.0
        )


        mat.transparency = 0.7


        trans = coin.SoTranslation()


        sphere = coin.SoSphere()

        sphere.radius = 0.1


        self.translation = trans


        self.sep.addChild(
            mat
        )

        self.sep.addChild(
            trans
        )

        self.sep.addChild(
            sphere
        )


        root.addChild(
            self.sep
        )



    # ======================================================
    # Rayon caméra
    # ======================================================

    def getRay(
        self,
        x,
        y
    ):

        view = Gui.ActiveDocument.ActiveView


        cam = view.getCameraNode()


        pos = cam.position.getValue()


        O = np.array(
            [
                pos[0],
                pos[1],
                pos[2]
            ]
        )


        p = view.getPoint(
            x,
            y
        )


        P = np.array(
            [
                p.x,
                p.y,
                p.z
            ]
        )


        D = P-O


        n = np.linalg.norm(
            D
        )


        if n == 0:
            return None,None


        D /= n


        return O,D



    # ======================================================
    # Démarrage
    # ======================================================

    def start(self):

        if self.running:
            return

        self.running = True

        self.sep.whichChild = -3

        Gui.ActiveDocument.ActiveView.addEventCallback(
            "SoEvent",
            self.callback
        )



    # ======================================================
    # Arrêt
    # ======================================================

    def stop(self):

        if not self.running:
            return


        self.running = False


        try:

            Gui.ActiveDocument.ActiveView.removeEventCallback(
                "SoEvent",
                self.callback
            )

        except:

            pass


        root = Gui.ActiveDocument.ActiveView.getSceneGraph()


        try:

            root.removeChild(
                self.sep
            )

        except:

            pass



    # ======================================================
    # Recherche point
    # ======================================================

    def findPoint(
        self,
        x,
        y
    ):

        O,D = self.getRay(
            x,
            y
        )


        if O is None:
            return None


        dist,idx = self.octree.search_ray(
            O,
            D,
            (
                float("inf"),
                None
            )
        )


        if idx is None:
            return None


        return idx, self.points[idx]



    # ======================================================
    # Callback Coin
    # ======================================================

    def callback(
        self,
        event
    ):


        if not self.running:
            return



        if event["Type"] == "SoLocation2Event":


            x,y = event["Position"]


            result = self.findPoint(
                x,
                y
            )


            if result is not None:

                idx, p = result


                self.sep.whichChild = -3


                self.translation.translation.setValue(
                    float(p[0]),
                    float(p[1]),
                    float(p[2])
                )
                
            
            Gui.Selection.clearSelection()



        elif event["Type"] == "SoMouseButtonEvent":


            if (
                event["Button"] == "BUTTON1"
                and
                event["State"] == "DOWN"
            ):


                x,y = event["Position"]


                result = self.findPoint(
                    x,
                    y
                )


                if result is not None:

                    idx, p = result


                    self.taskPanel.addPoint(
                        idx,
                        p[0],
                        p[1],
                        p[2]
                    )