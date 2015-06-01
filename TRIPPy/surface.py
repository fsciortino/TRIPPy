import geometry
import scipy
import scipy.linalg

edges = scipy.array(([-1,-1],
                     [-1, 1],
                     [ 1,-1],
                     [ 1, 1]))

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

    def intercept(self,ray):
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

    def area(self,sagi = None, meri = None):
        if not sagi is None:
            sagi = self.sagi.s
        if not meri is None:
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

    def edgetest(self,sagi,meri):

        if abs(meri) <= self.meri.s and abs(sagi) <= self.sagi.s:
            return True
        else:
            return False

    def split(self,sagi,meri):
        """ utilizes geometry.grid to change the rectangle into a generalized surface,
        it is specified with a single set of basis vectors to describe the meridonial,
        normal, and sagittal planes."""
        ins = float((sagi-1))/sagi
        inm = float((meri-1))/meri
        stemp = self.sagi.s/sagi
        mtemp = self.meri.s/meri

        self.sagi.s,self.meri.s = scipy.meshgrid(scipy.linspace(-self.sagi.s*ins,
                                                                 self.sagi.s*ins,
                                                                 sagi),
                                                 scipy.linspace(-self.meri.s*inm,
                                                                 self.meri.s*inm,
                                                                 meri))

        x_hat = self + self.sagi + self.meri #creates a vector which includes all the centers of the subsurface
        self.sagi.s = stemp*sagi #returns values to previous numbers
        self.meri.s = mtemp*meri

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
class Cylinder(Surf):

    def intercept(self,ray):
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

    def edge(self):
        pass

    def area(self):
        pass

    def split(self):
        pass

    def edgetest(self):
        pass
    


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
        temp = geometry.Point(geometry.Vecr((scipy.sqrt((self.sagi.s*scipy.cos(theta))**2
                                                        +(self.meri.s*scipy.sin(theta))**2)*scipy.ones(theta.shape),
                                            theta,
                                            scipy.zeros(theta.shape)))
                              ,self)

        temp.redefine(self._origin)
        return temp

    def area(self, sagi=None, meri=None):
        if not sagi is None:
            sagi = self.sagi.s
        if not meri is None:
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

    def area(self, radius=None):
        if not radius is None:
            radius = self.sagi

        super(Circle, self).area(radius, radius)

    def edgetest(self, radius=None):
        if not radius is None:
            radius = self.sagi
        super(Circle, self).edgetest(radius, 0)
