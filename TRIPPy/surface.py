import geometry
import scipy
import scipy.linalg
import _beam

edges = scipy.array(([-1,-1],
                     [-1, 1],
                     [ 1, 1],
                     [ 1,-1]))

class Surf(geometry.Origin):
    """Surf object with inherent cartesian backend mathematics.
     
    Creates a new Surf instance which can be set to a default 
    coordinate system of cartesian or cylindrical coordinates.
    All vector mathematics are accomplished in cartesian to 
    simplify computation effort. Cylindrical vectors are
    converted at last step for return.
    
    A surface is defined by a point and two vectors. The two 
    vectors being: 1st the normal to the surface, principal axis,
    z-vector or the (0,0,1) vector of the new system defined in
    the reference system. The second vector along with the 
    first fully defines meridonial ray paths, y-vector or the
    (0,1,0) vector (.meri). The sagittal ray path, x-vector or
    the (1,0,0) is defined through a cross product (.sagi).
    Center position and rotation matricies are stored at
    instantiation.

    These conventions of norm to z, meri to y axis and sagi to
    x axis are exactly as perscribed in the OSLO optical code,
    allowing for easier translation from its data into Toroidal
    systems.

    The surface cross-sectional area is specified and used to modify
    the sagittal and meridonial vectors. This is stored as lengths 
    of the two vectors, meri and sagi. This object assumes that the 
    surface is purely normal to the input norm vector across the
    entire surface.
           
    If the angles alpha, beta, and gamma are specified following
    the eulerian rotation formalism, it is processed in the 
    following manner: alpha is the rotation from the principal
    axis in the meridonial plane, beta is the rotation about the
    plane normal to the meridonial ray, or 2nd specified vector,
    and gamma is the 2nd rotation about the principal axis. 
    This might change based on what is most physically intuitive.
    These are converted to vectors and stored as attributes.
    
    Args:
        x_hat: geometry-derived object or Array-like of size 3 or 3xN.

        ref: Origin or Origin-derived object.
            Sets the default coordinate nature of the vector to 
            cartesian if False, or cylindrical if True.

        area: 2-element tuple of scipy-arrays or values.
            This sets the cross-sectional area of the view, which
            follows the convenction [sagi,meri]. Meri is the length
            in the direction of the optical axis, and sagi is the 
            length in the off axis of the optical and normal axes.
            Values are in meters.

    Kwargs:
        vec: Tuple of two Vec objects
            The two vectors describe the normal (or z) axis and
            the meridonial (or y) axis. Inputs should follow
            [meri,normal]. If not specified, it assumed that angle
            is specified.

        angle: tuple or array of 3 floats
            alpha, beta and gamma are eulerian rotation angles which
            describe the rotation and thus the sagittal and 
            meridonial rays.
            
        flag: Boolean.
            Sets the default coordinate nature of the vector to 
            cartesian if False, or cylindrical if True.
                
    Examples:   
        Accepts all array like (tuples included) inputs, though all data 
        is stored in numpy arrays.

        Generate an origin at (0,0,0) with a :math:`\pi/2` rotation:
            
                cent = Center() #implicitly in cyl. coords.
                newy = Vecr((1.,scipy.pi,0.))
                z = Vecr((0.,0.,1.))
                ex = Origin((0.,0.,0.), cent, vec=[newy,z])

        Generate an origin at (0,0,0) with a :math:`\pi/2` rotation:
            
                cent = Center() #implicitly in cyl. coords.
                ex1 = Origin((0.,0.,0.), cent, angle=(scipy.pi/2,0.,0.))

        Generate an origin at (1,10,-7) with a cartesian coord system:

                cent = Center() #implicitly in cyl. coords.
                place = Vecx((1.,10.,-7.))
                ex2 = Origin(place, cent, angle=(0.,0.,0.), flag=False)

        Generate an origin at (1,1,1) with a cartesian coord system:

                cent = Center(flag=False) #cartesian coords.
                ex3 = Origin((1.,1.,1.), cent, angle=(0.,0.,0.))

    """

    def __init__(self, x_hat, ref, area, vec=None, angle=None, flag=None):
        """
        """

        if flag is None:
            flag = ref.flag

        super(Surf,self).__init__(x_hat, ref, vec=vec, angle=angle, flag=flag)
        self.sagi.s = scipy.atleast_1d(area[0])/2
        self.meri.s = scipy.atleast_1d(area[1])/2 
        # this utilizes an unused attribute of the geometry.Origin where 
        #the length of the defining coordinate system unit vectors are used
        #to define the cross sectional area of the surface, and the norm is
        #the normal.

    def intercept(self, ray):
        """Solves for intersection point of surface and a ray or Beam
    
        Args:
            ray: Ray or Beam object
                It must be in the same coordinate space as the surface object.
            
        Returns:
            s: value of s [meters] which intercepts along norm, otherwise an
            empty tuple (for no intersection).
        
        Examples:
            Accepts all point and point-derived object inputs, though all data 
            is stored as a python object.

            Generate an y direction Ray in cartesian coords using a Vec from (0,0,1)::
            
                    cen = geometry.Center(flag=True)
                    ydir = geometry.Vecx((0,1,0))
                    zpt = geometry.Point((0,0,1),cen)

        """
        if self._origin is ray._origin:
            try:

                params = scipy.dot(scipy.linalg.inv(scipy.array([ray.norm.unit,
                                                                 self.meri.unit,
                                                                 self.sagi.unit]).T),
                                   (ray-self).x())

                if self.edgetest(params[2],params[1]):
                    return params[0]
                else:
                    return None

            except AttributeError:
                raise ValueError('not a surface object')
        else:           
            raise ValueError('not in same coordinate system, use redefine and try again')

