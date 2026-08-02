# -*- coding: utf-8 -*-

import numpy as np


class Octree:


    def __init__(
        self,
        points,
        indices,
        depth=0,
        max_points=50,
        max_depth=12
    ):

        self.points = points
        self.indices = indices
        self.children = []


        self.min = points[indices].min(axis=0)
        self.max = points[indices].max(axis=0)

        self.center = (
            self.min + self.max
        ) * 0.5



        if (
            len(indices) <= max_points
            or depth >= max_depth
        ):
            return



        for x in [0,1]:
            for y in [0,1]:
                for z in [0,1]:

                    mask = np.ones(
                        len(indices),
                        dtype=bool
                    )


                    for i,b in enumerate([x,y,z]):

                        if b:
                            mask &= (
                                points[indices,i]
                                >= self.center[i]
                            )
                        else:
                            mask &= (
                                points[indices,i]
                                < self.center[i]
                            )


                    child_idx = indices[mask]


                    if len(child_idx):

                        self.children.append(
                            Octree(
                                points,
                                child_idx,
                                depth+1,
                                max_points,
                                max_depth
                            )
                        )



    def distance_ray_box(self,O,D):

        invD = np.divide(
            1.0,
            D,
            out=np.full_like(
                D,
                np.inf
            ),
            where=D!=0
        )


        t1 = (
            self.min-O
        )*invD


        t2 = (
            self.max-O
        )*invD


        tmin = np.max(
            np.minimum(t1,t2)
        )


        tmax = np.min(
            np.maximum(t1,t2)
        )


        return tmax >= max(tmin,0)



    def search_ray(
        self,
        O,
        D,
        best
    ):


        if not self.distance_ray_box(O,D):
            return best



        if self.children:

            for child in self.children:

                best = child.search_ray(
                    O,
                    D,
                    best
                )


        else:

            for i in self.indices:

                P = self.points[i]


                d = np.linalg.norm(
                    np.cross(
                        P-O,
                        D
                    )
                )


                if d < best[0]:

                    best = (
                        d,
                        i
                    )


        return best