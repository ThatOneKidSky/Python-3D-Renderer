import numpy as np

class Cube:
    verticies = np.array([
        # X Y Z          # R G B A
        -.5, -.5, -.5,    1.0, 0.0, 0.0, 1.0, # 0 Front Top    Left
         .5, -.5, -.5,    0.0, 1.0, 0.0, 1.0, # 1 Front Top    Right
         .5,  .5, -.5,    0.0, 0.0, 1.0, 1.0, # 2 Front Bottom Right
        -.5,  .5, -.5,    1.0, 1.0, 0.0, 1.0, # 3 Front Bottom Left
        
        -.5, -.5,  .5,    1.0, 1.0, 0.0, 1.0, # 4 Back  Top    Left
         .5, -.5,  .5,    0.0, 1.0, 1.0, 1.0, # 5 Back  Top    Right
         .5,  .5,  .5,    1.0, 1.0, 1.0, 1.0, # 6 Back  Bottom Right
        -.5,  .5,  .5,    0.0, 0.0, 0.0, 1.0, # 7 Back  Bottom Left
    ], dtype=np.float32)
    indices = np.array([
        # Front
        0, 1, 2,   2, 3, 0,
        # Back
        4, 5, 6,   6, 7, 8,
        # Top
        0, 1, 5,   5, 4, 0,
        # Bottom
        2, 3, 6,   6, 7, 2,
        # Left
        0, 3, 4,   4, 7, 0,
        # Right
        1, 2, 5,   5, 6, 1,
    ], dtype=np.uint32)

    stride = 7