class Rect(Surf):
    """Origin object with inherent cartesian backend mathematics.
     
    Creates a new Origin instance which can be set to a default 
    coordinate system of cartesian or cylindrical coordinates.
    All vector mathematics are accomplished in cartesian to 
    simplify computation effort. Cylindrical vectors are
    converted at last step for return.
    
    An Origin is defined by a point and two vectors. The two 
    vectors being: 1st the normal to the surface, principal axis,
    z-vector or the (0,0,1) vector of the new system defined in
    the reference system. The second vector along with the 
    first fully defines meridonial ray paths, y-vector or the
    (0,1,0) vector (.meri). The sagittal ray path, x-vector or
    the (1,0,0) is defined through a cross product (.sagi).
    Point position and rotation matricies are stored at
    instantiation.

    These conventions of norm to z, meri to y axis and sagi to
    x axis are exactly as perscribed in the OSLO optical code,
    allowing for easier translation from its data into Toroidal
    systems.
           
    If the angles alpha, beta, and gamma are specified following
    the eulerian rotation formalism, it is processed in the 
    following manner: alpha is the rotation from the principal
    axis in the meridonial plane, beta is the rotation about the
    plane normal to the meridonial ray, or 2nd specified vector,
    and gamma is the 2nd rotation about the principal axis. 
    This might change based on what is most physically intuitive.
    These are converted to vectors and stored as attributes.
    
    Args:
        x_hat: geometry-derived object or Array-like of size 3 or 3xN.

    Kwargs:
        ref: Origin or Origin-derived object.
            Sets the default coordinate nature of the vector to 
            cartesian if False, or cylindrical if True.

        vec: Tuple of two Vector objects
            The two vectors describe the normal (or z) axis and
            the meridonial (or y) axis. Inputs should follow
            [meri,normal]. If not specified, it assumed that angle
            is specified.

        angle: tuple or array of 3 floats
            alpha, beta and gamma are eulerian rotation angles which
            describe the rotation and thus the sagittal and 
            meridonial rays.
            
        flag: Boolean.
            Sets the default coordinate nature of the vector to 
            cartesian if False, or cylindrical if True.
                
    Examples:   
        Accepts all array like (tuples included) inputs, though all data 
        is stored in numpy arrays.

        Generate an origin at (0,0,0) with a :math:`\pi/2` rotation:
            
                cent = Center() #implicitly in cyl. coords.
                newy = Vecr((1.,scipy.pi,0.))
                z = Vecr((0.,0.,1.))
                ex = Origin((0.,0.,0.), cent, vec=[newy,z])

        Generate an origin at (0,0,0) with a :math:`\pi/2` rotation:
            
                cent = Center() #implicitly in cyl. coords.
                ex1 = Origin((0.,0.,0.), cent, angle=(scipy.pi/2,0.,0.))

        Generate an origin at (1,10,-7) with a cartesian coord system:

                cent = Center() #implicitly in cyl. coords.
                place = Vecx((1.,10.,-7.))
                ex2 = Origin(place, cent, angle=(0.,0.,0.), flag=False)

        Generate an origin at (1,1,1) with a cartesian coord system:

                cent = Center(flag=False) #cartesian coords.
                ex3 = Origin((1.,1.,1.), cent, angle=(0.,0.,0.))

    """

    def area(self, sagi = None, meri = None):
        if sagi is None:
            sagi = self.sagi.s
        if meri is None:
            meri = self.meri.s

        return sagi*meri*4

    def edge(self):
        """ return points at the edge of rectangle """
        temp1 = self.sagi.x()
        temp2 = self.meri.x()
        return geometry.Point((self +
                               geometry.Vecx(scipy.dot(edges,
                                                       [temp1,temp2]).T)),
                              self._origin)

    def edgetest(self, sagi, meri):

        if abs(meri) <= self.meri.s and abs(sagi) <= self.sagi.s:
            return True
        else:
            return False

    def split(self, sagi, meri):
        """ utilizes geometry.grid to change the rectangle into a generalized surface,
        it is specified with a single set of basis vectors to describe the meridonial,
        normal, and sagittal planes."""
        ins = float((sagi - 1))/sagi
        inm = float((meri - 1))/meri
        stemp = self.sagi.s/sagi
        mtemp = self.meri.s/meri

        self.sagi.s,self.meri.s = scipy.meshgrid(scipy.linspace(-self.sagi.s*ins,
                                                                 self.sagi.s*ins,
                                                                 sagi),
                                                 scipy.linspace(-self.meri.s*inm,
                                                                 self.meri.s*inm,
                                                                 meri))

        x_hat = self + (self.sagi + self.meri) #creates a vector which includes all the centers of the subsurface
        self.sagi.s = stemp*sagi #returns values to previous numbers
        self.meri.s = mtemp*meri

        print(x_hat.x().shape)

        temp = Rect(x_hat,
                    self._origin,
                    [2*stemp,2*mtemp],
                    vec=[self.meri.copy(), self.norm.copy()],
                    flag=self.flag)
        #return temp

        return super(Rect, temp).split(temp._origin,
                                       [2*stemp,2*mtemp],
                                       vec=[temp.meri,temp.norm],
                                       flag=temp.flag,
                                       obj=type(temp))
