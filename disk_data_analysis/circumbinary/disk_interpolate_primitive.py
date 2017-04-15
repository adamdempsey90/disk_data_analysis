import numpy as np
from scipy.interpolate import griddata




def disk_interpolate_primitive_quantities(snapshot, XY, quantities = None):

    """
    Interpolate primitive quantity data (stored in a snapshot data structure) usually 
    evaluated in spatial locations placed in an unstructured fashion into a structured grid

    """


    
    if (quantities is None):
        quantities = ["RHO"]

        
    X,Y = XY[0], XY[1]
    x,y = snapshot.gas.POS[:,0] - snapshot.header.boxsize * 0.5, snapshot.gas.POS[:,1] - snapshot.header.boxsize * 0.5

    
    interp_quant = []
    for quant in quantities:
        
        z = getattr(snapshot.gas,quant)
        # interpolate Z values on defined grid
        Z = griddata(np.vstack((x.flatten(),y.flatten())).T, \
                          np.vstack(z.flatten()),(X,Y),method='linear').reshape(X.shape)
        interp_quant.append(Z)

    return interp_quant
        
        
