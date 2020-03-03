from __future__ import division
from __future__ import print_function
from past.utils import old_div
import TRIPPy3.surface
import TRIPPy3.beam
import scipy
import eqtools3 as eqtools

#data I found from /home/hutch/work/bolo/ -- NO DOCUMENTATION...

def ap(plasma, loc=(1.03220,.198424,.00045),angle=(0.,0.,0.)):
    
    vloc1 = TRIPPy.Vecr(loc)
    vloc2 = TRIPPy.Vecr((loc[0],loc[1],0.))
    vloc2.s = 1.0
    meri = TRIPPy.Vecx((0.,0.,1.))
    area = [.05*.0245,.52*.0245]
    return TRIPPy.surface.Rect(vloc1, plasma, area, vec=[meri,vloc2])

def det(origin, angle=(0.,old_div(scipy.pi,2), 0.), loc=(0,0,.0245*.235), radius=50e-6):
    return TRIPPy.surface.Circle(loc, origin, radius=radius, angle=angle) #actually a circular pinhole, but whatever

def dmbolo(num, plasma):
    
    loc = scipy.array([[1.03220, .198424, .00045],
                       [1.0416, 2.452484, .090805],
                       [1.02981, 2.89147, -.05969],
                       [1.03090, 3.33748, -.002550],
                       [1.0305, 5.38974, .00545],
                       [1.02872, 6.11321, .00145]])

    loc[:,1] -= old_div(scipy.pi,10)

    
    place = loc[num]

    apin = ap(plasma, place)
    temp = det(apin)
    temp.redefine(plasma)
    return [temp,apin]

def volweight(num,numsplit=(3,3), factor=1, fact2=None, eq='/home/ian/python/g1120824019.01400'):

    b =  TRIPPy.Tokamak(eqtools.EqdskReader(gfile=eq))
    
    rgrid = b.eq.getRGrid()
    zgrid = b.eq.getZGrid()
    rgrid = scipy.linspace(rgrid[0],rgrid[-1],len(rgrid)*factor)
    zgrid = scipy.linspace(zgrid[0],zgrid[-1],len(zgrid)*factor)
    
    dmbolo2 = dmbolo(num,b)
    
    surfs = dmbolo2[1].split(numsplit[0],numsplit[1])

    out = scipy.zeros((len(rgrid)-1,len(zgrid)-1))

    print((dmbolo2[0],dmbolo2[1]))

    for i in surfs:
        for j in i:
            surf2 = j
            if fact2 is None:
                surf2 = j
            else:
                surf2 = j.split(fact2,fact2)

            beam = TRIPPy.beam.multiBeam(dmbolo2[0],surf2)
            b.trace(beam)
            TRIPPy.plot.mayaplot.plotLine(beam)
            #out += TRIPPy.beam.volWeightBeam(beam,rgrid,zgrid)
    
    return out

def dmbolorays(num, plasma, avg=True):
    temp =  dmbolo(num, plasma)
    k = temp[1].edge()

    if avg:
        inp1 = TRIPPy.Point(old_div((k[:,0]+k[:,1]),2.),plasma)
        inp2 = TRIPPy.Point(old_div((k[:,2]+k[:,3]),2.),plasma)
    else:
        inp1 = TRIPPy.Point(old_div((k[:,0]+k[:,3]),2.),plasma)
        inp2 = TRIPPy.Point(old_div((k[:,1]+k[:,2]),2.),plasma)

    ray1 = TRIPPy.beam.Ray(temp[0],inp1)
    ray2 = TRIPPy.beam.Ray(temp[0],inp2)
    plasma.trace(ray1)
    plasma.trace(ray2)

    return (ray1,ray2)