"""
class Parabola(Surf):
"""
class Cyl(Surf):  
    """Origin object with inherent cartesian backend mathematics.
     
    Creates a new Origin instance which can be set to a default 
    coordinate system of cartesian or cylindrical coordinates.
    All vector mathematics are accomplished in cartesian to 
    simplify computation effort. Cylindrical vectors are
    converted at last step for return.
    
    An Origin is defined by a point and two vectors. The two 
    vectors being: 1st the normal to the surface, principal axis,
    z-vector or the (0,0,1) vector of the new system defined in
    the reference system. The second vector along with the 
    first fully defines meridonial ray paths, y-vector or the
    (0,1,0) vector (.meri). The sagittal ray path, x-vector or
    the (1,0,0) is defined through a cross product (.sagi).
    Point position and rotation matricies are stored at
    instantiation.

    These conventions of norm to z, meri to y axis and sagi to
    x axis are exactly as perscribed in the OSLO optical code,
    allowing for easier translation from its data into Toroidal
    systems.
           
    If the angles alpha, beta, and gamma are specified following
    the eulerian rotation formalism, it is processed in the 
    following manner: alpha is the rotation from the principal
    axis in the meridonial plane, beta is the rotation about the
    plane normal to the meridonial ray, or 2nd specified vector,
    and gamma is the 2nd rotation about the principal axis. 
    This might change based on what is most physically intuitive.
    These are converted to vectors and stored as attributes.
    
    Args:
        x_hat: geometry-derived object or Array-like of size 3 or 3xN.

    Kwargs:
        ref: Origin or Origin-derived object.
            Sets the default coordinate nature of the vector to 
            cartesian if False, or cylindrical if True.

        vec: Tuple of two Vector objects
            The two vectors describe the normal (or z) axis and
            the meridonial (or y) axis. Inputs should follow
            [meri,normal]. If not specified, it assumed that angle
            is specified.

        angle: tuple or array of 3 floats
            alpha, beta and gamma are eulerian rotation angles which
            describe the rotation and thus the sagittal and 
            meridonial rays.
            
        flag: Boolean.
            Sets the default coordinate nature of the vector to 
            cartesian if False, or cylindrical if True.
                
    Examples:   
        Accepts all array like (tuples included) inputs, though all data 
        is stored in numpy arrays.

        Generate an origin at (0,0,0) with a :math:`\pi/2` rotation:
            
                cent = Center() #implicitly in cyl. coords.
                newy = Vecr((1.,scipy.pi,0.))
                z = Vecr((0.,0.,1.))
                ex = Origin((0.,0.,0.), cent, vec=[newy,z])

        Generate an origin at (0,0,0) with a :math:`\pi/2` rotation:
            
                cent = Center() #implicitly in cyl. coords.
                ex1 = Origin((0.,0.,0.), cent, angle=(scipy.pi/2,0.,0.))

        Generate an origin at (1,10,-7) with a cartesian coord system:

                cent = Center() #implicitly in cyl. coords.
                place = Vecx((1.,10.,-7.))
                ex2 = Origin(place, cent, angle=(0.,0.,0.), flag=False)

        Generate an origin at (1,1,1) with a cartesian coord system:

                cent = Center(flag=False) #cartesian coords.
                ex3 = Origin((1.,1.,1.), cent, angle=(0.,0.,0.))

    """




    def __init__(self, x_hat, ref, area, radius, vec=None, angle=None, flag=None):
        """
        """
        if flag is None:
            flag = ref.flag

        super(Surf,self).__init__(x_hat, ref, vec=vec, angle=angle, flag=flag)
        self.norm.s = scipy.atleast_1d(area[0])/2
        self.meri.s = scipy.atleast_1d(area[1])/2 

        if self.meri.s > scipy.pi:
            raise ValueError('angle of cylinder can only be < 2*pi')
        self.sagi.s = abs(scipy.array(radius))

        # this utilizes an unused attribute of the geometry.Origin where 
        #the length of the defining coordinate system unit vectors are used
        #to define the cross sectional area of the surface, and the norm is
        #the normal.


    def intercept(self, ray):
        """Solves for intersection point of surface and a ray or Beam
    
        Args:
            ray: Ray or Beam object
                It must be in the same coordinate space as the surface object.
            
        Returns:
            s: value of s [meters] which intercepts along norm, otherwise an
            empty tuple (for no intersection).
        
        Examples:
            Accepts all point and point-derived object inputs, though all data 
            is stored as a python object.

            Generate an y direction Ray in cartesian coords using a Vec from (0,0,1)::
            
                    cen = geometry.Center(flag=True)
                    ydir = geometry.Vecx((0,1,0))
                    zpt = geometry.Point((0,0,1),cen)

        """


        # Proceedure will be to generate 
        if self._origin is ray._origin:
            try:
                rcopy = ray.copy()
                rcopy.redefine(self)
                
                intersect = _beam.interceptCyl(scipy.atleast_2d(rcopy.x()[:,-1]), 
                                               scipy.atleast_2d(rcopy.norm.unit), 
                                               scipy.array([self.sagi.s,self.sagi.s]),
                                               scipy.array([-self.norm.s,self.norm.s])) + rcopy.norm.s[-1]
                
                if not scipy.isfinite(intersect):
                    #relies on r1 using arctan2 so that it sets the branch cut properly (-pi,pi]
                    return None
                elif self.edgetest(intersect, (rcopy(intersect)).r1()):
                        return intersect
                else:
                    rcopy.norm.s[-1] = intersect
                    intersect = _beam.interceptCyl(scipy.atleast_2d(rcopy.x()[:,-1]), 
                                                   scipy.atleast_2d(rcopy.norm.unit), 
                                                   scipy.array([self.sagi.s,self.sagi.s]),
                                                   scipy.array([-self.norm.s,self.norm.s])) + rcopy.norm.s[-1]
                    if not scipy.isfinite(intersect):
                        #relies on r1 using arctan2 so that it sets the branch cut properly (-pi,pi]
                        return None
                    elif self.edgetest(intersect, (rcopy(intersect)).r1()):
                        return None
                    else:
                        return None

            except AttributeError:
                raise ValueError('not a surface object')
        else:           
            raise ValueError('not in same coordinate system, use redefine and try again')

    def edge(self, pts=20):

        if pts%2 == 1:
            raise ValueError('pts must be an even number')
            
        theta = scipy.linspace(-self.meri.s, self.meri.s, pts/2.)
        theta = scipy.concatenate([theta,theta[::-1]])
        z = self.norm.s*scipy.ones((pts,))
        z[pts/2:] = z[pts/2:] - 2*self.norm.s
        
        temp = geometry.Point(geometry.Vecr((self.sagi.s*scipy.ones((pts,)),
                                            theta,
                                             z))
                              ,self)
        
        temp.redefine(self._origin)
        return temp
        

    def area(self, sagi=None, meri=None):
        if sagi is None:
            sagi = self.sagi.s
        if meri is None:
            meri = self.meri.s

        return self.sagi.s*self.norm.s*self.meri.s


    def split(self, sagi, meri):
        """ utilizes geometry.grid to change the rectangle into a generalized surface,
        it is specified with a single set of basis vectors to describe the meridonial,
        normal, and sagittal planes."""
        ins = float((sagi - 1))/sagi
        inm = float((meri - 1))/meri
        stemp = self.norm.s/sagi
        mtemp = self.meri.s/meri

        z,theta = scipy.meshgrid(scipy.linspace(-self.norm.s*ins,
                                                self.norm.s*ins,
                                                sagi),
                                 scipy.linspace(-self.meri.s*inm,
                                                self.meri.s*inm,
                                                meri))

        vecin =geometry.Vecr((self.sagi.s*scipy.ones(theta.shape),
                              theta+scipy.pi/2,
                              scipy.zeros(theta.shape))) #this produces an artificial
        # meri vector, which is in the 'y_hat' direction in the space of the cylinder
        # This is a definite patch over the larger problem, where norm is not normal
        # to the cylinder surface, but is instead the axis of rotation.  This was
        # done to match the Vecr input, which works better with norm in the z direction
               
        pt1 = geometry.Point(geometry.Vecr((scipy.zeros(theta.shape),
                                            theta,
                                            z)),
                             self)

        pt1.redefine(self._origin)

        vecin = vecin.split()

        x_hat = self + pt1 #creates a vector which includes all the centers of the subsurface

        out = []
        #this for loop makes me cringe super hard
        for i in xrange(meri):
            try:
                temp = []
                for j in xrange(sagi):
                    inp = self.rot(vecin[i][j])
                    temp += [Cyl(geometry.Vecx(x_hat.x()[:,i,j]),
                                 self._origin,
                                 [2*stemp,2*mtemp],
                                 self.sagi.s,
                                 vec=[inp, self.norm.copy()],
                                 flag=self.flag)]
                out += [temp]
            except IndexError:
                inp = self.rot(vecin[i])
                out += [Cyl(geometry.Vecx(x_hat.x()[:,i]),
                            self._origin,
                            [2*stemp,2*mtemp],
                            self.norm.s,
                            vec=[inp, self.norm.copy()],
                            flag=self.flag)]
                

        return out
                       

    def edgetest(self, radius, angle):

        if abs(angle) <= self.meri.s:
            return True
        else:
            return False          
    
    def pixelate(self, sagi, meri):
        """ convert surface into number of rectangular surfaces"""
        ins = float((sagi - 1))/sagi
        inm = float((meri - 1))/meri
        stemp = self.norm.s/sagi
        mtemp = self.meri.s/meri

        z,theta = scipy.meshgrid(scipy.linspace(-self.norm.s*ins,
                                                self.norm.s*ins,
                                                sagi),
                                 scipy.linspace(-self.meri.s*inm,
                                                self.meri.s*inm,
                                                meri))

        vecin = geometry.Vecr((self.sagi.s*scipy.ones(theta.shape),
                               theta+scipy.pi/2,
                               scipy.zeros(theta.shape))) #this produces an artificial
        # meri vector, which is in the 'y_hat' direction in the space of the cylinder
        # This is a definite patch over the larger problem, where norm is not normal
        # to the cylinder surface, but is instead the axis of rotation.  This was
        # done to match the Vecr input, which works better with norm in the z direction
               
        pt1 = geometry.Point(geometry.Vecr((self.sagi.s*scipy.ones(theta.shape),
                                            theta,
                                            z)),
                             self)

        pt1.redefine(self._origin)
                
        vecin = vecin.split()

        x_hat = self + pt1 #creates a vector which includes all the centers of the subsurface

        out = []
        #this for loop makes me cringe super hard
        for i in xrange(meri):
            try:
                temp = []
                for j in xrange(sagi):
                    inp = self.rot(vecin[i][j])
                    temp += [Rect(geometry.Vecx(x_hat.x()[:,i,j]),
                                  self._origin,
                                  [2*stemp,2*scipy.tan(mtemp)*self.sagi.s],
                                  vec=[inp, self.sagi.copy()],
                                  flag=self.flag)]
                out += [temp]
            except IndexError:
                inp = self.rot(vecin[i])
                out += [Rect(geometry.Vecx(x_hat.x()[:,i]),
                             self._origin,
                             [2*stemp,2*scipy.tan(mtemp)*self.sagi.s],
                             vec=[inp, self.sagi.copy()],
                             flag=self.flag)]


        return out



