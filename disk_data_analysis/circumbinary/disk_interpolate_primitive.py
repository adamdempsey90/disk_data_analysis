import numpy as np
from scipy.interpolate import griddata,interp2d


class grid_polar():    
    def __init__(self,NR=None,Nphi=None,Rmin=1.0,Rmax=10.0,scale='log'):
        self.NR = NR
        self.Nphi = Nphi
        if (scale == 'log'):
            self.R, self.phi = np.meshgrid(np.logspace(np.log10(Rmin),np.log10(Rmax),NR),\
	                                   np.linspace(0,2*np.pi,Nphi))
        elif (scale == 'linear'):
             self.R, self.phi = np.meshgrid(np.arange(Rmin,Rmax,(Rmax-Rmin)/NR),\
                                            np.linspace(0,2*np.pi-np.pi/Nphi,Nphi))
            
        self.X, self.Y = self.R * np.cos(self.phi), self.R * np.sin(self.phi)
        #self.phi =
        #self.R = 

class grid_cartesian():    
    def __init__(self,NX=None,NY=None,Xmin=-10.0,Xmax=10.0,Ymin=-10.0,Ymax=10.0):
        self.NX = NR
        self.NX = Nphi

        self.X, self.Y = np.meshgrid(np.arange(Xmin + 0.5 * (Xmax-Xmin)/self.NX,Xmax,(Xmax-Xmin)/self.NX),\
                                     np.arange(Ymin + 0.5 * (Ymax-Ymin)/NY,Ymax,(Ymax-Ymin)/self.NY))
        


        
def interpolate_quantities(x,y, gridXY, quantity):

    """
    Interpolate primitive quantity data (stored in a snapshot data structure) usually 
    evaluated in spatial locations placed in an unstructured fashion into a structured grid

    """

        
    X,Y = gridXY[0], gridXY[1]

    # interpolate Z values on defined grid
    Z = griddata(np.vstack((x.flatten(),y.flatten())).T, \
                 np.vstack(quantity.flatten()),(X,Y),method='linear').reshape(X.shape)

    return Z
        

def disk_interpolate_primitive_quantities(snapshot, gridXY, quantities = None):

    if (quantities is None):
        quantities = ["RHO"]


    x,y = snapshot.gas.POS[:,0], snapshot.gas.POS[:,1]
    
    interp_quant = []
    for quant in quantities:
        quant = getattr(snapshot.gas,quant)
        interp_quant.append(interpolate_quantities(x,y, [gridXY[0],gridXY[1]], quant))
        
    return  interp_quant



def compute_gradient_on_grid(x,y,quantity,grid):

    
    quantity_interp = interpolate_quantities(x,y, [grid.X,grid.Y], quantity)

    delta_x = np.diff(grid.X).mean()
    delta_y = np.diff(grid.Y).mean()
    grad = np.gradient(quantity_interp,varargs=[delta_x,delta_y])

    gradx = grad[0].reshape(quantity_interp.shape)
    grady = grad[1].reshape(quantity_interp.shape)

    local_gradx = interp2d(grid.X,grid.Y,gradx)(x,y)

    print local_gradx.shape
