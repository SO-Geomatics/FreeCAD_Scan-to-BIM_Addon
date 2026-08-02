# ScanToBIM as FreeCAD Addon

## Features
FreeCAD already provides a powerful BIM workbench dedicated to the design of new constructions. However, modeling existing buildings requires a different approach, especially when working from laser scans or photogrammetric surveys.

To address this need, I decided to develop a set of dedicated scripts that will progressively evolve into a complete addon designed for Scan-to-BIM workflows. The goal is to provide tools that help users transform point cloud data into accurate geometric references and, ultimately, parametric BIM models of existing buildings directly within FreeCAD.

The ScanToBIM V0.2 addon currently includes a first function allowing users to intuitively select points from a point cloud directly in the 3D view and store them in a dedicated list.

This selection workflow will serve as the foundation for future features, including the automatic or assisted estimation of planes, lines, points, and other geometric references required for an efficient Scan-to-BIM process. Combined with the existing BIM capabilities of FreeCAD, this addon aims to provide a complete environment for the digital reconstruction and documentation of existing buildings.


## Development status
This ScanToBIM addon is currently **under development**. If you are interested in contributing, developing new features, or sharing ideas and suggestions, feel free to contact me.


## Installation
*Windows:*

Download all files and place them in the same directory.
Create the FREECAD_HOME environment variable and set it to your FreeCAD installation directory.

Example:

FREECAD_HOME = C:\Users\Admin\Documents\FreeCAD_1.1.3-Windows-x86_64-py311