"""
class Sphere(Surf):
"""
class Ellipse(Surf):
    """Origin object with inherent cartesian backend mathematics.
     
    Creates a new Origin instance which can be set to a default 
    coordinate system of cartesian or cylindrical coordinates.
    All vector mathematics are accomplished in cartesian to 
    simplify computation effort. Cylindrical vectors are
    converted at last step for return.
    
    An Origin is defined by a point and two vectors. The two 
    vectors being: 1st the normal to the surface, principal axis,
    z-vector or the (0,0,1) vector of the new system defined in
    the reference system. The second vector along with the 
    first fully defines meridonial ray paths, y-vector or the
    (0,1,0) vector (.meri). The sagittal ray path, x-vector or
    the (1,0,0) is defined through a cross product (.sagi).
    Point position and rotation matricies are stored at
    instantiation.

    These conventions of norm to z, meri to y axis and sagi to
    x axis are exactly as perscribed in the OSLO optical code,
    allowing for easier translation from its data into Toroidal
    systems.
           
    If the angles alpha, beta, and gamma are specified following
    the eulerian rotation formalism, it is processed in the 
    following manner: alpha is the rotation from the principal
    axis in the meridonial plane, beta is the rotation about the
    plane normal to the meridonial ray, or 2nd specified vector,
    and gamma is the 2nd rotation about the principal axis. 
    This might change based on what is most physically intuitive.
    These are converted to vectors and stored as attributes.
    
    Args:
        x_hat: geometry-derived object or Array-like of size 3 or 3xN.

    Kwargs:
        ref: Origin or Origin-derived object.
            Sets the default coordinate nature of the vector to 
            cartesian if False, or cylindrical if True.

        vec: Tuple of two Vector objects
            The two vectors describe the normal (or z) axis and
            the meridonial (or y) axis. Inputs should follow
            [meri,normal]. If not specified, it assumed that angle
            is specified.

        angle: tuple or array of 3 floats
            alpha, beta and gamma are eulerian rotation angles which
            describe the rotation and thus the sagittal and 
            meridonial rays.
            
        flag: Boolean.
            Sets the default coordinate nature of the vector to 
            cartesian if False, or cylindrical if True.
                
    Examples:   
        Accepts all array like (tuples included) inputs, though all data 
        is stored in numpy arrays.

        Generate an origin at (0,0,0) with a :math:`\pi/2` rotation:
            
                cent = Center() #implicitly in cyl. coords.
                newy = Vecr((1.,scipy.pi,0.))
                z = Vecr((0.,0.,1.))
                ex = Origin((0.,0.,0.), cent, vec=[newy,z])

        Generate an origin at (0,0,0) with a :math:`\pi/2` rotation:
            
                cent = Center() #implicitly in cyl. coords.
                ex1 = Origin((0.,0.,0.), cent, angle=(scipy.pi/2,0.,0.))

        Generate an origin at (1,10,-7) with a cartesian coord system:

                cent = Center() #implicitly in cyl. coords.
                place = Vecx((1.,10.,-7.))
                ex2 = Origin(place, cent, angle=(0.,0.,0.), flag=False)

        Generate an origin at (1,1,1) with a cartesian coord system:

                cent = Center(flag=False) #cartesian coords.
                ex3 = Origin((1.,1.,1.), cent, angle=(0.,0.,0.))

    """

    def __init__(self, x_hat, ref, area, vec=None, angle=None, flag=None):
        """
        """
 
        super(Surf,self).__init__(x_hat, ref, vec=vec, angle=angle, flag=flag)
        self.sagi.s = scipy.atleast_1d(area[0])
        self.meri.s = scipy.atleast_1d(area[1])


    def edge(self, angle=[0,2*scipy.pi], pts=20):
        theta = scipy.linspace(angle[0], angle[1], pts)
        temp = geometry.Point(geometry.Vecr((self.sagi.s*self.meri.s/scipy.sqrt((scipy.cos(theta)*self.meri.s)**2 
                                                                                +(scipy.sin(theta)*self.sagi.s)**2)*scipy.ones(theta.shape),
                                            theta,
                                            scipy.zeros(theta.shape)))
                              ,self)

        temp.redefine(self._origin)
        return temp

    def area(self, sagi=None, meri=None):
        if sagi is None:
            sagi = self.sagi.s
        if meri is None:
            meri = self.meri.s

        return scipy.pi*sagi*meri

    def edgetest(self, meri, sagi):
        if (meri/self.meri)**2+(sagi/self.sagi)**2 <= 1:
            return True
        else:
            return False

