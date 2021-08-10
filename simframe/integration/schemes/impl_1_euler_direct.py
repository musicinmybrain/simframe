from simframe.integration.scheme import Scheme

import numpy as np


def _f_impl_1_euler_direct(x0, Y0, dx, *args, **kwargs):
    """Implicit 1st-order Euler integration scheme with direct matrix inversion

    Parameters
    ----------
    x0 : Intvar
        Integration variable at beginning of scheme
    Y0 : Field
        Variable to be integrated at the beginning of scheme
    dx : IntVar
        Stepsize of integration variable
    args : additional positional arguments
    kwargs : additional keyworda arguments

    Returns
    -------
    dY : Field
        Delta of variable to be integrated

    Butcher tableau
    ---------------
     1 | 1
    ---|---
       | 1 
    """
    jac = Y0.jacobian(x0 + dx)  # Jacobian
    N = jac.shape[0]            # Problem size
    eye = np.eye(N)             # Identity matrix
    A = eye - dx[0] * jac
    return (np.linalg.inv(A) - eye) @ Y0


impl_1_euler_direct = Scheme(
    _f_impl_1_euler_direct, description="Implicit 1st-order direct Euler method")
