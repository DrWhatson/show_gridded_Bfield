# -*- coding: utf-8 -*-
"""Script to display gridded B-field produced with GALPROP

This script produces an interactive 3D diplay of the galactic B-field model as 
produced in GALPROP using Mayavi

Examples:

    python show_gridded_Bfield.py B_field_type10.bin shape=(256,256,51) 


Command line args:

    filename  : The B-field file is just a long stream of binary double 
                precision numbers with no formatting 

    --shape=nx,ny,nz :  

                The  the shape of the array must given via the 'shape' 
                command line option or it is assumed to be a default 
                (256,256,51)

    --hslice  : Whether or not to show a semi-tranparent horizontal slice 
                showing the B-field intensity

    --mask_points=100 :

                Too many points to show at once, so thin by <mask_points> factor
                default of 100 seems to work best

    scale_factor=3 : Scale size to apply to arrows. Default=3
 

"""

import numpy as np
import mayavi.mlab as mlab
import sys, getopt

def usage():
    print """Script to display gridded B-field produced with GALPROP

This script produces an interactive 3D diplay of the galactic B-field model as 
produced in GALPROP using Mayavi

Examples:

    python show_gridded_Bfield.py B_field_type10.bin shape=(256,256,51) 


Command line args:

    filename  : The B-field file is just a long stream of binary double 
                precision numbers with no formatting 

    --shape=nx,ny,nz :  

                The  the shape of the array must given via the 'shape' 
                command line option or it is assumed to be a default 
                (256,256,51)

    --hslice  : Whether or not to show a semi-tranparent horizontal slice 
                showing the B-field intensity

    --mask_points=100 :

                Too many points to show at once, so thin by <mask_points> factor
                default of 100 seems to work best

    scale_factor=3 : Scale size to apply to arrows. Default=3
 

"""
    

def check_shape(s,n):

    xyz = s.split(',')

    if len(xyz)!=3:
        print "Error: Shape needs to be a list of 3 integers"
        sys.exit(-1)
        
    try:    
        nx = int(xyz[0])
        ny = int(xyz[1])
        nz = int(xyz[2])
    except ValueError:
        print "Error: Invalid value in shape argument"
        sys.exit(-1)

    if nx*ny*nz*3 != n:
        print "Error: Shape size does not match size of data in file"
        sys.exit(-1)
        
    return (nx,ny,nz,3)


def check_mask_points(a):
    try:
        n = int(a)
    except ValueError:
        print "Error: Invalid value in mask_points argument"
        sys.exit(-1)
        
    return n



def check_scale_factor(a):
    try:
        sf = float(a)
    except ValueError:
        print "Error: Invalid value in scale_factor argument"
        sys.exit(-1)

    return sf 
    


options = ["shape=","hslice","vslice","mask_points=","scale_factor=","help"]

# Default

shape = [256,256,51,3]
hslice = False
vslice = False
mask_points = 100
scale_factor = 3

# First check there's a filename

if len(sys.argv)<2:
    print "Require filename to be given"
    usage()
    sys.exit(-1)

try:
    opts, args = getopt.getopt(sys.argv[1:],"h",options)
except getopt.GetoptError as err:
    print str(err)
    sys.exit(-1)


# Check if help is required
for o, a in opts:
    if o in ["-h","--help"]:
        usage()
        sys.exit(0)
    
bfile = args[0]

# Try openning it
try:
    data = np.fromfile(bfile,dtype=np.double)
except IOError:
    print "Problem opening file %s" % bfile
    sys.exit(-1)

nelem = len(data)
    
    
for o, a in opts:
    if o == "--shape":
        shape = check_shape(a,nelem)
    elif o=="--hslice":
        hslice = True
    elif o=="--vslice":
        vslice = True
    elif o=="--mask_points":
        mask_points = check_mask_points(a)
    elif o=="--scale_factor":
        scale_factor = check_scale_factor(a)
    else:
        print "Something odd happened!"
        sys.exit(-1)
        
data.shape=shape

nx = shape[0]
ny = shape[1]
nz = shape[2]

dx = nx/2+1
dy = ny/2+1
dz = nz/2+1

if hslice:
    amp = np.sqrt(data[:,:,dz,0]**2+data[:,:,dz,1]**2+data[:,:,dz,2]**2)
    mlab.imshow(amp,opacity=0.6,reset_zoom=False)

mlab.quiver3d(data[:,:,:,0],data[:,:,:,1],data[:,:,:,2],mask_points=mask_points,scale_factor=scale_factor,extent=[-dx,dx,-dy,dy,-dz,dz])

mlab.show()