class Circle(Ellipse):
    """Origin object with inherent cartesian backend mathematics.
     
    Creates a new Origin instance which can be set to a default 
    coordinate system of cartesian or cylindrical coordinates.
    All vector mathematics are accomplished in cartesian to 
    simplify computation effort. Cylindrical vectors are
    converted at last step for return.
    
    An Origin is defined by a point and two vectors. The two 
    vectors being: 1st the normal to the surface, principal axis,
    z-vector or the (0,0,1) vector of the new system defined in
    the reference system. The second vector along with the 
    first fully defines meridonial ray paths, y-vector or the
    (0,1,0) vector (.meri). The sagittal ray path, x-vector or
    the (1,0,0) is defined through a cross product (.sagi).
    Point position and rotation matricies are stored at
    instantiation.

    These conventions of norm to z, meri to y axis and sagi to
    x axis are exactly as perscribed in the OSLO optical code,
    allowing for easier translation from its data into Toroidal
    systems.
           
    If the angles alpha, beta, and gamma are specified following
    the eulerian rotation formalism, it is processed in the 
    following manner: alpha is the rotation from the principal
    axis in the meridonial plane, beta is the rotation about the
    plane normal to the meridonial ray, or 2nd specified vector,
    and gamma is the 2nd rotation about the principal axis. 
    This might change based on what is most physically intuitive.
    These are converted to vectors and stored as attributes.
    
    Args:
        x_hat: geometry-derived object or Array-like of size 3 or 3xN.

    Kwargs:
        ref: Origin or Origin-derived object.
            Sets the default coordinate nature of the vector to 
            cartesian if False, or cylindrical if True.

        vec: Tuple of two Vector objects
            The two vectors describe the normal (or z) axis and
            the meridonial (or y) axis. Inputs should follow
            [meri,normal]. If not specified, it assumed that angle
            is specified.

        angle: tuple or array of 3 floats
            alpha, beta and gamma are eulerian rotation angles which
            describe the rotation and thus the sagittal and 
            meridonial rays.
            
        flag: Boolean.
            Sets the default coordinate nature of the vector to 
            cartesian if False, or cylindrical if True.
                
    Examples:   
        Accepts all array like (tuples included) inputs, though all data 
        is stored in numpy arrays.

        Generate an origin at (0,0,0) with a :math:`\pi/2` rotation:
            
                cent = Center() #implicitly in cyl. coords.
                newy = Vecr((1.,scipy.pi,0.))
                z = Vecr((0.,0.,1.))
                ex = Origin((0.,0.,0.), cent, vec=[newy,z])

        Generate an origin at (0,0,0) with a :math:`\pi/2` rotation:
            
                cent = Center() #implicitly in cyl. coords.
                ex1 = Origin((0.,0.,0.), cent, angle=(scipy.pi/2,0.,0.))

        Generate an origin at (1,10,-7) with a cartesian coord system:

                cent = Center() #implicitly in cyl. coords.
                place = Vecx((1.,10.,-7.))
                ex2 = Origin(place, cent, angle=(0.,0.,0.), flag=False)

        Generate an origin at (1,1,1) with a cartesian coord system:

                cent = Center(flag=False) #cartesian coords.
                ex3 = Origin((1.,1.,1.), cent, angle=(0.,0.,0.))

    """

    def __init__(self, x_hat, ref, radius, vec=None, angle=None, flag=None):
        """
        """

        super(Surf,self).__init__(x_hat, ref, vec=vec, angle=angle, flag=flag)
        self.sagi.s = scipy.atleast_1d(radius)
        self.meri.s = scipy.atleast_1d(radius)

    def area(self, radius=None, radius2=None):
        if radius is None:
            radius = self.sagi.s
        if radius2 is None:
            radius2 = self.meri.s


        return super(Circle, self).area(radius, radius2)

    def edgetest(self, radius=None):
        if radius is None:
            radius = self.sagi.s

        return super(Circle, self).edgetest(radius, 0)
