import numpy as np

from simframe.frame.field import Field
from simframe.integration.abstractscheme import AbstractScheme

class Instruction(AbstractScheme):
    """Integration instruction that controls the execution of integration schemes."""

    __name__ = "Instruction"

    _Y = None
    _fstep = 1.

    def __init__(self, scheme, Y, fstep=1., description=""):
        """Integration instruction
        
        Parameters
        ----------
        scheme : AbstractScheme
            Integration scheme
        Y : Field
            Variable to be integrated
        fstep : float, optional, default : 1.0
            Fraction of stepsize that this scheme should be used
        description : str, optional, default : ""
            Description of integration instruction"""
        super().__init__(scheme, description)
        self.Y = Y
        self.fstep = fstep

    @property
    def Y(self):
        return self._Y
    @Y.setter
    def Y(self, value):
        if not isinstance(value, Field):
            raise TypeError("<Y> has to be of type Field.")
        self._Y = value

    @property
    def fstep(self):
        return self._fstep
    @fstep.setter
    def fstep(self, value):
        value = np.float(value)
        if value <= 0. or value > 1.:
            msg = "\033[93mWarning:\033[0m <fstep> is not in (0, 1]."
            print(msg)
        self._fstep = value

    def __call__(self, dx=None):
        """Execution of the integration instruction
        
        Parameters
        ----------
        dx : IntVar, optional, default : None
            Stepsize of the integration variable
            
        Return
        ------
        dY : Field
            Delta of the variable to be integrated"""
        ret = self.scheme(self.Y, self.fstep*dx)
        if ret is False:
            return False
        if ret is True:
            return ret
        else:
            self.Y._buffer += ret
            return True