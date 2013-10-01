import geometry
import surface
import scipy

class Ray(geometry.Point):

    def __init__(self, pt1, inp2, err=[]):

        try:
            self.norm = geometry.pts2Vec(pt1, inp2)
        except AttributeError:
            self.norm = inp2
            
        self._start = scipy.array(0)
        self._end = []
        super(Ray,self).__init__(pt1.x(), pt1._origin, err=err)
        
    def trace(self, plasma, step=1e-2):
        """ extends the norm vector into finding viewing length in vessel"""

        end = plasma.getMachineCrossSection()[0].max()+self.vec.s[0]
        sin = scipy.arange(0, end, step) #start from diode, and trace through to find when it hits the vessel
        idx = 1
        invesselflag = bool(plasma.inVessel(temp[0,0], temp[2,0]))
        
        # if diode is not invessel, find when the view is in vessel
        if not invesselflag:
            flag = True
            while flag:
                pntinves = bool(plasma.inVessel(temp[0,idx], temp[2,idx]))
                idx += 1

                if pntinves or idx == sin:
                    flag = False
                invesselflag = pntinves
            self._start = sin[idx]

        # find point at which the view escapes vessel
        if invesselflag:
            flag = True
            while flag:
            
                pntinves = bool(plasma.inVessel(temp[0,idx], temp[2,idx]))
                idx += 1

                if not pntinves or idx == sin:
                    flag = False
                    idx -= 1
                invesselflag = pntinves
            self._end = sin[idx]
        self.norm.s = scipy.array([0, self._start, self._end])

    def x(self):
        return (self.vec + self.norm).x()

    def __getitem__(self,idx):
        return (self.vec + self.norm)[idx]

# generate necessary beams for proper inversion (including etendue, etc)
class Beam(geometry.Origin):
    """ generates an origin with defined etendue and non scalar.
    Beams propagation is assumed to be non-refractive, such that
    the variation in the nature of the etendue analytical. 
    """

    def __init__(self, surf1, surf2, err=[]):
        """ the beam generates a normal vector which points from
        surface 1 to surface 2.  After which the sagittal and 
        meridonial rays are simply the surface 1 sagittal and
        meridonial rays with respect """

        normal = geometry.pts2Vec(surf1, surf2)
        #orthogonal coordinates based off of connecting normal
        snew = surf1.sagi - normal*((surf1.sagi * normal)*(surf1.sagi.s/normal.s))
        mnew = surf1.meri - normal*((surf1.meri * normal)*(surf1.meri.s/normal.s))
        super(Beam, self).__init__(surf1.x(), surf1._origin, Vec = [mnew,normal], err=err)
        #calculate area at diode.
        self.sagi.s = snew.s
        a1 = surf1.area(snew.s,mnew.s)

        #calculate area at aperature
        a2 = surf2.area((((self.sagi*surf2.sagi)/self.sagi.s)**2 + ((self.meri*surf2.sagi)/self.meri.s)**2)**.5,
                        (((self.sagi*surf2.meri)/self.sagi.s)**2 + ((self.meri*surf2.meri)/self.meri.s)**2)**.5)

        #generate etendue
        self.etendue = a1*a2/(normal.s ** 2)
        self._start = scipy.array(0)
        self._end = []
       
    def trace(self, plasma, step=1e-2):
        """ extends the norm vector into finding viewing length in vessel"""

        end = plasma.getMachineCrossSection()[0].max()+self.vec.s[0]
        self.norm.s = scipy.arange(0, end, step) #start from diode, and trace through to find when it hits the vessel
        sin = self.norm.s.size
        self._redefine(plasma)

        # set if in cylindrical coordinates
        if self.flag:
            temp = self.x()
        else:
            temp = self.c().x()
        idx = 1
        invesselflag = plasma.inVessel(temp[0])
        
        # if diode is not invessel, find when the view is in vessel
        if not invesselflag:
            flag = True
            while flag:

                pntinves = plasma.inVessel(temp[idx])
                idx += 1

                if pntinves or idx == sin:
                    flag = False
                invesselflag = pntinves
            self._start = sin[idx]

        # find point at which the view escapes vessel
        if invesselflag:
            flag = True
            while flag:
            
                pntinves = plasma.inVessel(temp[idx])
                idx += 1

                if not pntinves or idx == sin:
                    flag = False
                    idx -= 1
                invesselflag = pntinves
            self._end = sin[idx]
        self.norm.s = scipy.array([0, self._start, self._end])

    def x(self):
        return (self.vec + self.norm).x()

    def __getitem__(self,idx):
        return (self.vec + self.norm)[idx]
