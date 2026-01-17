import numpy as np
from ellipse import LsqEllipse as LsqE


class LsqEllipseNew(LsqE):
    """
    Ellipse representation following Wolfram MathWorld conventions.

    This class is a thin wrapper around the parent ellipse-fitting class
    and corrects a definition inconsistency present in the original
    implementation.

    In the original parent class, the ellipse parameters `width` and
    `height` are inverted with respect to the standard mathematical
    definition of an ellipse as described in
    https://mathworld.wolfram.com/Ellipse.html. As a consequence, an
    ellipse whose major axis is aligned with the x-axis is returned
    with a position angle `phi = 90 deg`, instead of the expected
    `phi = 0 deg`.

    This child class restores the Wolfram MathWorld notation, ensuring
    that:
      - `width` corresponds to the semi-major axis,
      - `height` corresponds to the semi-minor axis,
      - the position angle `phi` follows the standard mathematical
        convention.

    Using this class does not reimplement the ellipse fitting itself.
    Instead, it relies entirely on the parent class for the fitting
    procedure and post-processes the results to enforce the correct
    geometric conventions.

    Notes
    -----
    This class makes direct use of the parent ellipse-fitting
    implementation. Any scientific work making use of this class
    must therefore also cite the original software:

    .. code-block:: bibtex

        @software{ben_hammel_2020_3723294,
          author       = {Ben Hammel and Nick Sullivan-Molina},
          title        = {bdhammel/least-squares-ellipse-fitting: v2.0.0},
          month        = mar,
          year         = 2020,
          publisher    = {Zenodo},
          version      = {v2.0.0},
          doi          = {10.5281/zenodo.3723294},
          url          = {https://doi.org/10.5281/zenodo.3723294}
        }

    See Also
    --------
    ParentEllipseClass :
        Original ellipse fitting implementation upon which this class
        is based.
    """
    def as_parameters(self):
        """
        Return ellipse parameters in Wolfram MathWorld convention.

        Returns
        -------
        x0 : float
            x-coordinate of the ellipse center.
        y0 : float
            y-coordinate of the ellipse center.
        width : float
            Semi-major axis of the ellipse.
        height : float
            Semi-minor axis of the ellipse.
        phi : float
            Position angle of the major axis measured counter-clockwise
            from the x-axis, in radians.
        """

        # Eigenvectors are the coefficients of an ellipse in general form
        # the division by 2 is required to account for a slight difference in
        # the equations between (*) and (**)
        # a*x^2 +   b*x*y + c*y^2 +   d*x +   e*y + f = 0  (*)  Eqn 1
        # a*x^2 + 2*b*x*y + c*y^2 + 2*d*x + 2*f*y + g = 0  (**) Eqn 15
        # We'll use (**) to follow their documentation
        a = self.coefficients[0]
        b = self.coefficients[1] / 2.
        c = self.coefficients[2]
        d = self.coefficients[3] / 2.
        f = self.coefficients[4] / 2.
        g = self.coefficients[5]

        # Finding center of ellipse [eqn.19 and 20] from (**)
        x0 = (c*d - b*f) / (b**2 - a*c)
        y0 = (a*f - b*d) / (b**2 - a*c)
        center = (x0, y0)

        # Find the semi-axes lengths [eqn. 21 and 22] from (**)
        numerator = 2 * (a*f**2 + c*d**2 + g*b**2 - 2*b*d*f - a*c*g)
        denominator1 = (b**2 - a*c) * ( np.sqrt((a-c)**2+4*b**2) - (c+a))  # noqa: E201
        denominator2 = (b**2 - a*c) * (-np.sqrt((a-c)**2+4*b**2) - (c+a))
        width = np.sqrt(numerator / denominator1)
        height = np.sqrt(numerator / denominator2)

        # Angle of counterclockwise rotation of major-axis of ellipse to x-axis
        # [eqn. 23] from (**)
        # w/ trig identity eqn 9 form (***)
        if b == 0 and a < c:
            phi = 0.0
        elif b == 0 and a > c:
            phi = np.pi/2
        elif b != 0 and a < c:
            phi = 0.5 * np.arctan(2*b/(a-c))
        elif b != 0 and a > c:
            phi = 0.5 * (np.pi + np.arctan(2*b/(a-c)))
        elif a == c:
            phi = 0.0
        else:
            raise RuntimeError("Unreachable")

        return center, width, height, phi
    
    def inside(self, x, y, threshold = 0.9):
        # Check if coordinate (x, y) are withing the ellipse 
        #   that has been fit previously returing the following
        
        (xc, yc), a, b, phi = self.as_parameters()

        c, s = np.cos(phi), np.sin(phi)
        R = np.array( [[c, -s], [s, c]])
        v = np.vstack( (x-xc, y-yc) )    
        v = R.T@v
        condition = (v[0]/a)**2 + (v[1]/b)**2 < threshold

        return condition
